import MASH.api as mapi
import maya.cmds as cmds
import pymel.core as pmc
sl =cmds.ls(sl=1,fl=1)
mashNetwork= mapi.Network()
mashNetwork.createNetwork(name='Random_building',distributionStyle=1,geometry='instancer')
distribute_name=mashNetwork.distribute
if 'Random_building_ID' not in mashNetwork.getAllNodesInNetwork():
    mashNetwork.addNode("MASH_ID")
mashNetwork.setPointCount(5)
cmds.setAttr("Random_building_ID.numObjects",len(sl))
cmds.setAttr("Random_building_Distribute.amplitudeY",4)
cmds.setAttr("Random_building_ID.idtype",2)


class generate():

    def __init__():
        super(ClassName, self).__init__()
        mashNetwork= mapi.Network()
        mashNetwork.createNetwork(name='Random_building',distributionStyle=1,geometry='instancer')
        distribute_name=mashNetwork.distribute
        mashNetwork.addNode("MASH_Replicator")
        if 'Random_building_ID' not in mashNetwork.getAllNodesInNetwork():
            mashNetwork.addNode("MASH_ID")
        mashNetwork.setPointCount(5)
        cmds.setAttr("Random_building_ID.numObjects",len(sl))
        cmds.setAttr("Random_building_Distribute.amplitudeY",4)
        cmds.setAttr("Random_building_ID.idtype",2)
