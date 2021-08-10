import os
import pymel.core as pmc


UV_FILE_CONNECT = {'coverage':'coverage',
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


def create_mesh(mesh_name, index):
    trans_node, shape_node = pmc.polyCube(name=mesh_name)
    trans_node.setTranslation([0, 0, index])
    return trans_node


def create_node(shade_type, shade_name):
    node_list = None
    if shade_type == 'texture':
        file_node = pmc.shadingNode('file', asTexture=1, icm=1, n=shade_name) 
        uv_node = pmc.shadingNode('place2dTexture', asUtility=1)
        node_list = [file_node, uv_node]
    elif shade_type == 'shader':
        shade_node = pmc.shadingNode('lambert', n=shade_name+'_shader', asShader=True)
        sg_node = pmc.sets(renderable=True, name=shade_name+'_SG')
        node_list = [shade_node, sg_node]
    return node_list


def connect_node(node_a, node_b, con_type=None):
    if not con_type:
        pmc.connectAttr(node_a, node_b, f=True)
    if con_type == 'uv':
        for k, v in UV_FILE_CONNECT.items():
            pmc.connectAttr('{0}.{1}'.format(node_b, k), '{0}.{1}'.format(node_a, v), f=1)


def assign_shader(mesh_name, shade_name):
    pmc.select(mesh_name)
    pmc.hyperShade(assign=shade_name)


def main(account, texture_path):
    for i in range(1,account+1):
        mesh_trans = create_mesh('cube_{}'.format(i), i)
        shade_node = create_node('shader', 'test_{}'.format(i))
        connect_node(shade_node[0].name() + '.outColor', shade_node[1].name()+'.surfaceShader')
        assign_shader(mesh_trans, shade_node[0])
        texture_node = create_node('texture', 'test_{}_file'.format(i))
        thistexture_path = texture_path + "/{}.jpg".format(i)
        texture_node[0].setAttr('fileTextureName', thistexture_path)
        connect_node(texture_node[0].name(), texture_node[1].name(), con_type='uv')
        connect_node(texture_node[0]+'.outColor', shade_node[0]+'.color')


if __name__ == '__main__':
    texture_path = r"C:/Users/lwz/Desktop"
    main(5, texture_path)

##find select object shader name
pmc.hyperShade(shaderNetworksSelectMaterialNodes=True)
for shd in pmc.selected(materials=True):
    if [c for c in shd.classification() if 'shader/surface' in c]:
        print shd