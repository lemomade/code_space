from PySide2.QtWidgets import *
from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import *
from PySide2.QtCore import Slot, Qt
import MASH.api as mapi
import maya.cmds as cmds
import pymel.core as pmc
import maya.OpenMaya as om
import maya.OpenMayaFX as omfx

import maya.cmds as mc
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaFX as omfx
import gc
class Generate():
    def __init__(self):
        self.sl =cmds.ls(sl=1,fl=1)
        mashNetwork= mapi.Network()
        mashNetwork.createNetwork(name='Random_building',distributionStyle=1,geometry='instancer')
        distribute_name=mashNetwork.distribute
        mashNetwork.addNode("MASH_Replicator")
        if 'Random_building_ID' not in mashNetwork.getAllNodesInNetwork():
            mashNetwork.addNode("MASH_ID")
        pmc.connectAttr('Random_building_Distribute.outputPoints', 'Random_building_Replicator.inputPoints', f=True)
        pmc.connectAttr('Random_building_Replicator.outputPoints', 'Random_building_ID.inputPoints', f=True)
        pmc.connectAttr('Random_building_ID.outputPoints', 'Random_building.inputPoints', f=True)
        mashNetwork.setPointCount(5)
        cmds.setAttr("Random_building_ID.numObjects",len(self.sl))
        cmds.setAttr("Random_building_Distribute.amplitudeY",4)
        cmds.setAttr("Random_building_ID.idtype",2)
        cmds.setAttr("Random_building_Replicator.replicants",5)
        cmds.setAttr("Random_building_Replicator.offsetPositionZ",-5)

        
        
@Slot() #slot decorator
class RandomcityUI(QWidget):
    def __init__(self):
        super(RandomcityUI, self).__init__()
        self.initUI()
    def sliderheightValue(self,val):
        cmds.setAttr("Random_building_Distribute.amplitudeY",val)
        self.HSvalue.setText(str(val))
        return val
    def sliderrandomValue(self, val):
         cmds.setAttr("Random_building_ID.seed",val)
         self.RSvalue.setText(str(val))
         return val
    def NumberValue(self, val):
        cmds.setAttr("Random_building_Distribute.pointCount",val)
        self.NPvalue.setText(str(val))
        return val
    def sliderGXValue(self, val):
        cmds.setAttr("Random_city_Distribute.gridAmplitudeX",val)
        self.GXvalue.setText(str(val))
        return val
    def sliderGZValue(self, val):
        cmds.setAttr("Random_city_Distribute.gridAmplitudeZ",val)
        self.GZvalue.setText(str(val))
        return val

    def sliderDXValue(self, val):
        cmds.setAttr("Random_city_Distribute.gridx",val)
        self.DXvalue.setText(str(val))
        return val
    def sliderDZValue(self, val):
        cmds.setAttr("Random_city_Distribute.gridz",val)
        self.DZvalue.setText(str(val))
        return val  

    def AccountValue(self, val):
        cmds.setAttr("Random_building_Replicator.replicants",val)
        self.ACvalue.setText(str(val))
        return val
            
    def initUI(self):
        self.resize(300,300)
        vlayout = QVBoxLayout()
        Heightslider =self.heightslider()
        Randomslider= self.randomseedslider()
        Numberslider= self.Nemberslider()
        Accountslider= self.accountValue()
        path = self.createFilePath()
        GXslider =self.citygridX_slider()
        GZslider =self.citygridZ_slider()
        DXslider =self.citydistanceX_slider()
        DZslider =self.citydistanceZ_slider()

        vlayout.addLayout(Numberslider)
        vlayout.addLayout(Accountslider)
        vlayout.addLayout(Heightslider)
        vlayout.addLayout(Randomslider)
        Generatebutton = QPushButton('generate')
        vlayout.addWidget(Generatebutton)
        Generatebutton.clicked.connect(Generate)
        Readybutton = QPushButton('good shape!')
        Readybutton.clicked.connect(ChangeintoInstancer)
        vlayout.addWidget(Readybutton)
        vlayout.addLayout(GXslider)
        vlayout.addLayout(GZslider)
        vlayout.addLayout(DXslider)
        vlayout.addLayout(DZslider)
        vlayout.addLayout(path)

        self.setLayout(vlayout)
        Ramdombutton = QPushButton('ramdom City')
        Ramdombutton.clicked.connect(self.mapgenerate)
        vlayout.addWidget(Ramdombutton)

    def mapgenerate(self):
        l =pmc.ls('Random_building_Instancer_objects')[0]
        pmc.select(l.listRelatives())
        mashCityNetwork= mapi.Network()
        mashCityNetwork.createNetwork(name='Random_city',distributionStyle=6)
        distribute_name=mashCityNetwork.distribute
        if 'Random_city_ID' not in mashCityNetwork.getAllNodesInNetwork():
            mashCityNetwork.addNode("MASH_ID")
        mashCityNetwork.setPointCount(30)
        ground=cmds.polyPlane(h=100,w=100)
        cmds.setAttr("Random_city_ID.numObjects",len(l.listRelatives()))
        cmds.setAttr("Random_city_ID.idtype",2)
    
        shader_name=pmc.shadingNode('blinn', n='Random_city_map', asShader=True)
        pmc.sets(renderable=True, nss=True, empty=True, name='testSG_Random_city_map')
        pmc.connectAttr('Random_city_map.outColor', 'testSG_Random_city_map.surfaceShader', f=True)
        pmc.select(ground)
        pmc.hyperShade(assign='Random_city_map')
        file_name= pmc.shadingNode('file', asTexture=1, icm=1, n='cityTexture') 
        file_name.setAttr('fileTextureName', self.fd)
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
        pmc.hide('Random_building_Instancer')
        pmc.refresh()       

    def heightslider(self):
        hbox = QHBoxLayout()
        Label = QLabel('height:')
        self.HSvalue=QLabel('')
        heightslider = QSlider(Qt.Horizontal)
        heightslider.valueChanged[int].connect(self.sliderheightValue ) # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.HSvalue)
        hbox.addWidget(heightslider)
        return hbox

    def citygridX_slider(self):
        hbox = QHBoxLayout()
        Label = QLabel('citygridX:')
        self.GXvalue=QLabel('')
        heightslider = QSlider(Qt.Horizontal)
        heightslider.valueChanged[int].connect(self.sliderGXValue ) # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.GXvalue)
        hbox.addWidget(heightslider)
        return hbox
    def citygridZ_slider(self):
        hbox = QHBoxLayout()
        Label = QLabel('citygridZ:')
        self.GZvalue=QLabel('')
        heightslider = QSlider(Qt.Horizontal)
        heightslider.valueChanged[int].connect(self.sliderGZValue ) # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.GZvalue)
        hbox.addWidget(heightslider)
        return hbox

    def citydistanceX_slider(self):
        hbox = QHBoxLayout()
        Label = QLabel('citydistanceX:')
        self.DXvalue=QLabel('')
        heightslider = QSlider(Qt.Horizontal)
        heightslider.valueChanged[int].connect(self.sliderDXValue ) # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.DXvalue)
        hbox.addWidget(heightslider)
        return hbox
    def citydistanceZ_slider(self):
        hbox = QHBoxLayout()
        Label = QLabel('citydistanceZ:')
        self. DZvalue=QLabel('')
        heightslider = QSlider(Qt.Horizontal)
        heightslider.valueChanged[int].connect(self.sliderDZValue ) # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.DZvalue)
        hbox.addWidget(heightslider)
        return hbox   

    def accountValue(self):
        hbox = QHBoxLayout()
        Label = QLabel('Account:')
        self.ACvalue = QLabel('')
        accountslider = QSlider(Qt.Horizontal)
        accountslider.valueChanged[int].connect(self.AccountValue)  # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.ACvalue)
        hbox.addWidget(accountslider)
        return hbox

    def randomseedslider(self):
        hbox = QHBoxLayout()
        Label = QLabel('Random Seed:')
        self.RSvalue=QLabel('')
        randomseedslider = QSlider(Qt.Horizontal)
        randomseedslider.valueChanged[int].connect(self.sliderrandomValue)  # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.RSvalue)
        hbox.addWidget(randomseedslider)
        return hbox

    def Nemberslider(self):
        hbox = QHBoxLayout()
        Label = QLabel('account floor:')
        self.NPvalue=QLabel('')
        Nemberslider = QSlider(Qt.Horizontal)
        Nemberslider.valueChanged[int].connect(self.NumberValue)  # valueChanged signal
        hbox.addWidget(Label)
        hbox.addWidget(self.NPvalue)
        hbox.addWidget( Nemberslider)
        return hbox
        
    def createFilePath(self):
        hbox = QHBoxLayout()
        Label = QLabel('File Path')
        self.linePathEdit = QLineEdit()
        button = QPushButton('find path')
        button.clicked.connect(self.clicks)
        hbox.addWidget(Label)
        hbox.addWidget(self.linePathEdit)
        hbox.addWidget(button)
        return hbox
        
    def clicks(self):
        self.fd = QFileDialog.getOpenFileName(self, "Open Image", ".", "Image Files(*.jpg *.png)")[0]
        self.linePathEdit.setText(self.fd)
        
class ChangeintoInstancer():
    def __init__(self):
        self.MASHbakeInstancer()
        self.groupbox()
        

    def mashGetMObjectFromName(self,nodeName):
        sel = om.MSelectionList()
        sel.add(nodeName)
        thisNode = om.MObject()
        sel.getDependNode( 0, thisNode )
        return thisNode
    def groupbox(self):
        l =pmc.ls('Random_building_Instancer_objects')[0]
        ao=cmds.getAttr('Random_building_Distribute.pointCount',time=12)
        sl=l.listRelatives()
        li=[]
        pmc.showHidden(sl)
        for i in sl:
            li.append(i)
            if len(li)>=ao:
                pmc.group(li)
                li=[]
                continue# 打个组

    #if animation is true, the playback range will be baked, otherwise just this frame will be.
    def MASHbakeInstancer(self):
        #get interface settings
        translateFlag = True
        rotationFlag = True
        scaleFlag = True    
        expressBaking = True
        flushUndo = False
        garbageCollect = True

        #get the selection
        li = []
        l =mc.ls('Random_building_Instancer')
        #check it's an instancer
        for n in l:
            li.append(n)

        #get the visibility array - which isn't provided by the MFnInstancer function set
        thisNode = self.mashGetMObjectFromName(n)
        fnThisNode = om.MFnDependencyNode(thisNode)
        inPointsAttribute = fnThisNode.attribute("inputPoints")
        inPointsPlug = om.MPlug( thisNode, inPointsAttribute )
        inPointsObj = inPointsPlug.asMObject()
        inputPPData = om.MFnArrayAttrsData(inPointsObj)

        #reused vars for the particles
        m = om.MMatrix()
        dp = om.MDagPath()
        dpa = om.MDagPathArray()
        sa = om.MScriptUtil()
        sa.createFromList([0.0, 0.0, 0.0], 3)
        sp = sa.asDoublePtr()

        #start frame, end frame, animaiton

        sf = cmds.currentTime( query=True )
        ef = sf+1

        #set the instancer object
        instObj = li[0];

        for i in range(int(sf), int(ef)):
            #set the time
            mc.currentTime(i)
            self.g=instObj+"_objects"

            #if this is the first frame, create a transform to store everything under
            if i == sf:
                if mc.objExists(self.g) == True: mc.delete(self.g)
                mc.createNode("transform", n=self.g)
                l.append(self.g)

            #get the instancer
            sl = om.MSelectionList()
            sl.add(instObj)
            sl.getDagPath(0, dp)
            #create mfninstancer function set
            fni = omfx.MFnInstancer(dp)
            #cycle through the particles
            for j in range(fni.particleCount()):

                #get the instancer object
                fni.instancesForParticle(j, dpa, m)
                for ki in range(dpa.length()):
                    #get the instancer object name
                    fullPathName = dpa[ki].partialPathName()
                    #support namespaces, refrences, crap names
                    nameSpaceRemoved = fullPathName.rsplit(':', 1)[-1]
                    pipesRemoved = nameSpaceRemoved.rsplit('|', 1)[-1]
                    n = pipesRemoved+"_"+instObj+"_"+str(j)
                    #if we haven't got a node with the new name, make one, give it a safe name (which we will continue to identify it by).
                    if mc.objExists(n) == False:
                        #duplicate the object
                        n2 = mc.duplicate(dpa[ki].fullPathName(), rr=True, un=True)[0]
                        #rename it to the safe name
                        n = mc.rename(n2, n)

                        #parent it to the transform we created above
                        if mc.listRelatives(n, p=True) != self.g:
                            try:
                                n = mc.parent(n,self.g)[0]
                            except:
                                pass


                    #empty transformMatrix for the particle
                    tm = om.MTransformationMatrix(m)
                    instancedPath = dpa[ki]
                    #get the matrix from the instancer
                    instancedPathMatrix = instancedPath.inclusiveMatrix()
                    finalMatrixForPath = instancedPathMatrix * m
                    finalPoint = om.MPoint.origin * finalMatrixForPath;

                    t = tm.getTranslation(om.MSpace.kWorld)
                    #set the translate
                    try:
                        mc.setAttr(n+".t", finalPoint.x, finalPoint.y, finalPoint.z)
                        if translateFlag :
                            mc.setKeyframe(n+".t")
                    except:
                        pass



                    #set the rotate
                    r = tm.eulerRotation().asVector()
                    try:
                        mc.setAttr(n+".r", r[0]*57.2957795, r[1]*57.2957795, r[2]*57.2957795)
                        if rotationFlag:
                            mc.setKeyframe(n+".r")
                    except:
                        pass

                    #set the scale
                    tm.getScale(sp, om.MSpace.kWorld)
                    if scaleFlag:
                        sx = om.MScriptUtil().getDoubleArrayItem(sp, 0)
                        sy = om.MScriptUtil().getDoubleArrayItem(sp, 1)
                        sz = om.MScriptUtil().getDoubleArrayItem(sp, 2)
                        s = om.MTransformationMatrix(dpa[ki].inclusiveMatrix()).getScale(sp, om.MSpace.kWorld)
                        sx2 = om.MScriptUtil().getDoubleArrayItem(sp, 0)
                        sy2 = om.MScriptUtil().getDoubleArrayItem(sp, 1)
                        sz2 = om.MScriptUtil().getDoubleArrayItem(sp, 2)
                        try:
                            mc.setAttr(n+".s", sx*sx2, sy*sy2, sz*sz2)
                        except:
                            pass

            #flush undo
            if flushUndo:
                cmds.flushUndo()
            #python garbage collect
            if garbageCollect:
                gc.collect()
if __name__ == '__main__':

    twin = RandomcityUI()
    twin.show()


