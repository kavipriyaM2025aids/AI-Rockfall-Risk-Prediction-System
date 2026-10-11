import os
import glob
import json
import random
import cv2

def verify_yolo():
    yolo_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\dataset\yolo"
    verify_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\dataset\yolo_verification"
    report_json_path = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\dataset\yolo_verification_report.json"
    report_txt_path = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\dataset\yolo_verification_report.txt"
    
    # 1. Structure Verification
    expected_paths = [
        os.path.join(yolo_dir, "images", "train"),
        os.path.join(yolo_dir, "images", "val"),
        os.path.join(yolo_dir, "images", "test"),
        os.path.join(yolo_dir, "labels", "train"),
        os.path.join(yolo_dir, "labels", "val"),
        os.path.join(yolo_dir, "labels", "test"),
        os.path.join(yolo_dir, "data.yaml"),
        os.path.join(yolo_dir, "preprocessing_report.json")
    ]
    
    missing_structure = []
    for p in expected_paths:
        if not os.path.exists(p):
            missing_structure.append(p)
            
    # Track stats
    stats = {
        'train': {'images': 0, 'labels': 0},
        'val': {'images': 0, 'labels': 0},
        'test': {'images': 0, 'labels': 0}
    }
    
    class_0_count = 0
    class_1_count = 0
    missing_images = []
    missing_labels = []
    invalid_class_ids = []
    invalid_coords = []
    invalid_dims = []
    malformed_lines = []
    duplicates = []
    
    all_filenames = set()
    
    splits = ['train', 'val', 'test']
    
    # Selection for visualization
    vis_samples = {'train': [], 'val': [], 'test': []}
    
    for split in splits:
        img_dir = os.path.join(yolo_dir, "images", split)
        lbl_dir = os.path.join(yolo_dir, "labels", split)
        
        if not os.path.exists(img_dir) or not os.path.exists(lbl_dir):
            continue
            
        images = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]
        labels = [f for f in os.listdir(lbl_dir) if f.endswith('.txt')]
        
        stats[split]['images'] = len(images)
        stats[split]['labels'] = len(labels)
        
        img_basenames = set([f.replace('.jpg', '') for f in images])
        lbl_basenames = set([f.replace('.txt', '') for f in labels])
        
        for name in img_basenames:
            if name in all_filenames:
                duplicates.append(name)
            all_filenames.add(name)
            
        missing_l = img_basenames - lbl_basenames
        missing_i = lbl_basenames - img_basenames
        
        for m in missing_l: missing_labels.append(f"{split}/{m}.txt")
        for m in missing_i: missing_images.append(f"{split}/{m}.jpg")
        
        # Parse labels
        for lbl_file in labels:
            lbl_path = os.path.join(lbl_dir, lbl_file)
            img_path = os.path.join(img_dir, lbl_file.replace('.txt', '.jpg'))
            
            with open(lbl_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            has_0 = False
            has_1 = False
            
            for line_idx, line in enumerate(lines):
                parts = line.strip().split()
                if len(parts) != 5:
                    malformed_lines.append(f"{lbl_path}:{line_idx}")
                    continue
                    
                try:
                    cid = int(parts[0])
                    cx = float(parts[1])
                    cy = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])
                except ValueError:
                    malformed_lines.append(f"{lbl_path}:{line_idx} (non-numeric)")
                    continue
                    
                if cid == 0:
                    class_0_count += 1
                    has_0 = True
                elif cid == 1:
                    class_1_count += 1
                    has_1 = True
                else:
                    invalid_class_ids.append(f"{lbl_path}:{line_idx} (ID={cid})")
                    
                if cx < 0.0 or cx > 1.0 or cy < 0.0 or cy > 1.0:
                    invalid_coords.append(f"{lbl_path}:{line_idx} (cx={cx}, cy={cy})")
                    
                if w <= 0.0 or w > 1.0 or h <= 0.0 or h > 1.0:
                    invalid_dims.append(f"{lbl_path}:{line_idx} (w={w}, h={h})")
                    
            if os.path.exists(img_path):
                vis_samples[split].append({
                    'img_path': img_path,
                    'lbl_path': lbl_path,
                    'has_0': has_0,
                    'has_1': has_1
                })
                
    # 4. Visualization
    vis_counts = {'train': 10, 'val': 5, 'test': 5}
    selected_vis = {}
    
    random.seed(42)
    for split in splits:
        os.makedirs(os.path.join(verify_dir, split), exist_ok=True)
        samples = vis_samples[split]
        random.shuffle(samples)
        
        # Try to prioritize images with both, or at least class 1
        both = [s for s in samples if s['has_0'] and s['has_1']]
        c1_only = [s for s in samples if not s['has_0'] and s['has_1']]
        c0_only = [s for s in samples if s['has_0'] and not s['has_1']]
        none = [s for s in samples if not s['has_0'] and not s['has_1']]
        
        sorted_samples = both + c1_only + c0_only + none
        target = min(vis_counts[split], len(sorted_samples))
        final_selection = sorted_samples[:target]
        selected_vis[split] = []
        
        for idx, item in enumerate(final_selection):
            img_path = item['img_path']
            lbl_path = item['lbl_path']
            out_name = f"{split}_{idx+1:03d}.jpg"
            out_path = os.path.join(verify_dir, split, out_name)
            
            img = cv2.imread(img_path)
            if img is not None:
                img_h, img_w = img.shape[:2]
                with open(lbl_path, 'r') as f:
                    for line in f.readlines():
                        parts = line.strip().split()
                        if len(parts) == 5:
                            cid = int(parts[0])
                            cx, cy, w, h = map(float, parts[1:])
                            
                            x_min = int((cx - w/2) * img_w)
                            y_min = int((cy - h/2) * img_h)
                            x_max = int((cx + w/2) * img_w)
                            y_max = int((cy + h/2) * img_h)
                            
                            color = (0, 255, 0) if cid == 0 else (255, 0, 0)
                            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
                            cv2.putText(img, f"Class {cid}", (x_min, max(0, y_min - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                            
                cv2.imwrite(out_path, img)
                selected_vis[split].append(out_path)
                
    overall_status = "PASS"
    verification_errors = len(missing_structure) + len(missing_images) + len(missing_labels) + len(invalid_class_ids) + len(invalid_coords) + len(invalid_dims) + len(malformed_lines) + len(duplicates)
    
    if verification_errors > 0:
        overall_status = "FAIL"
        
    report = f'''========================================
YOLO DATASET VERIFICATION COMPLETE
========================================

Dataset:
{yolo_dir}

Train images:
{stats['train']['images']}

Validation images:
{stats['val']['images']}

Test images:
{stats['test']['images']}

Train labels:
{stats['train']['labels']}

Validation labels:
{stats['val']['labels']}

Test labels:
{stats['test']['labels']}

Class 0 objects:
{class_0_count}

Class 1 objects:
{class_1_count}

Missing images:
{len(missing_images)}

Missing labels:
{len(missing_labels)}

Invalid labels:
{len(invalid_class_ids)} (Invalid Class IDs)
{len(malformed_lines)} (Malformed lines)

Invalid coordinates:
{len(invalid_coords)}

Invalid dimensions:
{len(invalid_dims)}

Duplicate filenames:
{len(duplicates)}

Missing structure:
{len(missing_structure)}

Verification errors:
{verification_errors}

Overall status:
{overall_status}

Verification samples:
{verify_dir}

Report:
{report_json_path}
{report_txt_path}
'''

    print(report)
    
    with open(report_txt_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    report_dict = {
        'status': overall_status,
        'stats': stats,
        'class_0_count': class_0_count,
        'class_1_count': class_1_count,
        'errors': {
            'missing_structure': missing_structure,
            'missing_images': missing_images,
            'missing_labels': missing_labels,
            'invalid_class_ids': invalid_class_ids,
            'invalid_coords': invalid_coords,
            'invalid_dims': invalid_dims,
            'malformed_lines': malformed_lines,
            'duplicates': duplicates
        },
        'vis_samples': selected_vis
    }
    
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(report_dict, f, indent=4)

if __name__ == "__main__":
    verify_yolo()
