import maya.cmds as cmds
import pymel.core as pmc
def checkNewMenuItem( item ):
    
    for k,v in dic.items():
        if(k==item):
            (code.menu()).clear()
            for i in v:              
                pmc.menuItem(parent=(code +'|OptionMenu'), label='{}'.format(i))

def scnFileOpen():
    chosenFile = cmds.fileDialog2(fm=1, ds=0, cap="Open", ff=scnFilter ,okc="Select scene file", hfe=0)[0]
    cmds.textField('myMayaScenePathField', edit=1, text=chosenFile)

dic={'qt':['H.264','H.263'],'avi':['none','MS-YUV']}
window = cmds.window( title="playblast", iconName='Short Name', widthHeight=(500, 500) )
cmds.columnLayout( adjustableColumn=True )
cmds.optionMenuGrp(label='choose camera',columnAlign= (1,'left'))
allcameras = cmds.ls(type='camera') or []
exclude = ['topShape', 'sideShape', 'frontShape', 'perspShape']
cameras = list(set(allcameras)-set(exclude))
for camaras in cameras:
    cmds.menuItem( label='{}'.format(camaras) )
    

fm=cmds.optionMenuGrp(label='Format',columnAlign= (1,'left'),changeCommand=checkNewMenuItem)
for k,v in dic.items():
    pmc.menuItem( label='{}'.format(k) )
code=pmc.optionMenuGrp(label='code',columnAlign= (1,'left'))
for i in dic.get('qt'):
    a=pmc.menuItem( parent=(code +'|OptionMenu'),label='{}'.format(i) )
cmds.intFieldGrp( numberOfFields=2, label='framerange', value1=0, value2=120,columnAlign= (1,'left'))
cmds.intFieldGrp( numberOfFields=2, label='Size', value1=1920, value2=1080,columnAlign= (1,'left') ) 
cmds.intFieldGrp(numberOfFields=1,label='FrameRate', value1=24,columnAlign= (1,'left'))
cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 100), (2, 250)] )
cmds.text( label='Maya Scene' )
front = cmds.textField('myMayaScenePathField')
cmds.iconTextButton( style='iconAndTextCentered',command='scnFileOpen()', image1='fileOpen.xpm', height=18 )

#mel.eval('lookThroughModelPanel( "camera1" ,"modelPanel1");')
cmds.setParent( '..' )
cmds.showWindow( window )

