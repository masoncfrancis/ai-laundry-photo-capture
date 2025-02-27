from ultralytics import YOLO


# Load a model
model = YOLO("runs/detect/train9/weights/best.pt")  # my trained model

# Run batched inference on a list of images
results = model(["testimage1.jpg", "testimage2.jpg", "testimage3.jpg", "testimage4.jpg"])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs

    if len(result.boxes) > 0:
        # Crop the image using the first bounding box
        result.save_crop("croppedtest")
        print("Image cropped and saved to croppedtest")

    # don't need to crop images that don't have control panel in them since the API will return that the washer is not in use anyway if boxes can't be found
