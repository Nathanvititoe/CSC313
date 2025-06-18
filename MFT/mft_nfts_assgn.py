import os
import stat
import getpass
from datetime import datetime

# two real directory paths to combine, create MFT
DIR_1 = "/mnt/c/Users/Nathan Vititoe/OneDrive/Pictures/backgrounds" # full of pictures
DIR_2 = "mnt/c/Users/Nathan Vititoe/OneDrive/Documents/Resumes" # pdfs/word files

# class to simulate Master File Table (MFT) in a New Technology File System (NFTS)
class MFTSim:
    # init class attributes for file properties
    def __init__(self, path):
        # properties/permissions
        self.filename = os.path.basename(path) # get file name from path
        self.filetype = os.path.splitext(self.filename)[1][1:].lower() # get file type from extension
        self.location = path # get path
        self.owner = getpass.getuser() # sim file ownership
        self.is_system = self.filename.startswith('$') # sim sys files
        self.is_hidden = self.filename.startswith('.') # check file name for hidden files (.___)
        self.is_readonly = not os.access(path, os.W_OK) # check file permissions
        self.permissions = stat.filemode(os.stat(path).st_mode) # get file permission str

        stats = os.stat(path) # get file metadata (size, timestamps)

        # timestamps
        self.created = datetime.fromtimestamp(stats.st_ctime) # get created timestamp (NFTS)
        self.modified = datetime.fromtimestamp(stats.st_mtime) # get last modified timestamp
        self.accessed = datetime.fromtimestamp(stats.st_atime) # get last accessed timestamp

        # sizes
        self.logical_size = stats.st_size # get actual file size in bytes

        # physical size rounded to nearest multiple of 4096 bytes
        self.physical_size = ((stats.st_size + 4095) // 4096) * 4096  

    # method to output file details as a string
    def __str__(self):
        return (
            f"Filename: {self.filename}\n"
            f"Location: {self.location}\n"
            f"Owner: {self.owner}\n"
            f"System: {self.is_system}\n"
            f"Hidden: {self.is_hidden}\n"
            f"Read-Only: {self.is_readonly}\n"
            f"Permissions: {self.permissions}\n"
            f"Created: {self.format_timestamp(self.created)}\n"
            f"Modified: {self.format_timestamp(self.modified)}\n"
            f"Accessed: {self.format_timestamp(self.accessed)}\n"
            f"Logical Size: {self.logical_size} bytes\n"
            f"Physical Size: {self.physical_size} bytes"
        )
    
    def format_timestamp(self, ts):
        # Format timestamps for human readability
        return ts.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]  # only two decimals for ms

# walk tree to find directory, list files in that directory
def scan_directory(path):
    entries = []
    # iterate through files and look for the "path/filename"
    for root, _, files in os.walk(path):
        for file in files:
            try:
                full_path = os.path.join(root, file) # get file full path
                entry = MFTSim(full_path) # create an entry in MFT table for file
                entries.append(entry) # add entry to list
            except Exception as e:
                # skip files that throw exceptions
                continue
    return entries # return files from the given directory

# return list of MFT entries that match the given filename
def find_file(mft, item):
    matches = [] # init list
    # search mft for item
    for entry in mft:
        if entry.filename == item or entry.location == item:
            matches.append(entry)
    return matches

# main logic
def main():
    # combine directories to create table
    mft = scan_directory(DIR_1) + scan_directory(DIR_2)

    # input loop
    while True:
        print("\nOptions:\n1. Search for a file\n2. Print full MFT (sorted)\n3. Exit")
        choice = input("Choice: ").strip()

        if choice == '1':
            name = input("Enter filename or path: ").strip()
            results = find_file(mft, name) # find file
            
            # output search results
            if results:
                for entry in results:
                    print("\n" + str(entry))
            else:
                print("File not found.")

        elif choice == '2':
            # loop MFT and print all filenames sorted alphabetically
            for entry in sorted(mft, key=lambda e: e.filename.lower()):
                print("\n" + str(entry))
        # exit
        elif choice == '3':
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
