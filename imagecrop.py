
import os
import sys
from ultralytics import YOLO

def main(in_dir, out_dir):
    # Load a model
    print("Loading model...")
    model = YOLO("runs/detect/train9/weights/best.pt")  # my trained model

    # make sure out dir exists and make it if it doesn't
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Get list of image files in the in_dir directory
    print("Gathering image files...")
    image_files = [os.path.join(in_dir, f) for f in os.listdir(in_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Run batched inference on the list of images
    print("Running inference on images...")


    for image_file in image_files:
        print(f"\nProcessing {image_file}...")
        results = model([image_file])  # return a list of Results objects


        # Process results
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            # masks = result.masks  # Masks object for segmentation masks outputs
            # keypoints = result.keypoints  # Keypoints object for pose outputs
            # probs = result.probs  # Probs object for classification outputs
            # obb = result.obb  # Oriented boxes object for OBB outputs

            filename = result.path.split("/")[-1]

            if len(result.boxes) > 0:
                # Crop the image using the only bounding box
                result.save_crop(save_dir=out_dir, file_name=filename)
                print(f"Image cropped and saved to {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python imagecrop.py <in_dir> <out_dir>")
        sys.exit(1)

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    main(in_dir, out_dir)