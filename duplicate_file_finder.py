import os
import hashlib

# Function to calculate the hash of a file (MD5 checksum)
def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to find duplicate files in a given directory
def find_duplicates(directory):
    file_hashes = {}
    duplicates = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)

            # If the hash is already in the dictionary, it's a duplicate
            if file_hash in file_hashes:
                duplicates.append((file_hashes[file_hash], file_path))
            else:
                file_hashes[file_hash] = file_path

    return duplicates

# Function to display duplicates
def display_duplicates(duplicates):
    if not duplicates:
        print("No duplicate files found.")
    else:
        print("Duplicate files found:")
        for original, duplicate in duplicates:
            print(f"Original: {original}")
            print(f"Duplicate: {duplicate}")
            print("-" * 50)

# Main function to execute the script
def main():
    # Specify the directory to scan for duplicate files
    directory = input("Enter the directory path to search for duplicates: ")

    if not os.path.exists(directory):
        print("The specified directory does not exist. Please try again.")
        return

    print(f"Searching for duplicates in: {directory}")
    duplicates = find_duplicates(directory)
    display_duplicates(duplicates)

if __name__ == "__main__":
    main()
