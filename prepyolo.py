import os
import sys
from sklearn.model_selection import train_test_split
import shutil

def verify_annotations(images, annotations):
    image_basenames = {os.path.splitext(os.path.basename(img))[0] for img in images}
    annotation_basenames = {os.path.splitext(os.path.basename(ann))[0] for ann in annotations}
    missing_annotations = image_basenames - annotation_basenames
    if missing_annotations:
        print(f"Error: Missing annotations for images: {', '.join(missing_annotations)}")
        sys.exit(1)

def sortImagesAndAnnotations(directory):
    images = [os.path.join(directory + '/images', x) for x in os.listdir(directory + '/images')]
    annotations = [os.path.join(directory + '/annotations', x) for x in os.listdir(directory + '/annotations') if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    verify_annotations(images, annotations)

    # Split the data into training (80%), validation(10%), and test(10%) sets
    train_images, test_images, train_annotations, test_annotations = train_test_split(images, annotations, test_size=0.2, random_state=42)
    val_images, test_images, val_annotations, test_annotations = train_test_split(test_images, test_annotations, test_size=0.5, random_state=42)

    # Create directories for the training, validation, and test sets
    train_dir = os.path.join(directory, 'train')
    val_dir = os.path.join(directory, 'val')
    test_dir = os.path.join(directory, 'test')

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Move the images and annotations to the appropriate directories
    for img, ann in zip(train_images, train_annotations):
        shutil.move(img, os.path.join(train_dir, os.path.basename(img)))
        shutil.move(ann, os.path.join(train_dir, os.path.basename(ann)))

    for img, ann in zip(val_images, val_annotations):
        shutil.move(img, os.path.join(val_dir, os.path.basename(img)))
        shutil.move(ann, os.path.join(val_dir, os.path.basename(ann)))

    for img, ann in zip(test_images, test_annotations):
        shutil.move(img, os.path.join(test_dir, os.path.basename(img)))
        shutil.move(ann, os.path.join(test_dir, os.path.basename(ann)))

    print("Images and annotations sorted into training, validation, and test sets.")
    



def validate_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python prepyolo.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    validate_directory(directory)
    sortImagesAndAnnotations(directory)
