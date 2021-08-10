import maya.cmds as cmds
import pymel.core as pmc

cameraName = cmds.camera()
cameraShape = cameraName[1]
cn=cameraName[0]
pmc.spaceLocator(n=cn+"_aim")
group=pmc.createNode( 'lookAt' ,n=cn+"_group")
cmds.setAttr(cn+'_aim.translateZ',-5)
cmds.setAttr(cn+'_aim.rotateY',0)

cmds.parent( cn, cn+'_group', relative=True )
cmds.parent( cn+'_aim', cn+'_group', relative=True )

cmds.connectAttr(cn+'.translate',cn+'_group.constraintTranslate')
cmds.connectAttr(cn+'.parentInverseMatrix[0]',cn+'_group.constraintParentInverseMatrix')
cmds.connectAttr(cn+'.rotatePivot',cn+'_group.constraintRotatePivot')
cmds.connectAttr(cn+'.rotatePivotTranslate',cn+'_group.constraintRotateTranslate')

cmds.connectAttr(cn+'_group.distanceBetween',cameraName[1]+'.centerOfInterest')
cmds.connectAttr(cn+'_aim.translate',cn+'_group.target[0].targetTranslate')
cmds.connectAttr(cn+'_aim.translate.translateX ',cn+'_group.target[0].targetTranslateX')
cmds.connectAttr(cn+'_aim.translate.translateY ',cn+'_group.target[0].targetTranslateY')
cmds.connectAttr(cn+'_aim.translate.translateZ ',cn+'_group.target[0].targetTranslateZ')

cmds.connectAttr(cn+'_group.constraintRotateX ',cn+'.rotateX')
cmds.connectAttr(cn+'_group.constraintRotateY ',cn+'.rotateY')
cmds.connectAttr(cn+'_group.constraintRotateZ ',cn+'.rotateZ')

cmds.connectAttr(cn+'_aim.parentMatrix[0]',cn+'_group.target[0].targetParentMatrix')
cmds.connectAttr(cn+'_aim.rotatePivot',cn+'_group.target[0].targetRotatePivot')
cmds.connectAttr(cn+'_aim.rotatePivotTranslate',cn+'_group.target[0].targetRotateTranslate')
cmds.setAttr(cn+'_group.constraintRotateY',0)

cmds.setAttr(cn+'_group.aimVectorX',0)
cmds.setAttr(cn+'_group.aimVectorZ',-1)
cmds.setAttr(cn+'_aimShape.visibility',0)
cmds.setAttr(cn+'_aim.displayRotatePivot',1)


cmds.addAttr(cn,longName='overscan',at='double',min=0.0,max=1.0,dv=1)
cmds.setAttr(cn+'.overscan',e=1,keyable=1)
cmds.connectAttr(cn+'.overscan',cameraName[1]+'.overscan')

cmds.addAttr(cn,longName='RenderWidth',at='long',min=0,max=4096,dv=1920)
cmds.setAttr(cn+'.Render Width',e=1,keyable=1)
cmds.connectAttr(cn+'.Render Width','defaultResolution.width')
cmds.addAttr(cn,longName='RenderHeight',at='long',min=0,max=2160,dv=1080)
cmds.setAttr(cn+'.Render Height',e=1,keyable=1)
cmds.connectAttr(cn+'.Render Height','defaultResolution.height')
