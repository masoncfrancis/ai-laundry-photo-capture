from ultralytics import YOLO

# Load a model
model = YOLO("runs/detect/train/weights/best.pt")  # my trained model

# Run batched inference on a list of images
results = model(["testimage1.jpg", "testimage2.jpg", "testimage3.jpg", "testimage4.jpg", "testimage5.jpg"])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    # I can get the number of boxes in an image using len(result.boxes)

    # # get filename
    # filename = result.path.split("/")[-1]

    # # save the image with bounding boxes
    # result.save(filename="test"+filename)
