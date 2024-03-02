import shutil
import re
import os
import threading
import tqdm

SUBSTITUTES = {os.getcwd(): ""}
with open("substitutes.txt", 'r') as substitute_file:
    for match_line in substitute_file.readlines():
        substitute = re.findall(r'(.*)=(.*)', match_line)
        if len(substitute[0]) == 2:
            SUBSTITUTES[substitute[0][0]] = substitute[0][1]

def find_replace(file_path, lookup_dict):
    """
    Function to perform find and replace in a file using a lookup dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for key, value in lookup_dict.items():
        content = content.replace(key, value)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def copy_file(file, source_dir, root, dest_dir):
    
    if file.endswith('.kicad_sym') or file.endswith('.kicad_mod') or file.endswith('.stp') or file.endswith('.step'):
        # print(f"copying file... {os.path.basename(source_file)}")

        source_file = os.path.join(root, file)
        relative_path = os.path.relpath(source_file, source_dir)
        dest_file = os.path.join(dest_dir, relative_path)
        dest_dirname = os.path.dirname(dest_file)
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest_dirname, exist_ok=True)

        # Copy file
        shutil.copyfile(source_file, dest_file)
        
        if file.endswith('.kicad_sym') or file.endswith('.kicad_mod') :
            # Perform find and replace
            find_replace(dest_file, SUBSTITUTES)

def copy_directory(threads, source_dir, dest_dir, root, dirs, files):
    for file in files:
        thread = threading.Thread(target=copy_file, args=(file, source_dir, root, dest_dir))
        threads.append(thread)

def copy_modify_files(source_dir, dest_dir):
    """
    Function to copy *.kicad_sym and *.kicad_mod files from source directory to destination directory,
    retaining the folder structure and performing find and replace using a lookup dictionary.
    """
    threads = []
    for root, dirs, files in os.walk(source_dir):
        thread = threading.Thread(target=copy_directory, args=(threads, source_dir, dest_dir, root, dirs, files))
        threads.append(thread)
            # copy_file(file, source_dir, root, dest_dir)
        
    for thread in tqdm.tqdm(threads, desc="starting reads"):
        thread.start()
    
    for thread in tqdm.tqdm(threads):
        thread.join()

if __name__ == "__main__":
    # Define source directory, destination directory, and lookup dictionary
    source_directory = "kicad-latest"
    destination_directory = "temp"

    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)

    copy_modify_files(source_directory, destination_directory)