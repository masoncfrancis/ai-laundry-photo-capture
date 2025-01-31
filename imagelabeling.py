import os
import shutil
from PIL import Image

def rename_images(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    if not files:
        print("No jpg files found in the directory.")
        return
    
    # Sort files by the timestamp in their filenames
    files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    # Rename files
    for i, filename in enumerate(files):
        new_name = f"{i + 1}.jpg"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
        print(f"Renamed {filename} to {new_name}")

def label_images(directory):
    labels = {}
    existing_labels = set()
    
    # Read existing labels to avoid duplicates
    labels_file_path = os.path.join(directory, 'labels.txt')
    if os.path.exists(labels_file_path):
        with open(labels_file_path, 'r') as f:
            for line in f:
                filename = line.split(':')[0].strip()
                existing_labels.add(filename)
    
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
            label = input("Enter the label (yes/no): ").strip().lower()
            if label not in ['yes', 'no']:
                print("Invalid label. Please enter 'yes' or 'no'.")
                continue
            for i in range(start, end + 1):
                filename = f"{i}.jpg"
                if filename not in existing_labels:
                    labels[filename] = label
                    existing_labels.add(filename)
        except ValueError:
            print("Invalid input. Please enter numeric values for the range.")
    
    # Append labels to a file
    with open(labels_file_path, 'a') as f:
        for filename, label in labels.items():
            f.write(f"{filename}: {label}\n")
    print("Labels appended to labels.txt")

def sort_labeled_files(directory):
    yes_folder = os.path.join(directory, 'yes')
    no_folder = os.path.join(directory, 'no')
    os.makedirs(yes_folder, exist_ok=True)
    os.makedirs(no_folder, exist_ok=True)

    labels_file = os.path.join(directory, 'labels.txt')
    if not os.path.isfile(labels_file):
        print(f"Error: {labels_file} does not exist.")
        sys.exit(1)

    with open(labels_file, 'r') as f:
        for line in f:
            filename, label = line.strip().split(': ')
            src = os.path.join(directory, filename)
            if label == 'yes':
                dst = os.path.join(yes_folder, filename)
            elif label == 'no':
                dst = os.path.join(no_folder, filename)
            else:
                continue
            shutil.move(src, dst)
            print(f"Moved {filename} to {label} folder")

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

# Example usage
# rename_images('/path/to/your/directory')

if __name__ == "__main__":
    import sys

    # accept directory path from user as argument when running script
    if len(sys.argv) != 2:
        print("Usage: python imagelabeling.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    choice = input("Do you want to renumber the files, label them, sort labeled files, or resave images as JPEGs? (renumber/label/sort/resave): ").strip().lower()
    if choice == "renumber":
        rename_images(directory)
    elif choice == "label":
        label_images(directory)
    elif choice == "sort":
        sort_labeled_files(directory)
    elif choice == "resave":
        resave_images_as_jpeg(directory)
    else:
        print("Invalid choice. Please enter 'renumber', 'label', 'sort', or 'resave'.")
        sys.exit(1)