from ultralytics import YOLO
from PIL import Image
import json

# Load a model
model = YOLO("runs/detect/train/weights/best.pt")  # my trained model

# Run batched inference on a list of images
results = model(["testimage1.jpg", "testimage2.jpg", "testimage3.jpg", "testimage4.jpg", "testimage5.jpg", "testimage6.jpg"])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    # result.show()  # display to screen
    # I can get the number of boxes in an image using len(result.boxes)

    # get filename
    filename = result.path.split("/")[-1]

    # save the image with bounding boxes overlayed
    # result.save(filename="test"+filename)

    # save the image cropped to bounding box
    # result.save_crop(save_dir=".", file_name="crop"+filename)

    # crop the image using the bounding box, adding a small buffer area around the box to make the output image 275x200
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
        xBuffer = (275 - xSize) // 2
        yBuffer = (200 - ySize) // 2

        # Crop the image
        croppedImage = image.crop((x1 - xBuffer, y1 - yBuffer, x2 + xBuffer, y2 + yBuffer))
        croppedImage.save("cropped" + filename)


        
    else:
        print("No bounding box found in image.")
