import os
import random
import shutil
import uuid


class FileSystemEmulator:
    def __init__(self, directory, deleted_directory):
        self.directory = directory
        self.deleted_directory = deleted_directory

        # creates the directory and deleted_directory folders if they do not exist.
        try:
            os.makedirs(directory, exist_ok=True)
            os.makedirs(deleted_directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating folders: {e}")

        # removes everything from the directories.
        self.clear_directory(self.directory)
        self.clear_directory(self.deleted_directory)

    # Adds a random sample to the sample's directory. The name is a new UUID with a txt extension.
    def add_random_sample(self):
        new_file_name = f"{uuid.uuid4()}.txt"
        try:
            content = [random.randint(1,3), random.randint(1,3), random.randint(1,3)]
            with open(f"{self.directory}/{new_file_name}", 'w') as file:
                file.write(str(content))
        except IOError as e:
            print(f"Error writing to {self.directory}: {e}")

        return new_file_name

    # Counts and returns the number of files in the sample's directory.
    def read_files(self):
        try:
            files = os.listdir(self.directory)
            return files
        except FileNotFoundError:
            print(f"Directory not found: {self.directory}")
        except Exception as e:
            print(f"Error reading files: {e}")

    # Soft-deletes a file, which means that the file is not deleted, only moved to another directory.
    def soft_delete_file(self, file_name):
        try:
            shutil.move(f"{self.directory}/{file_name}", self.deleted_directory)
            print(f"File moved from '{self.directory}' to '{self.deleted_directory}'")
        except FileNotFoundError:
            print("Source file not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print(f"Error moving file: {e}")

    # Removes everything from a given directory
    def clear_directory(self, directory):
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
        except Exception as e:
            print(f"Error removing contents: {e}")

    # Reads a file and returns its contents as a string
    def read_content(self, file_name):
        try:
            with open(f"{self.directory}/{file_name}", 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except Exception as e:
            print(f"Error reading file: {e}")
