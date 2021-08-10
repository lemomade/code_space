import pymel.core as pmc
import maya.mel as mel

def output_net(model):
	shader=find_shader(model)
	##mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "exportSelectedNetwork");')
	pmc.exportSelected("C:/Users/lwz/Desktop/{}_net.ma".format(model[0]),type= "mayaAscii",options ="v=0;" ,pr=True,es=True,eur=True)


def output_model(model):
	pmc.select(model)
	pmc.hyperShade(assign='lambert1') 
	pmc.exportSelected("C:/Users/lwz/Desktop/{}_model.ma".format(model[0]),type= "mayaAscii",force=True,options ="v=0;" ,pr=True)

def find_shader(model):
	pmc.select(model)
	pmc.hyperShade(shaderNetworksSelectMaterialNodes=True)
	for shd in pmc.selected(materials=True):
		if [c for c in shd.classification() if 'shader/surface' in c]:
			return shd

def main():
	# model=pmc.ls(sl=1,fl=1)[0]
	model=pmc.ls(type='mesh')
	output_net(model)
	output_model(model)

def clearUnusedNode():
	mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
	

if __name__ == '__main__':
	main()

