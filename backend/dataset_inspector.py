import os
import glob
from collections import defaultdict

def inspect_dataset(dataset_path: str):
    print(f"Inspecting dataset at: {dataset_path}")
    if not os.path.exists(dataset_path) or not os.path.isdir(dataset_path):
        print("Dataset directory does not exist or is empty.")
        return None

    # Check for image files
    image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp')
    images = []
    for ext in image_extensions:
        images.extend(glob.glob(os.path.join(dataset_path, '**', ext), recursive=True))

    total_images = len(images)
    print(f"Total Images: {total_images}")

    if total_images == 0:
        return {"total_images": 0, "classes": {}}

    # Try to deduce classes based on directory structure
    class_counts = defaultdict(int)
    for img in images:
        parent_dir = os.path.basename(os.path.dirname(img))
        # If the parent directory is the dataset root itself, then the images are not categorized by folder
        if os.path.abspath(os.path.dirname(img)) != os.path.abspath(dataset_path):
            class_counts[parent_dir] += 1
        else:
            class_counts["Unclassified"] += 1

    print("\nClasses Distribution:")
    for cls, count in class_counts.items():
        print(f" - {cls} → {count} images")

    # Check for annotations (YOLO/COCO style or CSV/JSON)
    annotations = []
    anno_extensions = ('*.txt', '*.json', '*.csv', '*.xml')
    for ext in anno_extensions:
        annotations.extend(glob.glob(os.path.join(dataset_path, '**', ext), recursive=True))

    print(f"\nTotal Annotation Files Found: {len(annotations)}")
    if len(annotations) > 0:
        for idx, anno in enumerate(annotations[:5]):
            print(f" - {os.path.basename(anno)}")
        if len(annotations) > 5:
            print(f" ... and {len(annotations) - 5} more")
    
    return {
        "total_images": total_images,
        "classes": dict(class_counts),
        "annotation_count": len(annotations)
    }

if __name__ == "__main__":
    dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
    inspect_dataset(dataset_dir)
