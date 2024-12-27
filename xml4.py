# coding=utf-8
import os
import json
from xml.etree import ElementTree as ET
from xml.dom import minidom
import os.path
import struct

# 标签映射字典
LABEL_MAPPING = {
    'shoes': ['Slippers',],
    'bin': ['trash_can', 'trash', 'trash can'],
    'pedestal': ['base', 'Landing', 'Fan base'],
    'wire': ['cable', 'Cable', 'charger', 'Electric', 'Cable',],
    'socket': ['plug_in_board'],
    'cat': ['pet_cat', 'Cat', 'pet_unknown', 'Pet'],
    'dog': ['pet_dog', 'Dog'],
    'desk_rect': ['table', 'Table', 'dining_table', 'Dining_table', 'bedside_table'],
    'weighing-scale': ['weight_scale', 'Weighing'],
    'key': ['keys'],
    'person': ['person'],
    'chair': ['chair'],
    'couch': ['sofa', 'Sofa'],
    'bed': ['bed', 'Bed'],
    'tvCabinet': ['tv_cabinet', 'TV cabinet'],
    'fridge': ['refrigerator', 'Refrigerator'],
    'television': ['screen', 'TV', 'Television'],
    'washingMachine': ['washing_machine', 'Washing'],
    'electricFan': ['Fan'],
    'remoteControl': [],
    'shoeCabinet': ['shoebox']
}


def create_output_directory(input_path):
    """
    Create output directory based on input path.

    Args:
        input_path (str): Input directory path

    Returns:
        str: Path to output directory
    """
    # Get the parent directory and current folder name
    parent_dir = os.path.dirname(input_path.rstrip('/'))
    current_folder = os.path.basename(input_path.rstrip('/'))

    # Create new folder name with _xml suffix
    output_folder = f"{current_folder}_xml"

    # Create full output path
    output_path = os.path.join(parent_dir, output_folder)

    # Create directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")

    return output_path


def filter_label(original_label):
    """
    过滤并映射标签到预定义的类别

    Args:
        original_label (str): 原始标签名称

    Returns:
        str: 映射后的标签名称，如果没有匹配项则返回原始标签
    """
    try:
        if not isinstance(original_label, str):
            return "unknown"

        normalized_label = original_label.lower().strip()

        if not normalized_label:
            return "unknown"

        for target_label, variations in LABEL_MAPPING.items():
            if normalized_label == target_label.lower():
                return target_label
            if variations and normalized_label in [v.lower() for v in variations]:
                return target_label

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
            xmin = float(points[0])
            ymin = float(points[1])
            width = float(points[2])
            height = float(points[3])
            xmax = xmin + width
            ymax = ymin + height
            return [int(xmin), int(ymin), int(xmax), int(ymax)]
        else:
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
            header = img_file.read(8)

            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                img_file.seek(8)
                img_file.seek(8, 1)
                width = struct.unpack('>I', img_file.read(4))[0]
                height = struct.unpack('>I', img_file.read(4))[0]
                depth = struct.unpack('B', img_file.read(1))[0]
                return width, height, depth

            img_file.seek(2)
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
    # 在不同位置尝试查找图像文件
    search_paths = [
        os.path.join(json_dir, image_name),
        os.path.join(os.path.dirname(json_dir), image_name),
        os.path.join(os.path.dirname(json_dir), 'images', image_name),
        os.path.join(json_dir, '..', '..', 'images', image_name),
        os.path.join(json_dir, 'images', image_name),
    ]

    for path in search_paths:
        full_path = os.path.abspath(path)
        if os.path.exists(full_path):
            return full_path

    print(f"Warning: Could not find image file {image_name}")
    return None


def create_xml(json_data, json_file_path):
    """Create XML annotation from JSON data."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    image_name = data.get('image_name')
    if not image_name:
        regions = data.get('region', [])
        if isinstance(regions, list) and len(regions) > 0:
            image_name = regions[0].get('imageName')

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

    size = ET.SubElement(annotation, "size")
    json_dir = os.path.dirname(json_file_path)
    image_path = find_image_file(json_dir, image_name)

    if image_path and os.path.exists(image_path):
        dimensions = get_image_size(image_path)
        if dimensions:
            width, height, depth = dimensions
        else:
            width, height, depth = 1920, 1080, 3
    else:
        width, height, depth = 1920, 1080, 3

    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    ET.SubElement(annotation, "segmented").text = "0"

    regions = data.get("region", [])
    if isinstance(regions, dict):
        regions = [regions]

    for region in regions:
        try:
            coords = region.get("coordinates", {})
            if not coords:
                continue

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


def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    try:
        if not isinstance(elem, ET.Element):
            raise TypeError("Input must be an XML Element object")

        rough_string = ET.tostring(elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
        decoded_xml = pretty_xml.decode('utf-8')
        clean_xml = '\n'.join([line for line in decoded_xml.split('\n') if line.strip()])

        return clean_xml

    except ET.ParseError as e:
        print(f"XML parsing error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error in prettify_xml: {str(e)}")
        raise


def process_directory_recursive(input_path):
    """
    Recursively process all subdirectories while maintaining directory structure.

    Args:
        input_path (str): Root input directory path
    """
    # Create base output directory
    base_output_path = create_output_directory(input_path)

    # Walk through all subdirectories
    for root, dirs, files in os.walk(input_path):
        # Calculate relative path from input root
        rel_path = os.path.relpath(root, input_path)

        # Create corresponding output directory path
        output_dir = os.path.join(base_output_path, rel_path) if rel_path != '.' else base_output_path

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Process JSON files in current directory
        success_count = 0
        failure_count = 0
        problem_files = []

        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(root, file)
                try:
                    print(f"\nProcessing file: {file}")

                    with open(json_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                        print("JSON data loaded successfully")

                    print("Creating XML annotation...")
                    annotation = create_xml(json_data, json_path)

                    if annotation:
                        xml_str = prettify_xml(annotation)
                        print("XML string created successfully")

                        base_name = os.path.splitext(file)[0]
                        xml_filename = f"{base_name}.xml"

                        if not xml_filename:
                            raise ValueError("Failed to generate XML filename")

                        xml_path = os.path.join(output_dir, xml_filename)
                        print(f"Saving XML to: {xml_path}")

                        with open(xml_path, 'w', encoding='utf-8') as xml_file:
                            xml_file.write(xml_str)
                        print(f"Successfully created: {xml_filename}")
                        success_count += 1
                    else:
                        raise Exception("Failed to create XML annotation")

                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
                    problem_files.append((file, str(e)))
                    failure_count += 1

        # Print summary for current directory
        if success_count > 0 or failure_count > 0:
            print(f"\nDirectory Summary for {root}:")
            print(f"Successfully processed: {success_count} files")
            print(f"Failed to process: {failure_count} files")

            if problem_files:
                print("\nProblem files:")
                for file, error in problem_files:
                    print(f"- {file}: {error}")


if __name__ == "__main__":
    # 示例使用
    input_path = "/media/depth/v/20241224/"  # 替换为你的输入路径
    process_directory_recursive(input_path)