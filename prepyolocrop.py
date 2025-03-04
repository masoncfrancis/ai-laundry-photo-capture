import os
import sys
from sklearn.model_selection import train_test_split
import shutil

def verify_annotations(images, annotations):
    print("Verifying labels...")
    image_basenames = {os.path.splitext(os.path.basename(img))[0] for img in images}
    annotation_basenames = {os.path.splitext(os.path.basename(ann))[0] for ann in annotations}
    missing_annotations = image_basenames - annotation_basenames
    if missing_annotations:
        print(f"Error: Missing labels for images: {', '.join(missing_annotations)}")
        sys.exit(1)
    print("All labels are present.")

def sortImagesAndAnnotations(directory):
    print(f"Sorting images and labels in directory: {directory}")
    images = [os.path.join(directory + '/images', x) for x in os.listdir(directory + '/images')]
    annotations = [os.path.join(directory + '/labels', x) for x in os.listdir(directory + '/labels') if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    verify_annotations(images, annotations)

    print("Splitting data into training, validation, and test sets...")
    train_images, test_images, train_annotations, test_annotations = train_test_split(images, annotations, test_size=0.2, random_state=42)
    val_images, test_images, val_annotations, test_annotations = train_test_split(test_images, test_annotations, test_size=0.5, random_state=42)

    train_img_dir = os.path.join(directory, 'images/train')
    val_img_dir = os.path.join(directory, 'images/val')
    test_img_dir = os.path.join(directory, 'images/test')

    train_ann_dir = os.path.join(directory, 'labels/train')
    val_ann_dir = os.path.join(directory, 'labels/val')
    test_ann_dir = os.path.join(directory, 'labels/test')

    print("Creating directories for training, validation, and test sets...")
    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(test_img_dir, exist_ok=True)

    os.makedirs(train_ann_dir, exist_ok=True)
    os.makedirs(val_ann_dir, exist_ok=True)
    os.makedirs(test_ann_dir, exist_ok=True)

    print("Moving images and labels to the appropriate directories...")
    for img, ann in zip(train_images, train_annotations):
        print(f"Moving {img} to {os.path.join(train_img_dir, os.path.basename(img))}")
        shutil.move(img, os.path.join(train_img_dir, os.path.basename(img)))
        print(f"Moving {ann} to {os.path.join(train_ann_dir, os.path.basename(ann))}")
        shutil.move(ann, os.path.join(train_ann_dir, os.path.basename(ann)))

    for img, ann in zip(val_images, val_annotations):
        print(f"Moving {img} to {os.path.join(val_img_dir, os.path.basename(img))}")
        shutil.move(img, os.path.join(val_img_dir, os.path.basename(img)))
        print(f"Moving {ann} to {os.path.join(val_ann_dir, os.path.basename(ann))}")
        shutil.move(ann, os.path.join(val_ann_dir, os.path.basename(ann)))

    for img, ann in zip(test_images, test_annotations):
        print(f"Moving {img} to {os.path.join(test_img_dir, os.path.basename(img))}")
        shutil.move(img, os.path.join(test_img_dir, os.path.basename(img)))
        print(f"Moving {ann} to {os.path.join(test_ann_dir, os.path.basename(ann))}")
        shutil.move(ann, os.path.join(test_ann_dir, os.path.basename(ann)))

    print("Images and labels sorted into training, validation, and test sets.")
    
def validate_directory(directory):
    print(f"Validating directory: {directory}")
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)
    print(f"Directory {directory} is valid.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python prepyolo.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    validate_directory(directory)
    sortImagesAndAnnotations(directory)
