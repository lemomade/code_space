import maya.cmds as cmds
import pymel.core as pmc

a, b = cmds.polyCube(w=1, h=1, d=1, sx=2, sy=2, sz=10)

a, b = pmc.polyCube(w=1, h=1, d=1, sx=2, sy=2, sz=10)
dir(a)

a.setTransformation()
a.listAttr()

'pCube6.translateX'

cmds.setAttr('pCube6.translateZ', 12 )
pmc.setAttr('pCube6.translateZ', -12 )

dir(a)
a.setAttr('translateZ', 12)

for i in range(10):
    a, b = pmc.polyCube(w=1, h=1, d=1)
    a.setAttr('translateZ', i)








        