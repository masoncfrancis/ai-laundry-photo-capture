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
