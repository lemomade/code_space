import pymel.core as pmc


for i in pmc.ls(sl=1,fl=1):
    a = pmc.pointPosition(i.name(), w=1)
    b, c = pmc.polyCube()
    b.setTranslation(a)

