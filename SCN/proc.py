import os
import json
import copy
import base64
from xml.etree import cElementTree as ElementTree

# - C:/parzival/OneDrive/workspace/huanma/py/temp_files/PR/CX_SC002.xml
WORK_TREE = ""
WORK_ROOT = ""
VIDEO_TRACK_INDEX = 1
GRAPHIC_TRACK_INDEX = 2
TEXT_TYPE_LST = [u"源文本", "Source Text", u"Source Text"]
NEW_GRAPHIC_ITEMS = []


def run(xml_file,replace_text):
    load_xml(xml_file)

    # - Test
    # split_range = split_marker_info()
    # video_items, graphic_item = get_items()
    # video_info = video_items_info()
    # print(video_info)
    out_put_file = six(xml_file,replace_text)
    return out_put_file


def load_xml(xml_file):
    global WORK_TREE
    global WORK_ROOT

    WORK_TREE = ElementTree.parse(xml_file)
    WORK_ROOT = WORK_TREE.getroot()


def get_items():
    work_tracks = WORK_ROOT.findall("./sequence/media/video/track")
    video_track = work_tracks[VIDEO_TRACK_INDEX - 1]
    video_items = video_track.findall('clipitem')
    graphic_track = work_tracks[GRAPHIC_TRACK_INDEX - 1]
    graphic_item = graphic_track.findall('clipitem')
    return video_items, graphic_item


def split_marker_info():
    session_marker_lst = WORK_ROOT.findall("./sequence/marker")
    split_end_lst = [int(i.find('in').text) for i in session_marker_lst]
    split_end_lst.sort()
    split_start_lst = split_end_lst[:-1]
    split_start_lst.insert(0, 0)
    split_range = zip(split_start_lst, split_end_lst)
    return list(split_range)


def video_items_info():
    split_range = split_marker_info()
    video_info_lst = [[] for i in split_range]
    clip_items, _ = get_items()
    for i in clip_items:
        v_name = i.find('name').text
        v_start = int(i.find('start').text)
        v_end = int(i.find('end').text)
        for k in split_range:
            scence_index = split_range.index(k)
            if (k[0] <= v_start < k[1]):
                video_info_lst[scence_index].append({'name': v_name,
                                                     'start': v_start,
                                                     'end': v_end})
    return video_info_lst


def decode_text(base64_text):
    original_text = base64.b64decode(base64_text)
    separater = b'\x00'
    prefix = original_text.split(separater + b'{' + separater)[0]
    text_ascii = original_text.replace(prefix, b'').replace(separater, b'')
    text_json = json.loads(text_ascii)
    return text_json


def modify_text(text_json, session_index, scence_index, scence_suffix,replace_text,ii):
    if '#' in replace_text:
        replace_split = replace_text.split('_')
        session_text = replace_split[-2]
        scence_text = replace_split[-1]
        session_index_len = session_text.count('#')
        scence_index_len = scence_text.count('#')
        flag_0 = "#" * session_index_len
        flag_1 = '%0{}d'.format(session_index_len) % session_index
        replace_split[-2] = session_text.replace(flag_0, flag_1)
        flag_0 = "#" * scence_index_len
        flag_1 = '%0{}d'.format(scence_index_len) % scence_index
        # - TODO: AB 镜号
        # if scence_suffix:
        #     flag_1 = flag_1 + scence_suffix
        replace_split[-1] = scence_text.replace(flag_0, flag_1)

    elif '*' in replace_text:
        replace_split = replace_text.split('_')
        session_text = replace_split[-2]
        scence_text = replace_split[-1]
        session_index_len = session_text.count('*')
        scence_index_len = scence_text.count('*')
        flag_0 = "*" * session_index_len
        flag_1 = '%0{}d'.format(session_index_len) % session_index
        # old_text[-2] = session_text.replace(flag_0, flag_1)
        replace_split[-2] = session_text.replace(flag_0, flag_1)
        flag_0 = "*" * scence_index_len
        flag_1 = '%0{}d'.format(scence_index_len)% ii
        # - TODO: AB 镜号
        # if scence_suffix:
        #     flag_1 = flag_1 + scence_suffix
        replace_split[-1] = scence_text.replace(flag_0, flag_1)
    new_text = "_".join(replace_split)
    text_json[u'mTextParam'][u'mStyleSheet'][u'mText'] = new_text



def seven(scence, index, clip_name_lst, current_session, session,replace_text,ii):
    current_scence = index + 1
    # - A / B scence
    clip_name = scence['name']
    # print(session)
    # - TODO: AB 镜号
    if clip_name not in clip_name_lst:
        scence['suffix'] = None
        # scence['index'] = current_scence
    else:
        same_clip_num = clip_name_lst.count(clip_name)
        scence['suffix'] = chr(64 + same_clip_num)
        # for i in session:
        #     print(i['name'])
        # current_scence = current_scence - 1
    clip_name_lst.append(clip_name)
    # - graphic time
    _, graphic_item = get_items()
    graphic_item = graphic_item[0]
    new_graphic = copy.deepcopy(graphic_item)
    new_graphic.find('start').text = str(scence['start'])
    new_graphic.find('end').text = str(scence['end'])

    for i in new_graphic.findall("./filter/effect/parameter"):
        if i.find('name').text in TEXT_TYPE_LST:
            graphic_text_item = i
    graphic_text = graphic_text_item.find('value').text
    graphic_text = decode_text(graphic_text)
    modify_text(graphic_text, current_session, current_scence, scence['suffix'],replace_text,ii)
    a = temp_test(graphic_text)

    for i in new_graphic.findall("./filter/effect/name"):
        i.text=graphic_text[u'mTextParam'][u'mStyleSheet'][u'mText']

    for i in new_graphic.findall("./name"):
        i.text=graphic_text[u'mTextParam'][u'mStyleSheet'][u'mText']
    # a = graphic_text[u'mTextParam'][u'mStyleSheet'][u'mText']
    graphic_text_item.find('value').text = a
    NEW_GRAPHIC_ITEMS.append(new_graphic)


def encode_text(text_info):
    text_json = json.dumps(text_info[0], separators=(',', ':'))
    text_json_bytes = text_info[1] + text_info[2] + text_info[2].join(text_json) + text_info[2]
    base64_text = base64.b64encode(text_json_bytes)
    return base64_text


def temp_test(temp_var):
    var_value = temp_var[u'mTextParam'][u'mStyleSheet'][u'mText']
    prefix = bytes([len(var_value) * 2 + 172])
    # test = '{}'.format(len(var_value) * 2 + 172)
    prefix = prefix + b'\x06' + b'\x00' * 5
    temp_space = '\x00'
    temp_tree = json.dumps(temp_var, separators=(',', ':'))
    tree_fin = temp_space + temp_space.join(temp_tree) + temp_space
    tree_fin = prefix + bytes(tree_fin, encoding='utf-8')
    tree_b64 = base64.b64encode(tree_fin)
    # print(str(tree_b64, encoding='utf-8'))

    return str(tree_b64, encoding='utf-8')


def six(xml_path,replace_text):
    work_tracks = WORK_ROOT.findall("./sequence/media/video/track")
    graphic_track = work_tracks[GRAPHIC_TRACK_INDEX - 1]
    graphic_item = graphic_track.findall('clipitem')

    video_info_lst = video_items_info()
    video_info_lst_new = video_items_info_new()
    # print(video_info_lst_new)
    ii=0
    for session in video_info_lst:
        current_session = video_info_lst.index(session) + 1
        clip_name_lst = []
        for index, scence in enumerate(session):
            ii=ii+1
            seven(scence, index, clip_name_lst, current_session, session,replace_text,ii)

    graphic_track.remove(graphic_item[0])
    for i in NEW_GRAPHIC_ITEMS:
        graphic_track.append(i)
    out_file_name = os.path.basename(xml_path).split(os.path.extsep)
    if len(out_file_name) > 2:
        out_file_name = [os.path.extsep.join(out_file_name[:-1]), out_file_name[-1]]
    out_file_name = out_file_name[0] + '_out.' + out_file_name[1]
    out_file_path = os.path.join(os.path.dirname(xml_path), out_file_name)
    WORK_TREE.write(out_file_path, encoding="utf-8", xml_declaration=True)
    return out_file_path


# - TODO: AB 镜号
def video_items_info_new():
    split_range = split_marker_info()

    # video_info_lst = [[] for i in split_range]
    # print(video_info_lst)
    video_info_lst = []
    clip_items, _ = get_items()
    for i in clip_items:
        v_name = i.find('name').text
        v_start = int(i.find('start').text)
        v_end = int(i.find('end').text)
        for index, session_range in enumerate(split_range):
            if (session_range[0] <= v_start < session_range[1]):
                video_info_lst.append({'name': v_name,
                                       'start': v_start,
                                       'end': v_end,
                                       'session': index + 1})
            # scence_index = split_range.index(k)
            # if (k[0] <= v_start < k[1]):

    return video_info_lst


if __name__ == '__main__':
    run(r'W:\TD\TEST_FILE\PR\CX_SC002.xml')