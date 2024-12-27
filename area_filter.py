import os
import switch.etree.ElementTree as ET
from pathlib import Path

# 定义图片标准尺寸
IMG_SIZE_STD = 4624 * 3468

# 将原始像素阈值转换为比例阈值
CLASS_AREA_THRESHOLDS = {
    "shoes": 30000 / IMG_SIZE_STD,
    "bin": 50000 / IMG_SIZE_STD,
    "pedestal": 25000 / IMG_SIZE_STD,
    "wire": 35000 / IMG_SIZE_STD,
    "socket": 35000 / IMG_SIZE_STD,
    "cat": 10000 / IMG_SIZE_STD,
    "dog": 10000 / IMG_SIZE_STD,
    "desk_rect": 85000 / IMG_SIZE_STD,
    "desk_circle": 85000 / IMG_SIZE_STD,
    "weighing-scale": 20000 / IMG_SIZE_STD,
    "key": 20000 / IMG_SIZE_STD,
    "person": 75040 / IMG_SIZE_STD,
    "chair": 55000 / IMG_SIZE_STD,
    "couch": 66000 / IMG_SIZE_STD,
    "bed": 75000 / IMG_SIZE_STD,
    "tvCabinet": 70000 / IMG_SIZE_STD,
    "fridge": 120000 / IMG_SIZE_STD,
    "television": 55000 / IMG_SIZE_STD,
    "washingMachine": 55000 / IMG_SIZE_STD,
    "electricFan": 55000 / IMG_SIZE_STD,
    "remoteControl": 35000 / IMG_SIZE_STD,
    "shoeCabinet": 55000 / IMG_SIZE_STD
}


def calculate_area(bndbox):
    try:
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        width = xmax - xmin
        height = ymax - ymin
        if width < 0 or height < 0:
            print(f"警告: 负面积检测框，xmin: {xmin}, ymin: {ymin}, xmax: {xmax}, ymax: {ymax}")
            return 0
        return width * height
    except Exception as e:
        print(f"错误计算面积: {e}")
        return 0


def get_image_size(root):
    size = root.find("size")
    if size is not None:
        width = int(size.find("width").text)
        height = int(size.find("height").text)
        return width * height
    else:
        # 获取文件名信息（如果在XML根节点中有的话）
        filename = root.find("filename")
        file_info = f", 文件: {filename.text}" if filename is not None else ""
        print(f"警告: XML文件中未找到size标签{file_info}，将使用标准尺寸 {IMG_SIZE_STD} ({4624}x{3468})")
        return IMG_SIZE_STD  # 如果XML中没有size信息，使用标准尺寸

def filter_objects(root, class_thresholds):
    objects = root.findall("object")
    img_area = get_image_size(root)

    for obj in objects:
        name = obj.find("name").text
        if name in class_thresholds:
            bndbox = obj.find("bndbox")
            area = calculate_area(bndbox)
            area_ratio = area / img_area  # 计算物体占图片的面积比
            threshold_ratio = class_thresholds[name]  # 阈值已经是比例

            if area_ratio < threshold_ratio:
                root.remove(obj)
                print(f"删除对象: {name}, 面积比: {area_ratio:.6f} < 阈值比: {threshold_ratio:.6f}")


def process_xml_file(input_xml_path, output_xml_path, class_thresholds):
    try:
        tree = ET.parse(input_xml_path)
        root = tree.getroot()
        filter_objects(root, class_thresholds)
        tree.write(output_xml_path, encoding="utf-8", xml_declaration=True)
        print(f"处理完成: {input_xml_path} -> {output_xml_path}")
    except ET.ParseError as e:
        print(f"XML解析错误: {input_xml_path}, 错误: {e}")
    except Exception as e:
        print(f"处理文件时出错: {input_xml_path}, 错误: {e}")


def batch_process_xmls(input_dir, output_dir, class_thresholds):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    xml_files = list(input_path.glob("*.xml"))
    if not xml_files:
        print(f"在目录 {input_dir} 中未找到XML文件。")
        return

    for xml_file in xml_files:
        relative_path = xml_file.relative_to(input_path)
        output_file = output_path / relative_path
        process_xml_file(xml_file, output_file, class_thresholds)


if __name__ == "__main__":
    # 设置输入和输出目录
    INPUT_DIR = "/home/depth/20241204/xml/20241116-13311"  # 替换为您的XML文件所在的文件夹
    OUTPUT_DIR = "/home/depth/20241204/xml/20241116-13311"  # 替换为您希望保存处理后XML文件的文件夹

    # 开始批量处理
    batch_process_xmls(INPUT_DIR, OUTPUT_DIR, CLASS_AREA_THRESHOLDS)