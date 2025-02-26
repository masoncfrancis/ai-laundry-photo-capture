from PIL import Image


def crop_image_percentage(image_path, left_percent, top_percent, right_percent, bottom_percent, output_path):
    try:
        img = Image.open(image_path)
        width, height = img.size

        left = int(width * left_percent)
        top = int(height * top_percent)
        right = int(width * right_percent)
        bottom = int(height * bottom_percent)


        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(output_path)
        print(f"Image cropped and saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Example using percentages:
    image_path = "input_image.jpg"
    left_percent = 0.625  
    top_percent = 0.35   
    right_percent = 0.745 
    bottom_percent = 0.5 
    output_path = "cropped_image_percentage.jpg"

    crop_image_percentage(image_path, left_percent, top_percent, right_percent, bottom_percent, output_path)
