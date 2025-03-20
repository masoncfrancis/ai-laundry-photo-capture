
import os
import sys
import json
from PIL import Image
from ultralytics import YOLO

def main(in_dir, out_dir):
    # Load a model
    print("Loading model...")
    model = YOLO("runs/detect/train/weights/best.pt")  # my trained model

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
            
            # get filename, splitting the path by / or \ depending on OS
            filename = result.path.split("/")[-1] if "/" in result.path else result.path.split("\\")[-1]

            if len(result.boxes) > 0:
                boxCoords = json.loads(result.to_json())[0]["box"]
            x1 = boxCoords["x1"]
            y1 = boxCoords["y1"]
            x2 = boxCoords["x2"]
            y2 = boxCoords["y2"]

            # Use pillow to crop the image
            image = Image.open(result.path)
            xSize = x2 - x1
            ySize = y2 - y1

            # Add space around bounding box to make the output image 275x200
            xBufferLeft = ((275 - xSize) // 2) + ((275 - xSize) % 2) # adds remainder of division operation to left buffer to make sure image is 275x200
            xBufferRight = (275 - xSize) // 2
            yBufferTop = ((200 - ySize) // 2) + ((200 - ySize) % 2)  # adds remainder of division operation to top buffer to make sure image is 275x200
            yBufferBottom = (200 - ySize) // 2 

            # Crop the image
            croppedImage = image.crop((x1 - xBufferLeft, y1 - yBufferTop, x2 + xBufferRight, y2 + yBufferBottom))
            croppedImage.save(os.path.join(out_dir, filename))
            print(f"Image cropped and saved as {filename}.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python imagecrop.py <in_dir> <out_dir>")
        sys.exit(1)

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    main(in_dir, out_dir)