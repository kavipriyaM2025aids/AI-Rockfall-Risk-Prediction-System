import os
import glob
import json
from collections import Counter

dataset_dir = r"c:\Users\kavi priya\Downloads\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
ann_dir = os.path.join(dataset_dir, "annotation")

json_files = glob.glob(os.path.join(ann_dir, "*.json"))

labels_counter = Counter()
example_labels = []

print(f"Total JSON files: {len(json_files)}")

for i, jf in enumerate(json_files):
    if i % 1000 == 0:
        print(f"Processing file {i}/{len(json_files)}")
    try:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for shape in data.get('shapes', []):
                label = shape.get('label')
                # Important: DO NOT cast to string or list blindly, get exactly what's there
                # If label is not a string, let's convert it to string just to represent it, but carefully
                if not isinstance(label, str):
                    label_str = str(label)
                else:
                    label_str = label
                    
                labels_counter[label_str] += 1
                if len(example_labels) < 20:
                    example_labels.append(repr(label_str))
    except Exception as e:
        print(f"Error parsing {jf}: {e}")

print("\n===== ORIGINAL JSON LABELS =====")
unique_labels = list(labels_counter.keys())
print(f"Unique labels: {unique_labels}")

print("\nLabel counts:")
for lbl, count in labels_counter.items():
    print(f"  {repr(lbl)}: {count}")

print("\nExamples of raw labels stored in JSON:")
for ex in example_labels:
    print(f"  {ex}")
    
# Let's see if there are any weird characters in the unique labels
print("\nChecking for weird characters:")
for lbl in unique_labels:
    has_ws = any(c.isspace() for c in lbl)
    has_quote = "'" in lbl or '"' in lbl
    has_nl = "\n" in lbl
    is_empty = len(lbl) == 0
    print(f"Label {repr(lbl)} -> has_ws: {has_ws}, has_quote: {has_quote}, has_nl: {has_nl}, is_empty: {is_empty}")
