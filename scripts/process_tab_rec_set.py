import json
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def read_tab_rec_set_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    return json_data

def find_min_max_xy(points):
    xs, ys = [], []
    for point in points:
        xs.append(point[0])
        ys.append(point[1])
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return min_x, max_x, min_y, max_y

def ori_json_data_process(json_data):
    processed_data ={}
    if len(json_data) == 0:
        return processed_data
    processed_data['version'] = json_data['version']
    processed_data['img_path'] = json_data['imagePath']
    processed_data['img_height'] = json_data['imageHeight']
    processed_data['img_width'] = json_data['imageWidth']
    table_item = json_data['shapes']
    tables = []
    for sub_table in table_item:
        sub_tab_info = {}
        min_x, max_x, min_y, max_y = find_min_max_xy(sub_table['points'])
        sub_tab_info['label'] = sub_table['label']
        sub_tab_info['minx'] = min_x
        sub_tab_info['miny'] = min_y
        sub_tab_info['maxx'] = max_x
        sub_tab_info['maxy'] = max_y
    processed_data['tables'] = tables

    return processed_data

def json_to_xml(json_data):
    # 创建根元素
    root = ET.Element("annotation")
    
    # 添加基本信息
    ET.SubElement(root, "folder")
    ET.SubElement(root, "filename").text = json_data["img_path"]
    ET.SubElement(root, "path").text = json_data["img_path"]
    
    # 添加源信息
    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "TableRecSec-Detection"
    
    # 添加大小信息
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(json_data["img_width"])
    ET.SubElement(size, "height").text = str(json_data["img_height"])
    ET.SubElement(size, "depth").text = "3"
    
    ET.SubElement(root, "segmented").text = "0"
    
    # 添加对象信息
    for table in json_data["tables"]:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = "table"
        ET.SubElement(obj, "pose").text = "Frontal"
        ET.SubElement(obj, "truncated").text = "0"
        ET.SubElement(obj, "difficult").text = "0"
        ET.SubElement(obj, "occluded").text = "0"
        
        bndbox = ET.SubElement(obj, "bndbox")
        xmin = table['minx']
        ymin = table['miny']
        xmax = table['maxx']
        ymax = table['maxy']
        
        ET.SubElement(bndbox, "xmin").text = f"{xmin:.2f}"
        ET.SubElement(bndbox, "ymin").text = f"{ymin:.2f}"
        ET.SubElement(bndbox, "xmax").text = f"{xmax:.2f}"
        ET.SubElement(bndbox, "ymax").text = f"{ymax:.2f}"
    
    # 将 ET 对象转换为字符串并格式化
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="    ")
    
    return pretty_xml_str

def save_xml(xml_output, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(xml_output)

def main():
    root_path = 'datasets/TabRecSet/TD_annotation'  # chose your root
    save_root = 'datasets/TabRecSet/TD_annotation_xml' # chose your root
    for root, dirs, files in os.walk(root_path):
        if len(files) != 0:
            for f in files:
                json_path = os.path.join(root, f)
                json_data = read_tab_rec_set_json(json_path)
                processed_data = ori_json_data_process(json_data)
                pretty_xml = json_to_xml(processed_data)
                save_path = os.path.join(save_root, f.repalce('.json','.xml'))
                save_xml(pretty_xml, save_path)

if __name__ == "__main__":
    main()