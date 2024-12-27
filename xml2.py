# coding=utf-8
import os
import json
from xml.etree import ElementTree as ET
from xml.dom import minidom
import os.path
import struct

# 标签映射字典
LABEL_MAPPING = {
    'shoes': ['shoes', 'socks'],  # 添加socks因为都是脚部穿着物
    'bin': ['trash_can'],  # 保持原样
    'pedestal': ['base'],  # 保持原样
    'wire': ['cable', 'Cable', 'charger', 'Electric'],  # 添加Electric因为也属于电线类设备
    'socket': ['plug_in_board'],  # 保持原样
    'cat': ['pet_cat', 'pet_unknown'],  # 保持原样
    'dog': ['pet_unknown'],  # 保持原样
    'desk_rect': ['table', 'Table', 'dining_table', 'Dining_table', 'bedside_table'],  # 添加tea_table相关
    'desk_circle': ['table', 'Table', 'dining_table', 'Dining_table', 'bedside_table'],  # 添加tea_table相关
    'weighing-scale': ['weight_scale'],  # 保持原样
    'key': ['keys'],  # 保持原样
    'person': ['person'],  # 保持原样
    'chair': ['chair'],  # 保持原样
    'couch': ['sofa', 'Sofa'],  # 保持原样
    'bed': ['bed', 'Bed'],  # 保持原样
    'tvCabinet': ['tv_cabinet'],  # 保持原样
    'fridge': ['refrigerator'],  # 保持原样
    'television': ['screen'],  # 保持原样
    'washingMachine': ['washing_machine'],  # 保持原样
    'electricFan': ['Fan'],  # 添加Fan标签
    'remoteControl': [],  # 保持原样
    'shoeCabinet': ['shoebox']  # 保持原样
}


def filter_label(original_label):
    """
    过滤并映射标签到预定义的类别

    Args:
        original_label (str): 原始标签名称

    Returns:
        str: 映射后的标签名称，如果没有匹配项则返回原始标签
    """
    try:
        # 确保输入是字符串类型
        if not isinstance(original_label, str):
            return "unknown"

        # 转换标签为小写并去除空格，用于匹配
        normalized_label = original_label.lower().strip()

        # 如果标签为空，返回unknown
        if not normalized_label:
            return "unknown"

        # 遍历映射字典进行匹配
        for target_label, variations in LABEL_MAPPING.items():
            # 检查是否直接匹配目标标签
            if normalized_label == target_label.lower():
                return target_label
            # 检查是否匹配变体列表中的任何一个
            if variations and normalized_label in [v.lower() for v in variations]:
                return target_label

        # 如果没有找到匹配项，返回原始标签
        return original_label

    except Exception as e:
        print(f"Error in filter_label: {str(e)}")
        return "unknown"


def get_bounding_box(points, coords_type="points"):
    """
    Calculate bounding box from either polygon points or bbox coordinates.

    Args:
        points (list): List of coordinates
        coords_type (str): Type of coordinates ("points" or "bbox")

    Returns:
        list: [xmin, ymin, xmax, ymax] or None if error
    """
    try:
        if coords_type == "bbox":
            # bbox格式直接包含 [xmin, ymin, width, height]
            xmin = float(points[0])
            ymin = float(points[1])
            width = float(points[2])
            height = float(points[3])
            # 注意这里的width和height是相对值，需要计算xmax和ymax
            xmax = xmin + width
            ymax = ymin + height
            return [int(xmin), int(ymin), int(xmax), int(ymax)]
        else:  # points格式
            x_coords = []
            y_coords = []
            for i in range(0, len(points), 2):
                x_coords.append(float(points[i]))
                y_coords.append(float(points[i + 1]))

            xmin = min(x_coords)
            ymin = min(y_coords)
            xmax = max(x_coords)
            ymax = max(y_coords)

            return [int(xmin), int(ymin), int(xmax), int(ymax)]
    except (ValueError, TypeError) as e:
        print(f"Error processing points: {e}")
        return None


def get_image_size(image_path):
    """从JPEG或PNG文件中直接读取图像尺寸"""
    try:
        with open(image_path, 'rb') as img_file:
            # 读取前8个字节来判断文件类型
            header = img_file.read(8)

            # 检查是否为PNG文件 (PNG文件头: 89 50 4E 47 0D 0A 1A 0A)
            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                # PNG文件的宽度和高度存储在IHDR块中，跳过8字节的文件头
                img_file.seek(8)
                # 跳过块长度(4字节)和块类型(4字节)
                img_file.seek(8, 1)
                # 读取宽度和高度，各4字节
                width = struct.unpack('>I', img_file.read(4))[0]
                height = struct.unpack('>I', img_file.read(4))[0]
                # 读取位深度
                depth = struct.unpack('B', img_file.read(1))[0]
                return width, height, depth

            # 如果不是PNG，尝试作为JPEG处理
            img_file.seek(2)  # 回到JPEG文件的开始位置后的第2个字节
            while True:
                marker = img_file.read(2)
                if len(marker) < 2:
                    print(f"Warning: Reached end of file before finding size for {image_path}")
                    return None

                length = struct.unpack('>H', img_file.read(2))[0]

                if marker[0] == 0xFF and marker[1] in [0xC0, 0xC1, 0xC2]:
                    img_file.seek(1, 1)
                    height = struct.unpack('>H', img_file.read(2))[0]
                    width = struct.unpack('>H', img_file.read(2))[0]
                    depth = img_file.read(1)[0]
                    return width, height, depth

                img_file.seek(length - 2, 1)

    except Exception as e:
        print(f"Error reading image size for {image_path}: {str(e)}")
        return None


def find_image_file(json_dir, image_name):
    """查找图像文件的位置"""
    # 1. 在JSON文件所在目录查找
    direct_path = os.path.join(json_dir, image_name)
    if os.path.exists(direct_path):
        return direct_path

    # 2. 在JSON目录的父目录查找
    parent_path = os.path.join(os.path.dirname(json_dir), image_name)
    if os.path.exists(parent_path):
        return parent_path

    # 3. 在同级的images目录查找
    images_path = os.path.join(os.path.dirname(json_dir), 'images', image_name)
    if os.path.exists(images_path):
        return images_path

    # 4. 尝试在指定的其他可能位置查找
    additional_paths = [
        os.path.join(json_dir, '..', '..', 'images', image_name),
        os.path.join(json_dir, 'images', image_name),
    ]

    for path in additional_paths:
        full_path = os.path.abspath(path)
        if os.path.exists(full_path):
            return full_path

    print(f"Warning: Could not find image file {image_name}")
    return None


def create_xml(json_data, json_file_path):
    """Create XML annotation from JSON data."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    # 首先尝试从JSON数据中的image_name字段获取图像名称和扩展名
    image_name = data.get('image_name')
    if not image_name:
        # 如果在region中有imageName，使用它
        regions = data.get('region', [])
        if isinstance(regions, list) and len(regions) > 0:
            image_name = regions[0].get('imageName')

    # 如果还是没有找到，使用JSON文件名，并保持原始扩展名(.png)
    if not image_name:
        base_name = os.path.splitext(os.path.basename(json_file_path))[0]
        image_name = f"{base_name}.png"

    print(f"Using image name: {image_name}")

    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "images"
    ET.SubElement(annotation, "filename").text = image_name
    ET.SubElement(annotation, "path").text = f"images/{image_name}"

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"

    # 获取图像尺寸
    size = ET.SubElement(annotation, "size")
    json_dir = os.path.dirname(json_file_path)
    image_path = find_image_file(json_dir, image_name)

    if image_path and os.path.exists(image_path):
        dimensions = get_image_size(image_path)
        if dimensions:
            width, height, depth = dimensions
        else:
            print(f"Warning: Could not get dimensions for {image_name}. Using defaults.")
            width, height, depth = 1920, 1080, 3
    else:
        print(f"Warning: Image file {image_name} not found. Using default dimensions.")
        width, height, depth = 1920, 1080, 3

    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    ET.SubElement(annotation, "segmented").text = "0"

    # 处理region数据
    regions = data.get("region", [])
    if isinstance(regions, dict):
        regions = [regions]

    for region in regions:
        try:
            coords = region.get("coordinates", {})
            if not coords:
                continue

            # 确定坐标类型并获取相应的点
            if "points" in coords:
                points = coords["points"]
                coords_type = "points"
            elif "bbox" in coords:
                points = coords["bbox"]
                coords_type = "bbox"
            else:
                continue

            bbox = get_bounding_box(points, coords_type)
            if not bbox:
                continue

            obj = ET.SubElement(annotation, "object")

            # 获取标签名称，支持不同的数据结构
            original_label = coords.get("name", "unknown")
            filtered_label = filter_label(original_label)

            ET.SubElement(obj, "name").text = filtered_label
            ET.SubElement(obj, "pose").text = "Unspecified"
            ET.SubElement(obj, "truncated").text = "0"
            ET.SubElement(obj, "difficult").text = "0"

            bndbox = ET.SubElement(obj, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(bbox[0])
            ET.SubElement(bndbox, "ymin").text = str(bbox[1])
            ET.SubElement(bndbox, "xmax").text = str(bbox[2])
            ET.SubElement(bndbox, "ymax").text = str(bbox[3])

        except Exception as e:
            print(f"Warning: Error processing region: {str(e)}")
            continue

    return annotation


def process_directory(json_directory, xml_directory):
    """Process all JSON files in a directory and convert them to XML."""
    if not os.path.exists(xml_directory):
        os.makedirs(xml_directory)

    success_count = 0
    failure_count = 0
    problem_files = []

    for json_file in os.listdir(json_directory):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_directory, json_file)
            try:
                print(f"\nProcessing file: {json_file}")  # 添加调试信息

                with open(json_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)
                    print("JSON data loaded successfully")  # 添加调试信息

                print("Creating XML annotation...")  # 添加调试信息
                annotation = create_xml(json_data, json_path)

                if annotation:
                    # 在最后才进行 XML 美化
                    xml_str = prettify_xml(annotation)
                    print("XML string created successfully")  # 添加调试信息

                    # 确保这里有一个有效的文件名
                    base_name = os.path.splitext(json_file)[0]
                    xml_filename = f"{base_name}.xml"

                    if not xml_filename:
                        raise ValueError("Failed to generate XML filename")

                    print(f"XML filename will be: {xml_filename}")  # 添加调试信息

                    xml_path = os.path.join(xml_directory, xml_filename)
                    print(f"Full XML path will be: {xml_path}")  # 添加调试信息

                    with open(xml_path, 'w', encoding='utf-8') as xml_file:
                        xml_file.write(xml_str)
                    print(f"Successfully created: {xml_filename}")
                    success_count += 1
                else:
                    raise Exception("Failed to create XML annotation")

            except Exception as e:
                print(f"Error processing {json_file}: {str(e)}")
                problem_files.append((json_file, str(e)))
                failure_count += 1

    print("\nConversion Summary:")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {failure_count} files")

    if problem_files:
        print("\nProblem files:")
        for file, error in problem_files:
            print(f"- {file}: {error}")


def prettify_xml(elem):
    """
    Return a pretty-printed XML string for the Element.

    Args:
        elem (xml.etree.ElementTree.Element): XML元素对象

    Returns:
        str: 格式化后的XML字符串

    Raises:
        TypeError: 如果输入不是有效的XML Element对象
        xml.etree.ElementTree.ParseError: 如果XML解析失败
    """
    try:
        if not isinstance(elem, ET.Element):
            raise TypeError("Input must be an XML Element object")

        # 将XML元素转换为字节串，指定编码为utf-8
        rough_string = ET.tostring(elem, encoding='utf-8')

        # 使用minidom解析XML并添加格式化
        reparsed = minidom.parseString(rough_string)

        # 获取格式化的XML字符串，设置缩进为两个空格
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')

        # 将字节串解码为字符串，移除额外的空行
        decoded_xml = pretty_xml.decode('utf-8')
        clean_xml = '\n'.join([line for line in decoded_xml.split('\n') if line.strip()])

        return clean_xml

    except ET.ParseError as e:
        print(f"XML parsing error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error in prettify_xml: {str(e)}")
        raise


# 使用示例
if __name__ == "__main__":
    json_directory = "/home/depth/1/"  # Replace with your JSON files path
    xml_directory = "/home/depth/1/"  # Replace with your desired XML output path
    process_directory(json_directory, xml_directory)