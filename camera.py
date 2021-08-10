import maya.cmds as cmds
import pymel.core as pmc
class MayaClass(object):
	def main(self):
		cameraName = cmds.camera()
		cameraShape = cameraName[1]
		cn=cameraName[0]
		aim=cmds.spaceLocator(n=cn+"_aim")[0]
		group=cmds.createNode( 'lookAt' ,n=cn+"_group")
		cmds.setAttr(aim +".translateZ",-5)
		cmds.setAttr(aim +".rotateY",0)
		cmds.parent( cn, group, relative=True )
		cmds.parent( aim, group, relative=True )

		CONNECT_INDEXS={ cn+'.translate':group+'.translate',
						cn+'.parentInverseMatrix[0]':group+'.constraintParentInverseMatrix',
						cn+'.rotatePivot':group+'.constraintRotatePivot',
						cn+'.rotatePivotTranslate':group+'.constraintRotateTranslate',
						group+'.distanceBetween':cameraShape+'.centerOfInterest',
						group+'.constraintRotateX':cn+'.rotateX',
						group+'.distanceBetween':cn+'.rotateY',
						group+'.distanceBetween':cn+'.rotateZ',
						aim+'.translate':group+'.target[0].targetTranslate',
						aim+'.translate.translateX':group+'.target[0].targetTranslateX',
						aim+'.translate.translateY':group+'.target[0].targetTranslateY',
						aim+'.translate.translateZ':group+'.target[0].targetTranslateZ',
						aim+'.parentMatrix[0]':group+'.target[0].targetParentMatrix',
						aim+'.rotatePivot':group+'.target[0].targetRotatePivot',
						aim+'.rotatePivotTranslate':group+'.target[0].targetRotateTranslate',
						}

		for k, v in CONNECT_INDEXS.items():
			cmds.connectAttr('{}'.format(k),'{}'.format(v),f=1)

		# cmds.connectAttr(cn+'.translate',group+'.translate')
		cmds.setAttr(group+'.constraintRotateY',0)
		cmds.setAttr(group+'.aimVectorX',0)
		cmds.setAttr(group+'.aimVectorZ',-1)
		cmds.setAttr(cn+'_aimShape.visibility',0)
		cmds.setAttr(cn+'_aim.displayRotatePivot',1)

		cmds.addAttr(cn,longName='overscan',at='double',min=0.0,max=1.0,dv=1)
		cmds.setAttr(cn+'.overscan',e=1,keyable=1)
		cmds.connectAttr(cn+'.overscan',cameraShape+'.overscan')

		cmds.addAttr(cn,longName='RenderWidth',at='long',min=0,max=4096,dv=1920)
		cmds.setAttr(cn+'.Render Width',e=1,keyable=1)
		cmds.connectAttr(cn+'.Render Width','defaultResolution.width')
		cmds.addAttr(cn,longName='RenderHeight',at='long',min=0,max=2160,dv=1080)
		cmds.setAttr(cn+'.Render Height',e=1,keyable=1)
		cmds.connectAttr(cn+'.Render Height','defaultResolution.height')



