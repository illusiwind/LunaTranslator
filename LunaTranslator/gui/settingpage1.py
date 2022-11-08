
from PyQt5.QtWidgets import   QLabel 
import functools 
from utils.config import globalconfig 
from traceback import print_exc
import os
import gui.switchbutton 
from utils.getpidlist import getarch
import gui.attachprocessdialog   
from textsource.textractor import textractor
def clicksourcefuntion(self,i):
    if i==0:
        self.copyboardswitch.click()
    elif i==1:
        self.ocrswitch.click()
    elif i==2:
        self.textractorswitch.click()
def setTabOne(self) :
        self.clicksourcesignal.connect(functools.partial(clicksourcefuntion,self))
  
        grids=[
                [ (QLabel('选择文本输入源'),3)],
                [   (QLabel('剪贴板'),3),(self.getsimpleswitch(globalconfig['sourcestatus'],'copy',name='copyboardswitch',callback=functools.partial(textsourcechange,self,'copy')),1),'',
                    (QLabel('OCR'),3),(self.getsimpleswitch(globalconfig['sourcestatus'],'ocr',name='ocrswitch',callback=functools.partial(textsourcechange,self,'ocr')),1),'',
                    (QLabel('Textractor'),3),(self.getsimpleswitch(globalconfig['sourcestatus'],'textractor',name='textractorswitch',callback=functools.partial(textsourcechange,self,'textractor')),1)],
                [(QLabel(''),10),(QLabel('选择游戏'),3),(self.getcolorbutton(globalconfig ,'',enable=globalconfig['sourcestatus']['textractor'],name='selectbutton',icon='fa.gear',constcolor="#FF69B4",callback=functools.partial(settingtextractor,self) ),1)],
                [(QLabel(''),10),(QLabel('选择文本'),3),(self.getcolorbutton(globalconfig ,'',enable=globalconfig['sourcestatus']['textractor'],name='selecthookbutton',icon='fa.gear',constcolor="#FF69B4",callback=functools.partial(settingsource,self)),1)],
                [''], 
                [(QLabel('提取的文本自动复制到剪贴板'),3),(self.getsimpleswitch(globalconfig ,'outputtopasteboard',name='outputtopasteboard'),1)],
                
        ] 
        self.yitiaolong("基本设置",grids)
        
 
        self.sourceswitchs={'copy':self.copyboardswitch,'ocr':self.ocrswitch,'textractor':self.textractorswitch}# ,'textractor_pipe':self.Textractor_forward_extension_switch}
 

        self.resetsourcesignal.connect(functools.partial(resetsource,self))   
            

    
def settingtextractor(self ): 
         
        if globalconfig['sourcestatus']['textractor']==False:
            return 
         
        self.object.hookselectdialog.hide() 
        
        # self.a=gui.attachprocessdialog.AttachProcessDialog(self.object.translation_ui)
        # self.a.show()
        #ret=self.a.exec_()
        def callback(selectedp):
            
            #self.object.textsource=None
            pid,pexe,hwnd=(  selectedp)   
        
            arch=getarch(pid)
            if arch is None:
                return
            if   self.object.textsource:
                self.object.textsource.end()  
            
            self.object.hookselectdialog.changeprocessclearsignal.emit()
            if self.object.savetextractor:
                self.object.textsource=self.object.savetextractor
                self.object.textsource.reset(self.object,self.object.textgetmethod,self.object.hookselectdialog,pid,hwnd,pexe )

            else:
                
                self.object.textsource=textractor(self.object,self.object.textgetmethod,self.object.hookselectdialog,pid,hwnd,pexe ) 
                
                self.object.savetextractor=self.object.textsource 
            settingsource(self)
        self.object.AttachProcessDialog.callback=callback
        self.object.AttachProcessDialog.show() 
         
def settingsource(self):
    if globalconfig['sourcestatus']['textractor']==False:
                return 
    #self.hide()
    self.object.hookselectdialog.show() 
    self.object.hookselectdialog.hiding=False
def resetsource(self):
        self.object.hookselectdialog.changeprocessclearsignal.emit()
        for k in self.sourceswitchs:
                if globalconfig['sourcestatus'][k]==True:
                    if k=='textractor':
                        if 'textsource' in dir(self.object) and  self.object.textsource and self.object.textsource.ending==False: 
                            self.object.textsource.end() 
                    self.sourceswitchs[k].setChecked(False) 
                    globalconfig['sourcestatus'][k]=False
def textsourcechange(self,who,checked):   
        if checked : 
            resetsource(self)
            globalconfig['sourcestatus'][who]=True
        else:
            globalconfig['sourcestatus'][who]=False  
            if 'textsource' in dir(self.object) and self.object.textsource:
                self.object.textsource.end() 
            
            if who=='ocr'   :
                self.object.translation_ui.showhidestate=True
                self.object.translation_ui.showhide()
                self.object.translation_ui.refreshtooliconsignal.emit()

        if checked : 
            self.object.starttextsource() 
        self.selectbutton.setEnabled(globalconfig['sourcestatus']['textractor']) 
        self.selecthookbutton.setEnabled(globalconfig['sourcestatus']['textractor'])
        if who=='textractor' and checked:
            settingtextractor(self )
        
        self.object.translation_ui.showhidetoolbuttons()
    # 翻译设定标签栏