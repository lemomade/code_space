import MASH.api as mapi
import maya.cmds as cmds

sphereToDistributeOn = cmds.polySphere(r=12)
cmds.polyCube()

# create a new MASH network
mashNetwork = mapi.Network()
mashNetwork.createNetwork(name="HelloWorld")
# print out the default node names
print (mashNetwork.waiter)
print (mashNetwork.distribute)
print (mashNetwork.instancer)
# add a Signal node
node = mashNetwork.addNode("MASH_Signal")
# set the signal node to have some scale noise
cmds.setAttr(node.name+".scaleX", 10)
# print out the name of the signal node
print (node.name)
# add a Falloff to the Signal node
falloff = node.addFalloff()
# move the falloff
falloffParent = cmds.listRelatives(falloff, p=True)[0]
cmds.setAttr(falloffParent+".translateX", 8)
# make it so the network distributes onto the surface of a mesh
mashNetwork.meshDistribute(sphereToDistributeOn[0])
# set the point count of the network
mashNetwork.setPointCount(1000)
# print all the nodes in the network
nodes = mashNetwork.getAllNodesInNetwork()
print ("All nodes in network: ")
print (nodes)
# find all the falloffs in the network
for node in nodes:    
    mashNode = mapi.Node(node)
    falloffs = mashNode.getFalloffs()
    if falloffs:
        print( node+" has the following falloffs: " + str(falloffs))



import MASH.api as mapi
import maya.cmds as cmds
import pymel.core as pmc
sl =cmds.ls(sl=1,fl=1)

mashNetwork= mapi.Network()
mashNetwork.createNetwork(name='Random_city',distributionStyle=6)
distribute_name=mashNetwork.distribute
if 'Random_city_ID' not in mashNetwork.getAllNodesInNetwork():
    mashNetwork.addNode("MASH_ID")
mashNetwork.setPointCount(30)
ground=cmds.polyPlane(h=20,w=20)
cmds.setAttr("Random_city_ID.numObjects",len(sl))


shader_name=pmc.shadingNode('blinn', n='Random_city_map', asShader=True)
pmc.sets(renderable=True, nss=True, empty=True, name='testSG_Random_city_map')
pmc.connectAttr('Random_city_map.outColor', 'testSG_Random_city_map.surfaceShader', f=True)
pmc.select(ground)
pmc.hyperShade(assign='Random_city_map')
file_name= pmc.shadingNode('file', asTexture=1, icm=1, n='cityTexture') 
file_name.setAttr('fileTextureName', r"C:/Users/lwz/Desktop/do.png")
place2dTexture_name = pmc.shadingNode('place2dTexture', asUtility=1)
connect_attr_dict = {'coverage':'coverage',
                         'translateFrame':'translateFrame',
                         'rotateFrame':'rotateFrame',
                         'mirrorU':'mirrorU',
                         'mirrorV':'mirrorV',
                         'stagger':'stagger',
                         'wrapU':'wrapU',
                         'wrapV':'wrapV',
                         'repeatUV':'repeatUV',
                         'offset':'offset',
                         'rotateUV':'rotateUV',
                         'noiseUV':'noiseUV',
                         'vertexUvOne':'vertexUvOne',
                         'vertexUvTwo':'vertexUvTwo',
                         'vertexUvThree':'vertexUvThree',
                         'vertexCameraOne':'vertexCameraOne',
                         'outUV':'uv',
                         'outUvFilterSize':'uvFilterSize'}
for k, v in connect_attr_dict.items():
     pmc.connectAttr('{0}.{1}'.format(place2dTexture_name.name(), k), '{0}.{1}'.format(file_name.name(), v), f=1)
pmc.connectAttr('{0}.outColor'.format(file_name.name()), '{0}.color'.format(shader_name.name()), f=1)
pmc.connectAttr('cityTexture.outColor', '{}.mColour'.format(distribute_name), f=True)   
pmc.connectAttr('{}.worldMatrix'.format(ground[0]), '{}.inMapMatrix'.format(distribute_name), f=True)   
cmds.setAttr("{}.mapDirection".format(distribute_name),1)
pmc.refresh()
