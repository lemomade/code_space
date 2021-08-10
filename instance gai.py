#MASHbakeInstancer
#This function takes an instancer, and turns all the particles being fed into it to real geometry.

import maya.cmds as mc
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaFX as omfx

import maya.cmds as mc
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaFX as omfx
import gc

def mashGetMObjectFromName(nodeName):
    sel = om.MSelectionList()
    sel.add(nodeName)
    thisNode = om.MObject()
    sel.getDependNode( 0, thisNode )
    return thisNode

#if animation is true, the playback range will be baked, otherwise just this frame will be.
def MASHbakeInstancer(animationFlag):
    #get interface settings
    translateFlag = True
    rotationFlag = True
    scaleFlag = True    
    expressBaking = True
    flushUndo = False
    garbageCollect = True
    if expressBaking:
        scriptEditorOpen = cmds.window ("scriptEditorPanel1Window", exists=True)
        if scriptEditorOpen:
            cmds.deleteUI ("scriptEditorPanel1Window",  window = True)

    #get the selection
    li = []
    l = mc.ls(sl=True) or []
    #check it's an instancer
    for n in l:
        if mc.nodeType(n) != "instancer": continue
        li.append(n)
    #did we find at least 1?
    if len(li) == 0: raise Exception('Select an instancer node.')
    l = []

    #get the visibility array - which isn't provided by the MFnInstancer function set
    thisNode = mashGetMObjectFromName(n)
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
    sf = int(mc.playbackOptions(q=True, min=True))-1
    ef = int(mc.playbackOptions(q=True, max=True))+2

    if (animationFlag==False):
        sf = cmds.currentTime( query=True )
        ef = sf+1

    #set the instancer object
    instObj = li[0];

    for i in range(int(sf), int(ef)):
        #set the time
        mc.currentTime(i)
        g = instObj+"_objects"

        #if this is the first frame, create a transform to store everything under
        if i == sf:
            if mc.objExists(g) == True: mc.delete(g)
            mc.createNode("transform", n=g)
            l.append(g)

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
                    if mc.listRelatives(n, p=True) != g:
                        try:
                            n = mc.parent(n, g)[0]
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
                    if translateFlag and animationFlag:
                        mc.setKeyframe(n+".t")
                except:
                    pass



                #set the rotate
                r = tm.eulerRotation().asVector()
                try:
                    mc.setAttr(n+".r", r[0]*57.2957795, r[1]*57.2957795, r[2]*57.2957795)
                    if rotationFlag and animationFlag:
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
                        if animationFlag:
                            mc.setKeyframe(n+".s")
                    except:
                        pass

        #flush undo
        if flushUndo:
            cmds.flushUndo()

        #python garbage collect
        if garbageCollect:
            gc.collect()


# ===========================================================================
# Copyright 2017 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
