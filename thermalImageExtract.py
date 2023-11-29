import fnv
import fnv.reduce
import fnv.file
import os

def process_seq_file(file_path):
    try:
        imager_file = fnv.file.ImagerFile(file_path)
        # Your operations here, e.g., reading frames, processing data
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    finally:
        print('here')
        # Close the file or any other cleanup if needed

def main():
    directory = "path/to/seq/files"
    for filename in os.listdir(directory):
        if filename.endswith(".seq"):
            process_seq_file(os.path.join(directory, filename))

if __name__ == "__main__":
    main()