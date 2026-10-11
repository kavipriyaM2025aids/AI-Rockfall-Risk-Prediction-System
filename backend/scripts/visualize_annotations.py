import os
import glob
import json

def run_visualization():
    try:
        import cv2
        use_cv2 = True
    except ImportError:
        use_cv2 = False
        from PIL import Image, ImageDraw, ImageFont

    dataset_path = r"C:\Users\kavi priya\Downloads\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
    images_dir = os.path.join(dataset_path, "images")
    annotations_dir = os.path.join(dataset_path, "annotation")
    
    out_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\dataset_annotation_samples"
    
    class_dirs = {
        '1': os.path.join(out_dir, "class_1"),
        'n': os.path.join(out_dir, "class_n"),
        '': os.path.join(out_dir, "class_empty"),
        "'": os.path.join(out_dir, "class_apostrophe")
    }
    
    for d in class_dirs.values():
        os.makedirs(d, exist_ok=True)
        
    report_file = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\annotation_visualization_report.txt"
    
    # Limits requested: 10 for '1', 10 for 'n', all for empty, all for "'"
    limits = {
        '1': 10,
        'n': 10,
        '': 1000,
        "'": 1000
    }
    
    counts = {k: 0 for k in limits.keys()}
    
    json_files = glob.glob(os.path.join(annotations_dir, "**", "*.json"), recursive=True)
    
    report_lines = ["ANNOTATION VISUALIZATION REPORT", "================================="]
    
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            img_basename = os.path.basename(jf).replace('.json', '')
            img_path = os.path.join(images_dir, img_basename + ".jpg")
            
            if not os.path.exists(img_path):
                continue
                
            img_classes = set()
            for shape in data.get('shapes', []):
                label = str(shape.get('label', '')).strip()
                if label == '':
                    label = ''
                img_classes.add(label)
                
            target_classes = []
            should_process = False
            for c in img_classes:
                c_mapped = c if c in limits else ''
                if counts[c_mapped] < limits[c_mapped]:
                    should_process = True
                    target_classes.append(c_mapped)
                    counts[c_mapped] += 1
                    
            if not should_process:
                continue
                
            if use_cv2:
                img = cv2.imread(img_path)
                if img is None: continue
                img_h, img_w = img.shape[:2]
            else:
                img = Image.open(img_path).convert('RGB')
                draw = ImageDraw.Draw(img)
                img_w, img_h = img.size
            
            for shape in data.get('shapes', []):
                label = str(shape.get('label', '')).strip()
                if label == '': label = ''
                
                points = shape.get('points', [])
                
                if len(points) == 2:
                    p1, p2 = points
                    x_min, y_min = min(p1[0], p2[0]), min(p1[1], p2[1])
                    x_max, y_max = max(p1[0], p2[0]), max(p1[1], p2[1])
                    
                    is_oob = (x_min < 0 or y_min < 0 or x_max > img_w or y_max > img_h)
                    
                    if use_cv2:
                        color = (0, 0, 255) if is_oob else (0, 255, 0)
                        thickness = 4 if is_oob else 2
                        cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, thickness)
                        text = f"{label} (OOB)" if is_oob else (label if label else "EMPTY")
                        cv2.putText(img, text, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    else:
                        color = "red" if is_oob else "green"
                        width = 4 if is_oob else 2
                        draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=width)
                        text = f"{label} (OOB)" if is_oob else (label if label else "EMPTY")
                        draw.text((x_min, y_min - 15), text, fill=color)
                        
                    report_lines.append(f"Image: {img_basename}.jpg | Label: '{label}' | BBox: [{x_min:.2f}, {y_min:.2f}, {x_max:.2f}, {y_max:.2f}] | OOB: {is_oob}")
            
            for c in target_classes:
                out_path = os.path.join(class_dirs[c], img_basename + "_vis.jpg")
                if use_cv2:
                    cv2.imwrite(out_path, img)
                else:
                    img.save(out_path)
                
        except Exception as e:
            print(f"Error processing {jf}: {e}")
            continue
            
    with open(report_file, 'w', encoding='utf-8') as rf:
        rf.write("\n".join(report_lines))
        
    print(f"Visualization complete. Saved representations.")
    for k, v in counts.items():
        print(f"Class '{k}': {v} images")
    print(f"Report generated at {report_file}")

if __name__ == '__main__':
    run_visualization()
