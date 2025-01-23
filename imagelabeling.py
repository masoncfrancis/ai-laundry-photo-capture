import os
import time
import sys

def rename_images(directory):
    # Get list of jpg files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.jpg')]
    
    # Check if there are no jpg files
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
                labels[f"{i}.jpg"] = label
        except ValueError:
            print("Invalid input. Please enter numeric values for the range.")
    
    # Write labels to a file
    with open(os.path.join(directory, 'labels.txt'), 'w') as f:
        for filename, label in labels.items():
            f.write(f"{filename}: {label}\n")
    print("Labels saved to labels.txt")

# Example usage
# rename_images('/path/to/your/directory')

if __name__ == "__main__":
    # accept directory path from user as argument when running script
    if len(sys.argv) != 2:
        print("Usage: python imagelabeling.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)
    
    rename_images(directory)
    label_images(directory)
