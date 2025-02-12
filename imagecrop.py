import cv2
import numpy as np

# 1. Contour Approximation Method
def crop_around_black_control_panel(image_path, padding=10):
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_area = 0
        largest_contour = None

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_contour = contour

        if largest_contour is not None:
            epsilon = 0.02 * cv2.arcLength(largest_contour, True)  # Adjust epsilon as needed
            approx_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

            x, y, w, h = cv2.boundingRect(approx_contour)

            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(img.shape[1], x + w + padding)
            y2 = min(img.shape[0], y + h + padding)

            cropped_img = img[y1:y2, x1:x2]
            return cropped_img, (x1, y1, x2, y2)
        else:
            return None, None

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


# 2. Rotated Bounding Box Method
def crop_around_black_control_panel_rotated(image_path, padding=10):
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_area = 0
        largest_contour = None

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_contour = contour

        if largest_contour is not None:
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            box = box.astype(int)  # Correct way to convert to integers

            x_coords = box[:, 0]
            y_coords = box[:, 1]
            x1 = np.min(x_coords)
            y1 = np.min(y_coords)
            x2 = np.max(x_coords)
            y2 = np.max(y_coords)

            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(img.shape[1], x2 + padding)
            y2 = min(img.shape[0], y2 + padding)

            cropped_img = img[y1:y2, x1:x2]

            return cropped_img, (x1, y1, x2, y2)
        else:
            return None, None

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Example Usage (Both Methods):

image_path = "input_image.jpg"  # Replace with your image path

# Contour Approximation
cropped_image_approx, coordinates_approx = crop_around_black_control_panel(image_path, padding=20)

if cropped_image_approx is not None:
    original_image_approx = cv2.imread(image_path)
    if coordinates_approx:
        x1, y1, x2, y2 = coordinates_approx
        cv2.rectangle(original_image_approx, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imshow("Bounding Box Preview (Approx)", original_image_approx)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imshow("Cropped Image (Approx)", cropped_image_approx)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("cropped_output_approx.jpg", cropped_image_approx)
    print(f"Cropped image (Approx) saved to cropped_output_approx.jpg")
    print(f"Cropping coordinates (Approx): {coordinates_approx}")


# Rotated Bounding Box
cropped_image_rotated, coordinates_rotated = crop_around_black_control_panel_rotated(image_path, padding=20)

if cropped_image_rotated is not None:
    original_image_rotated = cv2.imread(image_path)
    if coordinates_rotated:
        x1, y1, x2, y2 = coordinates_rotated
        cv2.rectangle(original_image_rotated, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imshow("Bounding Box Preview (Rotated)", original_image_rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imshow("Cropped Image (Rotated)", cropped_image_rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("cropped_output_rotated.jpg", cropped_image_rotated)
    print(f"Cropped image (Rotated) saved to cropped_output_rotated.jpg")
    print(f"Cropping coordinates (Rotated): {coordinates_rotated}")