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
SUFFIX = '.srt'
def run(xml_file,replace_text):
    load_xml(xml_file)

    # - Test
    # split_range = split_marker_info()
    # video_items, graphic_item = get_items()
    # video_info = video_items_info()
    # print(video_info)
    out_put_file=six(xml_file, replace_text)
    return out_put_file

def load_xml(xml_file):
    global WORK_TREE
    global WORK_ROOT

    WORK_TREE = ElementTree.parse(xml_file)
    WORK_ROOT = WORK_TREE.getroot()




def six(xml_path, replace_text):
    video_info_lst = video_items_info_new()
    ii=0
    for session in video_info_lst:
        current_session = video_info_lst.index(session)
        for index, scence in enumerate(session):
            ii = ii + 1
            a=modify_text(current_session, index+1, replace_text, ii)
            session[index]['name']=a


    out_file_name = os.path.basename(xml_path).split(os.path.extsep)
    if len(out_file_name) > 2:
        out_file_name = [os.path.extsep.join(out_file_name[:-1]), out_file_name[-1]]
    out_file_name = out_file_name[0] + '_out'+ SUFFIX
    out_file_path = os.path.join(os.path.dirname(xml_path), out_file_name)

    ac = 0
    if os.path.exists(out_file_path):
        os.remove(out_file_path)
    for ii in video_info_lst:
        for i in ii:
            for k,v in i.items():
                name = i['name']
                start = i['start']
                end = i['end']
            ac=ac+1
            with open(out_file_path,'a') as new_file:
                time = seconds_to_frame(start,24)+" --> "+seconds_to_frame(end,24)
                new_file.write(str(ac)+"\n")
                new_file.write(time+"\n")
                new_file.write(name+"\n")
                new_file.write("\n")
                new_file.close()
    return out_file_path
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

def seconds_to_frame(in_frame,rate):
    in_frame= in_frame * 1.0000
    rate = rate * 1.0
    r = in_frame % rate
    seconds = in_frame / rate

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    r = r/rate*1000.0
    out_seconds="%02d:%02d:%02d,%03d" % (h, m, s, r)
    return out_seconds

def modify_text( session_index, scence_index,replace_text,ii):
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
    return new_text

def video_items_info_new():
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

