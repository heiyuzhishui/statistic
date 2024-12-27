import os
import json
from xml.etree import ElementTree as ET
from xml.dom import minidom


def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def get_bounding_box(points):
    """Calculate bounding box from polygon points."""
    try:
        # Convert points from strings to floats and separate x, y coordinates
        x_coords = []
        y_coords = []
        for i in range(0, len(points), 2):
            x_coords.append(float(points[i]))
            y_coords.append(float(points[i + 1]))

        # Calculate bounding box
        xmin = min(x_coords)
        ymin = min(y_coords)
        xmax = max(x_coords)
        ymax = max(y_coords)

        return [int(xmin), int(ymin), int(xmax), int(ymax)]
    except (ValueError, TypeError) as e:
        print(f"Error processing points: {e}")
        return None


def create_xml(json_data, image_name):
    """Create XML annotation from JSON data."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "images"
    ET.SubElement(annotation, "filename").text = image_name
    ET.SubElement(annotation, "path").text = f"images/{image_name}"

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = "1920"
    ET.SubElement(size, "height").text = "1080"
    ET.SubElement(size, "depth").text = "3"

    ET.SubElement(annotation, "segmented").text = "0"

    if "region" in data:
        for region in data["region"]:
            try:
                coords = region.get("coordinates", {})
                if not coords:
                    print(f"Warning: No coordinates found in region for {image_name}")
                    continue

                # Skip if no points or invalid points
                points = coords.get("points")
                if not points:
                    print(f"Warning: No points found in coordinates for {image_name}")
                    continue

                # Get bounding box
                bbox = get_bounding_box(points)
                if not bbox:
                    print(f"Warning: Could not calculate bounding box for {image_name}")
                    continue

                obj = ET.SubElement(annotation, "object")
                name = coords.get("name", "unknown")
                obj_class = coords.get("class", "unknown")

                # Use both name and class for the object name if available
                ET.SubElement(obj, "name").text = f"{name}_{obj_class}" if obj_class != "unknown" else name
                ET.SubElement(obj, "pose").text = "Unspecified"
                ET.SubElement(obj, "truncated").text = "0"
                ET.SubElement(obj, "difficult").text = "0"

                bndbox = ET.SubElement(obj, "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(bbox[0])
                ET.SubElement(bndbox, "ymin").text = str(bbox[1])
                ET.SubElement(bndbox, "xmax").text = str(bbox[2])
                ET.SubElement(bndbox, "ymax").text = str(bbox[3])

            except Exception as e:
                print(f"Warning: Error processing region in {image_name}: {str(e)}")
                continue

    return prettify_xml(annotation)


def process_directory(json_directory, xml_directory):
    """Process all JSON files in a directory and convert them to XML."""
    if not os.path.exists(xml_directory):
        os.makedirs(xml_directory)

    # Keep track of success and failure counts
    success_count = 0
    failure_count = 0
    problem_files = []

    for json_file in os.listdir(json_directory):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_directory, json_file)
            try:
                with open(json_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)

                    # Check if image_name exists
                    image_name = json_data.get('image_name')
                    if not image_name:
                        # Try to get from file object if exists
                        image_name = json_data.get('file', {}).get('name')
                        if not image_name:
                            print(f"Warning: No image name found in {json_file}")
                            image_name = os.path.splitext(json_file)[0] + '.jpg'

                    xml_str = create_xml(json_data, image_name)
                    xml_filename = os.path.splitext(image_name)[0] + '.xml'
                    xml_path = os.path.join(xml_directory, xml_filename)

                    with open(xml_path, 'w', encoding='utf-8') as xml_file:
                        xml_file.write(xml_str)
                    print(f"XML file '{xml_filename}' has been created successfully.")
                    success_count += 1

            except Exception as e:
                print(f"Error processing {json_file}: {str(e)}")
                problem_files.append((json_file, str(e)))
                failure_count += 1

    # Print summary
    print("\nConversion Summary:")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {failure_count} files")
    if problem_files:
        print("\nProblem files:")
        for file, error in problem_files:
            print(f"- {file}: {error}")


# Usage
if __name__ == "__main__":
    json_directory = "/home/depth/下载/ck/ck9/"  # Replace with your JSON files path
    xml_directory = "/home/depth/下载/ck/ck9/"  # Replace with your desired XML output path
    process_directory(json_directory, xml_directory)