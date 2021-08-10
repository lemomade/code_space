pmc.importFile(r'C:\Users\lwz\Desktop\pSphereShape1_model.ma')
pmc.importFile(r'C:\Users\lwz\Desktop\pSphereShape1_net.ma')
model=pmc.ls(type='mesh')
for i in model:
    tName=i.getTransform()
    sg_node = pmc.sets(renderable=True, name='{}'.format(tName)+'_SG')
    pmc.connectAttr('{}_shader.outColor'.format(tName), '{}_SG.surfaceShader'.format(tName), f=True)
for i in model:
    tName=i.getTransform()
    pmc.select(tName)
    pmc.hyperShade(assign='{}_shader'.format(tName))#auto connect shader and object


pmc.importFile(r'C:\Users\lwz\Desktop\pSphereShape1_model.ma',r'C:\Users\lwz\Desktop\pSphereShape1_model.ma')

pmc.file(save=True,force=True,'type'='mayaAscii')



pmc.importFile(r'C:\Users\lwz\Desktop\pSphereShape1_model.ma',r'C:\Users\lwz\Desktop\pSphereShape1_model.ma')
cmds.file(rename='test1')
cmds.file(save=True,type='mayaAscii')
pmc.file(save=True,force=True,type='mayaAscii')
# autosave and import 
