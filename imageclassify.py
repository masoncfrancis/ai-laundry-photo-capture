
import os
import sys
from ultralytics import YOLO

def main(in_dir):
    # Load a model
    print("Loading model...")
    model = YOLO("runs/classify/train/weights/best.pt")  # my trained model

    # Get list of image files in the in_dir directory
    print("Gathering image files...")
    image_files = [os.path.join(in_dir, f) for f in os.listdir(in_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Run inference on the list of images
    print("Running inference on images...")


    for image_file in image_files:
        print(f"\nProcessing {image_file}...")
        results = model([image_file])  # return a list of Results objects


        # Process results
        for result in results:

            # get filename, splitting the path by / or \ depending on OS
            filename = result.path.split("/")[-1] if "/" in result.path else result.path.split("\\")[-1]

            # print out highest probability class for each image
            summary = result.summary()
            print(f"Image: {filename}, Class: {summary[0]['name']}, Probability: {summary[0]['confidence']}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python imageclassify.py <in_dir>")
        sys.exit(1)

    in_dir = sys.argv[1]

    main(in_dir)