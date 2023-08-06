# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making QT4C available.  
# Copyright (C) 2020 THL A29 Limited, a Tencent company.  All rights reserved.
# QT4C is licensed under the BSD 3-Clause License, except for the third-party components listed below. 
# A copy of the BSD 3-Clause License is included in this file.
#
'''
qpath模块

详见QPath类说明
'''

import re
import pythoncom
import win32gui
import winerror
from pkg_resources import iter_entry_points

from qt4c import wincontrols
from qt4c import uiacontrols
from qt4c import util
from qt4c.exceptions import ControlExpiredError,ControlAmbiguousError,ControlNotFoundError
import testbase.logger as logger
import six

class EnumQPathKey(object):
    MAX_DEPTH = "MAXDEPTH"
    INSTANCE = "INSTANCE"
    UI_TYPE = "UITYPE"

class EnumUIType(object):
    WIN = 'Win'
    UIA = 'UIA'

class QPathError(Exception):
    """QPath异常类定义
    """
    pass


class QPath(object):
    '''Query Path类，使用QPath字符串定位UI控件
    
    QPath的定义：
    Qpath ::= Seperator UIObjectLocator Qpath
    Seperator ::= 路径分隔符，任意的单个字符
    UIObjectLocator ::= UIObjectProperty && UIObjectLocator
    UIObjectProperty ::= UIProperty | RelationProperty | IndexProperty | UITypeProperty 
    UIProperty ::= [Window/UIA/Html]Property Operator “Value”
    UITypeProperty ::= Win | UIA | Html
    RelationProperty ::= MaxDepth = "Number"(最大搜索子孙深度)
    IndexProperty ::= Instance="Integer"(Integer:找到的多个控件中的第几个（负数表示从后往前数）)
    
    Operator ::= '=' | '~=' ('=' 表示精确匹配; '~=' 表示用正则表达式匹配) 
     
    UI控件基本上都是由树形结构组织起来的。为了方便定位树形结构的节点，QPath采用了路径结构
    的字符串形式。 QPath以第一个字符为路径分隔符，如 "/Node1/Node2/Node3"和 “|Node1|Node2|Node3"是一样的路径，都表示先找到Node1，再在Node1的子孙节点里找Node2，然后在Node2的子孙节点里
    找Node3。而定位每个Node需要改节点的多个属性以"&&"符号连接起来, 形成    "/Property1='value1' && property2~='value2' && ..."的形式，其中"~="表示正则匹配。QPath支持的属性包括wincontrols.Window和htmlcontrols.HtmlElement的类属性。QPath中的每个节点都有两个默认属性'UIType'和'MaxDepth'。 "UIType='Win32|UIA|Html'"，三个取值分别对应了三种QPath支持的UI类型。当UIType没有指定时默认取值为父节点的值。而"MaxDepth"表示该节点离祖先节点的最大深度，
    如果没有明确指定时默认取值为'1',即直接父子关系。QPath还支持"Instance”属性，用于当找到多个节点时指定选择第几个节点。
    
    例子：
    Qpath ="/ ClassName='TxGuiFoundation' && Caption~='QQ\d+' && Instance='-1' 
            / UIType='UIA' && name='mainpanel' && MaxDepth='10'"
    '''
    
    PROPERTY_SEP = '&&'
    OPERATORS = ["=", "~="]
    MATCH_FUNCS = {}
    MATCH_FUNCS["="]=lambda x, y: x == y
    MATCH_FUNCS["~="]= lambda string, pattern: re.search(pattern, string) != None
    CONTROL_TYPES = {
                   EnumUIType.WIN: wincontrols.Control,
                   EnumUIType.UIA: uiacontrols.Control
                   }
    
    def __init__(self, qpath_string):
        """Contructor
        
        :type qpath_string: string
        :param qpath_string: QPath字符串   
        """
        self.update_control_type()
        if not isinstance(qpath_string, six.string_types):
            raise QPathError("输入的QPath(%s)不是字符串!"  % (qpath_string) )
        self._strqpath = qpath_string
        self._path_sep, self._parsed_qpath = self._parse(qpath_string)
        self._error_qpath = None

    def update_control_type(self):
        for ep in iter_entry_points("qt4c.controls"):
            control_class = ep.load()
            self.CONTROL_TYPES[ep.name] = control_class
     

    def _find_controls_recur(self, root, qpath):
        '''递归查找控件
        
        :param root: 根控件
        :param qpath: 解析后的qpath结构
        :return: 返回(found_controls, remain_qpath)， 其中found_controls是找到的控件，remain_qpath
        是未能找到控件时剩下的未能匹配的qpath。
        '''
        qpath = qpath[:]
        props = qpath[0]
        props = dict((entry[0].upper(), entry[1]) for entry in props.items()) #使属性值大小写不敏感
        max_depth = 1 #默认depth是1
        if ( EnumQPathKey.MAX_DEPTH in props):
            max_depth = int(props[EnumQPathKey.MAX_DEPTH][1])
            if max_depth <= 0 :
                raise QPathError("MaxDepth=%s应该>=1" % max_depth)
            del props[EnumQPathKey.MAX_DEPTH]
        
        instance = None #默认没有index属性
        if (EnumQPathKey.INSTANCE in props):
            instance = int(props[EnumQPathKey.INSTANCE][1])
            del props[EnumQPathKey.INSTANCE]
            
        children = None
        if EnumQPathKey.UI_TYPE in props:
            uitype = props[EnumQPathKey.UI_TYPE][1]
            del props[EnumQPathKey.UI_TYPE]  
            child_ctrl_type = self.CONTROL_TYPES[uitype]
            if not isinstance(root, child_ctrl_type):
                try:
                    children = [child_ctrl_type(root)]
                except:
                    children = []
        if children is None:
            try:
                children = root.Children
            except ControlExpiredError:
                children = []
                
        found_child_controls = []
        for ctrl in children:
            if(self._match_control(ctrl, props)):
                found_child_controls.append(ctrl)
            
            if(max_depth > 1): 
                props_copy = props.copy()
                props_copy[EnumQPathKey.MAX_DEPTH] = ['=', str(max_depth - 1)]
                _controls, _ = self._find_controls_recur(ctrl, [props_copy])
                found_child_controls += _controls
        if not found_child_controls:
            return [], qpath
        
        if instance != None:
            try:
                found_child_controls = [found_child_controls[instance]]
            except IndexError:
                return [], qpath
        
        qpath.pop(0)
        
        if not qpath: #找到控件
            return found_child_controls, qpath
            
        else: #在子孙中继续寻找
            found_ctrls = []
            error_path = qpath
            for root in found_child_controls:
                ctrls, remain_qpath = self._find_controls_recur(root, qpath)
                found_ctrls += ctrls
                if len(remain_qpath) < len(error_path):
                    error_path = remain_qpath
            # remove same control
            cpy_found_ctrls = found_ctrls[:]
            found_ctrls = []
            for ctrl in cpy_found_ctrls:
                if ctrl not in found_ctrls:
                    found_ctrls.append(ctrl)
                    
            return found_ctrls, error_path
    

    def _match_control(self, control, props):
        """控件是否匹配给定的属性
        
        :param control: 控件
        :param props: 要匹配的控件属性字典，如{'classname':['=', 'window']}
        """
        attrs = dict((attr.upper(), attr) for attr in dir(control))
        for propname in props:
            if not propname in attrs:
                return False
            
            try: 
                act_prop_value = getattr(control, attrs[propname])
            except pythoncom.com_error as e: 
                return False
            except win32gui.error as e:
                if e.winerror == winerror.ERROR_INVALID_WINDOW_HANDLE: #无效窗口句柄
                    return False
                else:
                    raise e
            except ControlExpiredError as e:
                return False
                                   
            operator, exp_prop_value = props[propname]
            if act_prop_value is None:
                return False
            
            if isinstance(act_prop_value, bool):
                if exp_prop_value.upper() == 'TRUE':
                    exp_prop_value = True
                elif exp_prop_value.upper() == 'FALSE':
                    exp_prop_value = False
                else:
                    raise QPathError('不正确的bool属性值:%s' % exp_prop_value)
                if act_prop_value != exp_prop_value:
                    return False
            
            elif isinstance(act_prop_value, six.integer_types):
                if re.search('^0x', exp_prop_value) != None:
                    exp_prop_value = int(exp_prop_value, 16)
                else:
                    exp_prop_value = int(exp_prop_value)
                if act_prop_value != exp_prop_value:
                    return False
            
            elif isinstance(exp_prop_value, six.string_types):
                if not self.MATCH_FUNCS[operator](util.myEncode(act_prop_value), util.myEncode(exp_prop_value)):
                    return False
                    
            else:
                raise QPathError('不支持控件属性值类型：%s' % type(act_prop_value))
            
        return True            

    def _parse_property(self, prop_str):
        """解析property字符串，返回解析后结构
        
        例如将 "ClassName='Dialog' " 解析返回 {ClassName: ['=', 'Dialog']}
        """
        
        parsed_pattern = "(\w+)\s*([=~!<>]+)\s*[\"'](.*)[\"']"
        match_object = re.match(parsed_pattern, prop_str)
        if match_object is None:
            raise QPathError("属性(%s)不符合QPath语法" % prop_str)
        prop_name, operator, prop_value = match_object.groups()
        if not operator in self.OPERATORS:
            raise QPathError("QPath不支持操作符：%s"  % operator) 
        return {prop_name: [operator, prop_value]}
        
    def _parse(self, qpath_string):
        """解析qpath，并返回QPath的路径分隔符和解析后的结构
        
        将例如"| ClassName='Dialog' && Caption~='SaveAs' | UIType='UIA' && ControlID='123' && Instanc='-1'"
        的QPath解析为下面结构：[{'ClassName': ['=', 'Dialog'], 'Caption': ['~=', 'SaveAs']}, {'UIType': ['=', 'UIA'], 'ControlID': ['=', '123'], 'Instance': ['=', '-1']}]
        
        :param qpath_string: qpath 字符串
        :return: (seperator, parsed_qpath)
        """
        qpath_string = qpath_string.strip()
        seperator = qpath_string[0]
        locators = qpath_string[1:].split(seperator)
        
        parsed_qpath = []
        for locator in locators:
            props = locator.split(self.PROPERTY_SEP)
            parsed_locators = {}
            for prop_str in props:
                prop_str = prop_str.strip()
                if len(prop_str) == 0: 
                    raise QPathError("%s 中含有空的属性。" % locator)
                parsed_props = self._parse_property(prop_str)
                parsed_locators.update(parsed_props)
            parsed_qpath.append(parsed_locators)
        return seperator, parsed_qpath
       
    def __str__(self):
        '''返回格式化后的QPath字符串
        '''
        qpath_str = ""
        for locator in self._parsed_qpath:
            qpath_str += self._path_sep + " "
            delimit_str = " " + self.PROPERTY_SEP + " "
            locator_str = delimit_str.join(["%s %s '%s'"  % (key, locator[key][0], locator[key][1]) for key in locator])
            qpath_str += locator_str
        return qpath_str

    def getErrorPath(self):
        """返回最后一次QPath.search搜索未能匹配的路径
        
        :rtype: string
        """
        if self._error_qpath:
            props = self._error_qpath[0]
            delimit_str = " " + self.PROPERTY_SEP + " "
            return delimit_str.join(["%s %s '%s'" % (key, props[key][0], props[key][1]) for key in props]) 
        
    def search(self, root=None):
        """根据qpath和root查找控件
        
        :type root: 实例类型
        :param root:  查找开始的控件
        :return: 返回找到的控件列表
        """
        
        if root is None:
            root = wincontrols.Control() # desktop Control
        controls, self._error_qpath = self._find_controls_recur(root, self._parsed_qpath)
        return controls
    
def _find_by_name(root, name):
    qp = QPath("/Name='%s'&&MaxDepth='50'" % name)
    controls = qp.search(root)
    count = len(controls)
    if count > 1:
        logger.warning("根据qpath<%s>找到%d个控件，请优化qpath" % (qp._strqpath,count))
        return controls[0]
    elif count == 0:
        print(qp._strqpath)
        raise ControlNotFoundError("<%s>对应的控件不存在" % qp._strqpath)
    else:
        return controls[0]
        
if __name__ == '__main__':
    pass
