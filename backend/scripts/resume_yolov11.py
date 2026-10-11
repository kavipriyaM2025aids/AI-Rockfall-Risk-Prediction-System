import os
import sys
import time

# Limit CPU usage to prevent laptop overheating
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
os.environ["VECLIB_MAXIMUM_THREADS"] = "2"
os.environ["NUMEXPR_NUM_THREADS"] = "2"

import torch
torch.set_num_threads(2)

from ultralytics import YOLO

def main():
    checkpoint_path = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\runs\detect\rockguard_yolov11\weights\last.pt"
    
    print("========================================")
    print("ROCKGUARD AI — YOLOv11 RESUME")
    print("========================================")
    print(f"Checkpoint:\n{checkpoint_path}")
    print("\nModel:\nYOLOv11 Nano")
    print("\nPrevious completed epochs:\n4")
    print("\nTarget epochs:\n50")
    print("\nImage size:\n640")
    print("\nBatch:\n16")
    print("\nWorkers:\n0")
    print("\nDevice:\nCPU")
    print("\nPyTorch CPU threads:\n2")
    print("========================================")
    print("\nLoading checkpoint...")
    
    try:
        model = YOLO(checkpoint_path)
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        sys.exit(1)
        
    print("Resuming training...")
    start_time = time.time()
    try:
        model.train(resume=True)
    except Exception as e:
        print(f"Training stopped due to error: {e}")
        sys.exit(1)
        
    end_time = time.time()
    print(f"Training duration: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
