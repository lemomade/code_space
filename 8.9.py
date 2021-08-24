
import maya.cmds as cmds
import pymel.core as pmc


cameraName = cmds.camera()
cameraShape = cameraName[1]
pmc.spaceLocator(n=cameraName[0]+"_aim")
group=pmc.createNode( 'lookAt' ,n=cameraName[0]+"_group")
cmds.connectAttr(cameraName[0]+'.translate',cameraName[0]+'_group.constraintTranslate')
cmds.connectAttr(cameraName[0]+'.parentInverseMatrix[0]',cameraName[0]+'_group.constraintParentInverseMatrix')
cmds.connectAttr(cameraName[0]+'.rotatePivot',cameraName[0]+'_group.constraintRotatePivot')
cmds.connectAttr(cameraName[0]+'.rotatePivotTranslate',cameraName[0]+'_group.constraintRotateTranslate')
cmds.connectAttr(cameraName[0]+'_group.constraintRotate',cameraName[0]+'.rotate')
cmds.connectAttr(cameraName[0]+'_group.distanceBetween',cameraName[1]+'.centerOfInterest')
cmds.connectAttr(cameraName[0]+'_aim.translate',cameraName[0]+'_group.target[0].targetTranslate')
cmds.connectAttr(cameraName[0]+'_aim.translate.translateX ',cameraName[0]+'_group.target[0].targetTranslateX')
cmds.connectAttr(cameraName[0]+'_aim.translate.translateY ',cameraName[0]+'_group.target[0].targetTranslateY')
cmds.connectAttr(cameraName[0]+'_aim.translate.translateZ ',cameraName[0]+'_group.target[0].targetTranslateZ')
cmds.connectAttr(cameraName[0]+'_aim.parentMatrix[0]',cameraName[0]+'_group.target[0].targetParentMatrix')
cmds.connectAttr(cameraName[0]+'_aim.rotatePivot',cameraName[0]+'_group.target[0].targetRotatePivot')
cmds.connectAttr(cameraName[0]+'_aim.rotatePivotTranslate',cameraName[0]+'_group.target[0].targetRotateTranslate')

cmds.parent( cameraName[0], cameraName[0]+'_group', relative=True )
cmds.parent( cameraName[0]+'_aim', cameraName[0]+'_group', relative=True )

