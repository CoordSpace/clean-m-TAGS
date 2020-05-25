import sys
import os
import json

"""
    Clean up any stray mtag files or empty directories in your music collection.

    Usage: python clean_mtags.py "\mtag\path"

"""


to_delete = False
deleted = []


def main():
    if len(sys.argv) != 2:
        print("Incorrect arguments. \nUsage: python clean_mtags.py \"path_to_mtags\"")
        exit()

    for root, directories, files in os.walk(sys.argv[1]):
        for name in files:
            to_delete = False
            file = os.path.join(root, name)
            if name[-5:] == ".tags":
                with open(file, newline='', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    # Check if this is a valid mtag file
                    if len(data) > 0:
                        # Is the media this tag points at still there?
                        if os.path.isfile(data[0]['@'][1:]):
                            to_delete = False
                        else:
                            to_delete = True
                    else:
                        to_delete = True
            if to_delete:
                print("Deleted File: " + file)
                os.remove(file)
                deleted.append(file)

    for root, directories, files in os.walk(sys.argv[1]):
        for directory in directories:
            folder_path = os.path.join(root, directory)
            if len(os.listdir(folder_path)) == 0:
                os.rmdir(folder_path)
                print("Deleting Directory: " + folder_path)

    print("Done!")


if __name__ == "__main__":
    main()