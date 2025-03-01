import cv2
import numpy as np
import argparse

def draw_yolo_box(image_path, label_path):
    # Load the image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    # Create a copy for drawing
    annotated_image = image.copy()
    
    # Read the YOLO annotation file
    with open(label_path, 'r') as f:
        for line in f:
            # Parse YOLO format: class x_center y_center width height
            class_id, x, y, w, h = map(float, line.split())
            
            # Convert normalized coordinates to pixels
            x_pixels = int(x * width)
            y_pixels = int(y * height)
            w_pixels = int(w * width)
            h_pixels = int(h * height)
            
            # Calculate top-left and bottom-right corners
            x1 = max(0, int(x_pixels - w_pixels / 2))
            y1 = max(0, int(y_pixels - h_pixels / 2))
            x2 = min(width - 1, int(x_pixels + w_pixels / 2))
            y2 = min(height - 1, int(y_pixels + h_pixels / 2))
            
            # Draw the bounding box
            cv2.rectangle(
                annotated_image,
                (x1, y1),
                (x2, y2),
                color=(0, 255, 0),  # Green color
                thickness=2
            )
            
            # Add class label
            cv2.putText(
                annotated_image,
                f'Class {int(class_id)}',
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
    
    return annotated_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw YOLO bounding boxes on an image.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("label_path", type=str, help="Path to the YOLO label file.")
    args = parser.parse_args()

    result = draw_yolo_box(args.image_path, args.label_path)
    cv2.imwrite("annotated_image.jpg", result)