import os
import glob
import json

def parse_labels():
    dataset_path = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\dataset\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
    annotations_dir = os.path.join(dataset_path, "annotation")
    annotation_files = glob.glob(os.path.join(annotations_dir, "**", "*.json"), recursive=True)
    
    classes = {}
    shape_types = set()
    
    for json_file in annotation_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for shape in data.get('shapes', []):
                    lbl = str(shape.get('label'))
                    classes[lbl] = classes.get(lbl, 0) + 1
                    shape_types.add(shape.get('shape_type'))
        except Exception as e:
            print(f"Error parsing {json_file}: {e}")
            
    print(f"Total annotations processed: {sum(classes.values())}")
    print(f"Shape types found: {list(shape_types)}")
    print("Classes found:")
    for c, count in sorted(classes.items(), key=lambda x: int(x[0]) if x[0].isdigit() else x[0]):
        print(f"  - Class '{c}': {count} objects")

if __name__ == "__main__":
    parse_labels()
