# ai-laundry-photo-capture
A collection of scripts for capturing and labeling photos intended to train an image classification ai model


## install

Make sure to install pytorch before installing
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

## train

Run this command to train. Images are automatically resized to 640 because that's what the model was trained on.

```
yolo detect train data=trainyolo.yaml model=yolo11s.pt epochs=60 imgsz=640
```
