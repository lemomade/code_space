import pymel.core as pmc


pmc.shadingNode('blinn', n='test_shading', asShader=True)
pmc.sets(renderable=True, nss=True, empty=True, name='testSG')
pmc.connectAttr('test_shading.outColor', 'testSG.surfaceShader', f=True)
pmc.hyperShade(assign=myBlinn)
pmc.hyperShade(assign='test_shading')


a = pmc.shadingNode('file', asTexture=1, icm=1, n='test_texture')

a.name()

a.setAttr('fileTextureName', r"C:/Users/Parzival/Desktop/a1.jpg")

b = pmc.shadingNode('place2dTexture', asUtility=1)

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
    pmc.connectAttr('{0}.{1}'.format(b.name(), k), '{0}.{1}'.format(a.name(), v), f=1)



