import pymel.core as pmc
account =5
for i in range(1,account+1):
    pmc.polyCube(name='cube_{}'.format(i))
    pmc.setAttr('cube_{}.translateZ'.format(i), i*2 )
    c=pmc.shadingNode('lambert', n='test_shading_{}'.format(i), asShader=True)
    pmc.sets(renderable=True, name='testSG_{}'.format(i))
    pmc.connectAttr('test_shading_{}.outColor'.format(i),'testSG_{}.surfaceShader'.format(i),f=True)
    
    pmc.select( 'cube_{}'.format(i) )
    pmc.hyperShade(assign='test_shading_{}'.format(i)) 

    a = pmc.shadingNode('file', asTexture=1, icm=1, n='test_texture_{}'.format(i)) 
    a.setAttr('fileTextureName', r"C:/Users/lwz/Desktop/{}.jpg".format(i))
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
    pmc.connectAttr('{0}.outColor'.format(a.name()), '{0}.color'.format(c.name()), f=1)



