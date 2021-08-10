import maya.cmds as cmds
import pymel.core as pmc
import maya.mel as mel
def playBlast(item):
    mel.eval('lookThroughModelPanel( "{}" ,"modelPanel1");'.format(dicsave['camera']))
    pmc.playblast(  f=dicsave['f'], st=dicsave['st'],et=dicsave['et'], fmt=dicsave['fmt'],h=dicsave['h'],w=dicsave['w'],framePadding=4,compression=dicsave['co'], quality=100,clearCache=True,forceOverwrite = True)

def checkNewMenuItem( item ):
    global code
    for k,v in dic.items():
        if(k==item):
            (code.menu()).clear()
            for i in v:              
                pmc.menuItem(parent=(code +'|OptionMenu'), label='{}'.format(i))
    dicsave['fmt']=item
def showdic(*args):
    print dicsave
def setdic(item):
    dicsave['camera']=item
def setcode(item):
    dicsave['co']=item
def printMenu(self,arg=None):
    global a
    global b
    global c
    st = cmds.intFieldGrp(a, query=True, value1=True)
    et = cmds.intFieldGrp(a, query=True, value2=True)  
    h = cmds.intFieldGrp(b, query=True, value1=True) 
    w = cmds.intFieldGrp(b, query=True, value2=True)
    fr = cmds.intFieldGrp(c, query=True, value1=True)
    dicsave['st']=st
    dicsave['et']=et
    dicsave['h']=h
    dicsave['w']=w
    dicsave['fr']=fr
def scnFileOpen():
    if( dicsave['fmt']=='qt'):
        chosenFile = cmds.fileDialog2( fileFilter='mov',fm=0, dialogStyle=2)[0]
    elif( dicsave['fmt']=='avi'):
        chosenFile = cmds.fileDialog2( fileFilter='avi',fm=0, dialogStyle=2)[0]
    dicsave['f']=chosenFile
    print dicsave
    cmds.textField('myMayaScenePathField', edit=1, text=chosenFile)

def createWindow():
    window = cmds.window( title="playblast", iconName='Short Name', widthHeight=(500, 500) )
    cmds.columnLayout( adjustableColumn=True ,rowSpacing=10)
    cmds.setParent( '..' )
    cmds.showWindow( window )

def createCameraOp():
    cmds.optionMenuGrp(label='choose camera',columnAlign= (1,'left'),changeCommand=setdic)
    allcameras = cmds.ls(type='camera') or []
    cameras_tr = cmds.listRelatives(allcameras, parent=True)
    exclude = ['top', 'side', 'front', 'persp']
    cameras = list(set(cameras_tr)-set(exclude))
   
    if(default_camera not in cameras):
        mel.eval('error "默认摄像机不存在，请改名字"')
    else :
        cameras.remove(default_camera)
        cameras_a=[default_camera]
        camerasa=cameras_a.extend(cameras)
    for camaras in cameras_a:
        cmds.menuItem( label='{}'.format(camaras))


def createformatAndCodeOp():
    global code    
    fm=cmds.optionMenuGrp(label='Format',columnAlign= (1,'left'),changeCommand=checkNewMenuItem)
    for k,v in dic.items():
        pmc.menuItem( label='{}'.format(k) )
    code=pmc.optionMenuGrp(label='code',columnAlign= (1,'left'),changeCommand=setcode)
    for i in dic.get('qt'):
        a=pmc.menuItem( parent=(code +'|OptionMenu'),label='{}'.format(i) )

def createSavePath():
    cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)] ,rowSpacing=(1, 20))
    cmds.text( label='Maya Scene' )
    front = cmds.textField('myMayaScenePathField')
    cmds.iconTextButton( style='iconAndTextVertical',align='right',command='scnFileOpen()', image1='fileOpen.xpm', height=8 )
def int_field():
    global a
    global b
    global c
    a=cmds.intFieldGrp( numberOfFields=2, label='framerange', value1=0, value2=120,columnAlign= (1,'left'),changeCommand=printMenu) 
    b=cmds.intFieldGrp( numberOfFields=2, label='Size', value1=1080, value2=1920,columnAlign= (1,'left'),changeCommand=printMenu ,extraLabel = 'height/width') 
    c=cmds.intFieldGrp(numberOfFields=1,label='FrameRate', value1=24,columnAlign= (1,'left'),changeCommand=printMenu)
def main():
    createWindow()
    createCameraOp()
    createformatAndCodeOp() 
    int_field()
    createSavePath()
    cmds.text( label='' )
    cmds.button( label='Play Blast!', command=playBlast,height=35)



if __name__ == '__main__':
    default_camera='camera3'
    dic={'qt':['H.264','H.263'],'avi':['none','MS-YUV','MS-RLE']}
    dicsave={'f':" ",'st':0,'et':120,'fmt':"qt",'fr':24,'h':1080,'w':1920,'co':"H.264",'camera':default_camera}
    main()


