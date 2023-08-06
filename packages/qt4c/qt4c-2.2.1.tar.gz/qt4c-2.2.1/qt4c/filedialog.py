# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making QT4C available.  
# Copyright (C) 2020 THL A29 Limited, a Tencent company.  All rights reserved.
# QT4C is licensed under the BSD 3-Clause License, except for the third-party components listed below. 
# A copy of the BSD 3-Clause License is included in this file.
#

'''文件窗口模块
'''

from qt4c.qpath import QPath
from qt4c.control import ControlContainer
import qt4c.wincontrols as win
import six

class FileDialog(win.Window, ControlContainer):
    '''文件窗口基类
    '''
    def __init__(self,qpath=None):
        '''constructor
        '''
        win.Window.__init__(self, locator=qpath)
        ControlContainer.__init__(self)
        locators = {
#            '打开按钮'     :{'type':win.Control, 'root':self, 'locator': QPath('/Caption = "打开(&O)" && visible="True"')}, #打开按钮
            '文件名编辑框' :{'type':win.Control, 'root':self, 'locator': QPath('/ClassName="ComboBoxEx32" && Visible="True"')},#顶上那个combobox
            '文件.文件路径展示框' :{'type':win.ComboBox, 'root':self, 'locator': QPath('/ControlId = "0x471" && visible="True" && MaxDepth = "2"')},#显示当前文件夹名称的combox
             '取消按钮':{'type':win.Control, 'root':self, 'locator': QPath('/Caption ~= "取消" && visible="True"')}, #取消按钮
                    }
        self.updateLocator(locators)
    
    @property
    def FilePath(self):
        '''返回当前文件路径。如果没有选择文件，返回的是当前文件夹路径
        '''
        import ctypes
        import win32con, win32gui
        import qt4c.util as util
        
        hwnd = self.HWnd
        size = win32con.MAX_PATH
        pid = self.ProcessId
        pm = util.ProcessMem(pid, size)
        msgid = win32con.CDM_GETFILEPATH
        rdsize = win32gui.SendMessage(hwnd, msgid, size, pm.Buffer)
        if rdsize <= 0:
            return None
        else:
            buff = ctypes.create_unicode_buffer(rdsize)
            pm.read(buff, ctypes.sizeof(buff))
            if six.PY2:
                return buff.value.encode('utf8')
            return buff.value
        
class OpenFileDialog(FileDialog):
    '''打开文件窗口
    '''    
    def __init__(self):
        FileDialog.__init__(self,QPath("/Caption ~= '打开' && Classname ~= '#32770' && Visible='True'"))
        locators = {
            '打开按钮'   :{'type':win.Control, 'root':self, 'locator': QPath('/Caption = "打开(&O)" && visible="True"')}, #打开按钮
            '图像.文件类型'   :{'type':win.Control, 'root':self, 'locator': QPath('/Caption~= "图像文件" && visible="True"')}, #打开图片窗口的文件类型Combox
            '文件.文件类型':{'type':win.Control, 'root':self, 'locator': QPath('/Caption~= "All Files" && visible="True"')}, #打开文件窗口的文件类型Combox
            '输入框':{'type':win.Control, 'root':self, 'locator': QPath("/ClassName='ComboBoxEx32'&&Visible='True'/ClassName='ComboBox'/ClassName='Edit'")}, #输入框              
            '内容显示区':{'type':win.Control, 'root':self, 'locator':QPath("/Caption='FolderView'&&Visible='True'&&MaxDepth = '2'") }, #输入框    
             '打开.文件浏览窗口':{'type':win.Control, 'root':self, 'locator': QPath("/ClassName='SHELLDLL_DefView'&&Visible='True'")}, #XP打开文件里的文件浏览窗口      
              '打开.win7文件浏览窗口':{'type':win.Control, 'root':self, 'locator': QPath("/ClassName='SysListView32'&& Caption = 'FolderView' && Visible='True' && MaxDepth = '3'")}, #win7打开文件里的文件浏览窗口       
              }
        self.updateLocator(locators)
    
    def open(self,filename):
        
        self.bringForeground()
        self.Controls['文件名编辑框'].Text=filename
        self.Controls['打开按钮'].click()
        self.waitForInvalid(timeout=30)

class SelectFileDialog(FileDialog):
    '''选择文件/文件夹窗口，适用于1.90之后发送文件打开的窗口
    '''    

    def __init__(self):
        FileDialog.__init__(self,QPath("|Caption ~= '选择文件/文件夹' && Classname ~= '#32770' && Visible='True'"))
        locators = {
            '发送按钮'   :{'type':win.Control, 'root':self, 'locator': QPath('/Caption = "发送(&S)" && visible="True"')}, #打开按钮
            '图像.文件类型'   :{'type':win.Control, 'root':self, 'locator': QPath('/Caption~= "图像文件" && visible="True"')}, #打开图片窗口的文件类型Combox
            '文件.文件类型':{'type':win.Control, 'root':self, 'locator': QPath('/Caption~= "All Files" && visible="True"')}, #打开文件窗口的文件类型Combox
            '输入框':{'type':win.Control, 'root':self, 'locator': QPath("/ClassName='ComboBoxEx32'&&Visible='True'/ClassName='ComboBox'/ClassName='Edit'")}, #输入框              
            'xp内容显示区':{'type':win.Control, 'root':self, 'locator':QPath("/Caption='FolderView'&&Visible='True'&&MaxDepth = '2'") }, #输入框
            'win7内容显示区':{'type':win.Control, 'root':self, 'locator':QPath("/ClassName='DirectUIHWND'&&Visible='True'&&MaxDepth = '5'") }, #输入框    
            '打开.文件浏览窗口':{'type':win.Control, 'root':self, 'locator': QPath("/ClassName='SHELLDLL_DefView'&&Visible='True'&&MaxDepth = '4'")}, #XP打开文件里的文件浏览窗口      
            '打开.win7文件浏览窗口':{'type':win.Control, 'root':self, 'locator': QPath("/ClassName='SHELLDLL_DefView'&&Visible='True'&&MaxDepth = '4'")}, #win7打开文件里的文件浏览窗口       
              }
        self.updateLocator(locators)
    
    def open(self,filename):
        self.bringForeground()
        self.Controls['文件名编辑框'].Text = filename
        self.Controls['发送按钮'].click()
        self.waitForInvalid(timeout=30)
        
class SaveAsDialog(FileDialog):
    '''另存为窗口
    '''    
    def __init__(self):
        FileDialog.__init__(self,QPath("/Caption ~= '存' && Classname = '#32770' && Visible='True'"))
        locators = {
             '保存按钮'   :{'type':win.Control, 'root':self, 'locator': QPath('/Caption = "保存(&S)" && visible="True"')}, #打开按钮
            '取消按钮'   :{'type':win.Control, 'root':self, 'locator': QPath('/Caption = "取消" && visible="True"')}, #打开按钮
            '输入框'    :{'type':win.Control, 'root':self, 'locator': QPath('/ClassName="ComboBoxEx32" && Visible="True"/ClassName="ComboBox" /ClassName="Edit"')},#xp
            'win7输入框'     :{'type':win.Control, 'root':self, 'locator': QPath('/ClassName="Edit"&&MaxDepth = "5"')},#win7
            '保存类型'   :{'type':win.ComboBox, 'root':self, 'locator': QPath('/Caption ~= "\." &&ClassName="ComboBox" && Visible="True" ')}, #保存类型Combox            
            '保存在'   :{'type':win.Control, 'root':self, 'locator':  QPath('/ClassName="ComboBox" && Visible="True" &&Instance = "0"')}, #xp保存类型Combox            
            '文件路径选择框'   :{'type':win.Control, 'root':self, 'locator':  QPath('/ClassName="Breadcrumb Parent" && Visible="True" &&MaxDepth = "5"/ClassName="ToolbarWindow32"')}, #win7上的文件路径
            '文件路径编辑框'   :{'type':win.Control, 'root':self, 'locator':  QPath('/ClassName="WorkerW"/ClassName="Edit"&&MaxDepth = "6"')}, #win7上的文件路径
                  }
        self.updateLocator(locators)
        
    def save(self, filepath, style=None):
        '''保存至路径
        
        :param filepath: 要保存至的全路径
        :type filepath: string
        :param style: 保存类型
        :type style: string
        '''
        self.bringForeground()
        import platform
        if platform.release() == 'XP':
            self.Controls['输入框'].Text = filepath
        else:
            self.Controls['win7输入框'].Text = filepath
        if style != None:
            self.Controls['保存类型'].SelectedIndex = style
        self.Controls['保存按钮'].click()
        self.waitForInvalid()
 

        
class BrowseDialog(FileDialog):
    '''浏览文件夹窗口
    '''    
    def __init__(self):
        FileDialog.__init__(self,QPath("/Caption = '浏览文件夹' && Classname = '#32770' && Visible='True'"))
        locators = {
            '保存按钮'   :{'type':win.ComboBox, 'root':self, 'locator': QPath('/Caption = "保存(&S)" && visible="True"')}, #打开按钮
            '保存类型'   :{'type':win.Control, 'root':self, 'locator': QPath('/Caption~="图像文件" && ClassName="ComboBox" && Visible="True"')}, #保存类型Combox            
             
                    }
        self.updateLocator(locators)
 

class BrowseFolderDialog(win.Window):
    '''浏览文件夹窗口
    '''
    def __init__(self):
        win.Window.__init__(self, locator=QPath("/Caption = '浏览文件夹' && Classname = '#32770' && Visible='True'"))
        locators = {
            '确定按钮'  :{'type':win.Control, 'root':self, 'locator': QPath("/Caption = '确定' && Visible='True' && maxDepth= '2'")},
            '取消按钮'  :{'type':win.Control, 'root':self, 'locator': QPath("/Caption = '取消' && Visible='True' && maxDepth= '2'")},
            '选择您要发送的文件夹':   {'type':win.TreeView, 'root':self, 'locator': QPath("/classname='SHBrowseForFolder ShellNameSpace Control' /ClassName='SysTreeView32' && Visible='True'")},           
                    }
        self.updateLocator(locators)
        
        
class FileFolder(FileDialog):
    '''打开文件窗口
    '''
    def __init__(self):
        FileDialog.__init__(self,QPath("/Classname= 'CabinetWClass' && Visible='True'"))
        locators = {
            '文件.文件浏览窗口'   :{'type':win.Control, 'root':self, 'locator': QPath('/ControlId = "0x1" && visible="True" && MaxDepth="7"')}, #打开件夹后文件的展示窗口
            
              }
        self.updateLocator(locators)

class ExploreFileFolder(FileDialog):
    '''XP左边有文件树型结构的文件窗口
    '''
    def __init__(self):
        FileDialog.__init__(self,QPath("/Classname='ExploreWClass' && Visible='True'"))
        locators = {
            '文件地址显示框'   :{'type':win.Control, 'root':self, 'locator': QPath('/ControlId = "0xA205" && Classname="Edit" && visible="True" && MaxDepth="5"')}, 
            
              }
        self.updateLocator(locators)

class Win7ExploreFileFolder(FileDialog):
    '''win7下在aio中打开收到文件的文件夹窗口
    '''
    
    def __init__(self):
        FileDialog.__init__(self,QPath("/Classname='CabinetWClass' && Visible='True'"))
        locators = {
            '文件地址显示框'   :{'type':win.Control, 'root':self, 'locator': QPath('/ControlId = "0x3E9" && Classname="ToolbarWindow32" && visible="True" && MaxDepth="8"')}, 
            
              }
        self.updateLocator(locators)
        
if __name__ == '__main__':
    pass
