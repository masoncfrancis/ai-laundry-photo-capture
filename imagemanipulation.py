from PIL import Image
import os
import shutil


def rename_images(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    if not files:
        print("No jpg files found in the directory.")
        return

    file_data = []
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            # Try to extract timestamp from filename
            parts = file.split('_')
            if len(parts) > 1 and parts[1].split('.')[0].isdigit():
                timestamp = int(parts[1].split('.')[0])
            else:
                # Fallback to file creation time
                creation_time = os.path.getctime(file_path)
                if creation_time:
                    timestamp = int(creation_time)
                else:
                    print(f"Skipping file with no valid timestamp: {file}")
                    continue
            file_data.append((file, timestamp))
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    # Sort files by timestamp
    file_data.sort(key=lambda x: x[1])

    # Rename files to temporary names to avoid conflicts
    temp_names = []
    for i, (filename, _) in enumerate(file_data):
        temp_name = f"temp_{i + 1}.jpg"
        os.rename(os.path.join(directory, filename), os.path.join(directory, temp_name))
        temp_names.append(temp_name)

    # Rename temporary files to final names
    for i, temp_name in enumerate(temp_names):
        new_name = f"{i + 1}.jpg"
        os.rename(os.path.join(directory, temp_name), os.path.join(directory, new_name))
        print(f"Renamed {temp_name} to {new_name}")

def label_images(directory):
    labels = {}
    existing_labels = {}

    # Read existing labels to avoid duplicates
    labels_file_path = os.path.join(directory, 'labels.txt')
    if os.path.exists(labels_file_path):
        with open(labels_file_path, 'r') as f:
            for line in f:
                filename, label = line.strip().split(': ')
                existing_labels[filename] = label

    while True:
        try:
            start = int(input("Enter the start of the range (or -1 to finish): "))
            if start == -1:
                break
            if start < 1:
                print("Invalid input. Please enter a positive number.")
                continue
            end = int(input("Enter the end of the range: "))
            if end < start:
                print("Invalid input. End of the range must be greater than or equal to the start.")
                continue
            label = input("Enter the label (y/n/s/r for yes/no/stopped/running): ").strip().lower()
            if label not in ['y', 'n', 's', 'r']:
                print("Invalid label. Please enter 'y', 'n', 's', or 'r'.")
                continue

            # Map short labels to full labels
            label_mapping = {'y': 'yes', 'n': 'no', 's': 'stopped', 'r': 'running'}
            full_label = label_mapping[label]

            for i in range(start, end + 1):
                filename = f"{i}.jpg"
                file_path = os.path.join(directory, filename)
                if os.path.exists(file_path):
                    labels[filename] = full_label
                else:
                    print(f"File {filename} does not exist. Skipping.")
        except ValueError:
            print("Invalid input. Please enter numeric values for the range.")

    # Append labels to a file
    with open(labels_file_path, 'w') as f:  # Overwrite the file to ensure updated labels
        for filename, label in {**existing_labels, **labels}.items():
            f.write(f"{filename}: {label}\n")
    print("Labels updated in labels.txt")

def sort_labeled_files(directory):
    # Create folders for all labels
    yes_folder = os.path.join(directory, 'yes')
    no_folder = os.path.join(directory, 'no')
    stopped_folder = os.path.join(directory, 'stopped')
    running_folder = os.path.join(directory, 'running')
    
    os.makedirs(yes_folder, exist_ok=True)
    os.makedirs(no_folder, exist_ok=True)
    os.makedirs(stopped_folder, exist_ok=True)
    os.makedirs(running_folder, exist_ok=True)

    labels_file = os.path.join(directory, 'labels.txt')
    if not os.path.isfile(labels_file):
        print(f"Error: {labels_file} does not exist.")
        sys.exit(1)

    with open(labels_file, 'r') as f:
        for line in f:
            filename, label = line.strip().split(': ')
            src = os.path.join(directory, filename)
            
            # Determine the destination folder based on the label
            if label == 'yes':
                dst = os.path.join(yes_folder, filename)
            elif label == 'no':
                dst = os.path.join(no_folder, filename)
            elif label == 'stopped':
                dst = os.path.join(stopped_folder, filename)
            elif label == 'running':
                dst = os.path.join(running_folder, filename)
            else:
                print(f"Unknown label '{label}' for file {filename}. Skipping.")
                continue
            
            # Move the file to the appropriate folder
            if os.path.exists(src):
                shutil.move(src, dst)
                print(f"Moved {filename} to {label} folder")
            else:
                print(f"File {filename} does not exist. Skipping.")

def resave_images_as_jpeg(directory):
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.bmp', '.gif', '.tiff', '.jpg', '.jpeg'))]
    if not files:
        print("No image files found in the directory.")
        return

    errors = []
    for filename in files:
        file_path = os.path.join(directory, filename)
        try:
            with Image.open(file_path) as img:
                new_filename = os.path.splitext(filename)[0] + '.jpg'
                new_file_path = os.path.join(directory, new_filename)
                img.convert('RGB').save(new_file_path, 'JPEG')
                print(f"Converted {filename} to {new_filename}")
        except Exception as e:
            error_message = f"Failed to convert {filename}: {e}"
            print(error_message)
            errors.append(error_message)
    
    if errors:
        print("\nErrors occurred during the conversion process:")
        for error in errors:
            print(error)

def crop_washer_image_directory(directory):
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.bmp', '.gif', '.tiff', '.jpg', '.jpeg'))]
    if not files:
        print("No image files found in the directory.")
        return

    for filename in files:
        file_path = os.path.join(directory, filename)
        crop_washer_image_percentage(file_path)

def crop_washer_image_percentage(image_path):
    left_percent = 0.625  
    top_percent = 0.35   
    right_percent = 0.745 
    bottom_percent = 0.5 

    try:
        img = Image.open(image_path)
        width, height = img.size

        left = int(width * left_percent)
        top = int(height * top_percent)
        right = int(width * right_percent)
        bottom = int(height * bottom_percent)


        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(image_path)
        print(f"Image cropped and saved to {image_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_yolo_text_files(directory):
    try:
        start = int(input("Enter the start of the range: "))
        end = int(input("Enter the end of the range: "))
        content = input("Enter the contents for the YOLO text files: ").strip()

        for i in range(start, end + 1):
            filename = f"{i}.jpg"
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                text_filename = os.path.splitext(filename)[0] + '.txt'
                text_file_path = os.path.join(directory, text_filename)
                with open(text_file_path, 'w') as f:
                    f.write(content)
                print(f"Generated {text_filename} with provided content.")
            else:
                print(f"File {filename} does not exist. Skipping.")

    except ValueError:
        print("Invalid input. Please enter numeric values for the range.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# rename_images('/path/to/your/directory')

if __name__ == "__main__":
    import sys

    # accept directory path from user as argument when running script
    if len(sys.argv) != 2:
        print("Usage: python imagemanipulation.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    choice = input("Do you want to renumber the files, label them, sort labeled files, crop washer images, resave images as JPEGs, or generate YOLO text files? (renumber/label/sort/cropwasher/resave/generateyolo): ").strip().lower()
    if choice == "renumber":
        rename_images(directory)
    elif choice == "label":
        label_images(directory)
    elif choice == "sort":
        sort_labeled_files(directory)
    elif choice == "resave":
        resave_images_as_jpeg(directory)
    elif choice == "cropwasher":
        crop_washer_image_directory(directory)
    elif choice == "generateyolo":
        generate_yolo_text_files(directory)
    else:
        print("Invalid choice. Please enter 'renumber', 'label', 'sort', 'cropwasher', 'resave', or 'generateyolo'.")
        sys.exit(1)