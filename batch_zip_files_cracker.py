import os
import zipfile
import sys
import argparse

def read_and_validate_args():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Batch zip files cracker')

    # Add the arguments
    my_parser.add_argument('-s',
                           '--source_folder',
                           type=str,
                           required=True,
                           help='the source folder to search zip files')
    my_parser.add_argument('-p',
                           '--pattern',
                           type=str,
                           required=True,
                           help='the pattern of zip files')
    my_parser.add_argument('-d',
                           '--dictionaries_folder',
                           type=str,
                           required=True,
                           help='the password dictionaries')
    my_parser.add_argument('-t',
                           '--target_folder',
                           type=str,
                           required=True,
                           help='the target folder for unzipped files')

    # Execute parse_args()
    args = my_parser.parse_args()
    source_folder = args.source_folder
    pattern = args.pattern
    dictionaries_folder = args.dictionaries_folder
    target_folder = args.target_folder

    # Check each arg
    if not os.path.isdir(source_folder):
        print('The source_folder specified does not exist')
        sys.exit()

    if not os.path.isdir(dictionaries_folder):
        print('The dictionaries_folder specified does not exist')
        sys.exit()
    
    if not os.path.isdir(target_folder):
        print('The target_folder specified does not exist')
        sys.exit()

    print(f"""
        Folder: {source_folder}
        Pattern: {pattern}
        Dictionaries_folder: {dictionaries_folder}
        Target_folder: {target_folder}
    """)

    return source_folder,pattern,dictionaries_folder,target_folder

def get_matched_zip_file(source_folder, pattern):
    matched_zip_files_list = []

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".zip"):
                print(f"Found a zip file: {file}")
                if pattern in file:
                    # Generate the full path of the file
                    zip_file_full_path = os.path.join(root, file)
                    print(f"Found a zip file that matches the pattern '{pattern}': {zip_file_full_path}")
                    matched_zip_files_list.append(zip_file_full_path)
            else:
                print(f"{file} is not a zip file, skip...")

    if len(matched_zip_files_list) == 0:
        print(f"Cannot find any zip files that match pattern {pattern} under folder {source_folder}, exit...")
        sys.exit()
    else:
        print(f"Found {len(matched_zip_files_list)} zip files:")
        print(matched_zip_files_list)

    return matched_zip_files_list

def get_password_files(dictionaries_folder):
    # File all password dictionary files
    password_files_list = []

    for root, dirs, files in os.walk(dictionaries_folder):
        for file in files:
            # Assume all the password dictionary files are txt files
            if file.endswith(".txt"):
                print(f"Found a dictionary file: {file}")
                # Generate the full path of the file
                password_file_full_path = os.path.join(root, file)
                password_files_list.append(password_file_full_path)
            else:
                print(f"{file} is not a password txt file, skip...")


    if len(password_files_list) == 0:
        print(f"Cannot find any password dictionary files under folder {dictionaries_folder}, exit...")
        sys.exit()
    else:
        print(f"Found {len(password_files_list)} dictionary files:")
        print(password_files_list)

    return password_files_list

def get_passwords(password_files_list):
    # Read all password into a list
    passwords_list = []

    print("Reading all the passwords to a list...")

    for password_file in password_files_list:
        with open(password_file) as file:
            for line in file: 
                # Strip whitespace
                line = line.strip()
                passwords_list.append(line)

    if len(passwords_list) == 0:
        print(f"Cannot find any password in the dictionary files, exit...")
        sys.exit()
    else:
        print(f"Found {len(passwords_list)} passwords in dictionary files:")
        print(passwords_list)

    return passwords_list

def batch_crack_zip_files(matched_zip_files_list, passwords_list, target_folder):
    cracked_zip_files_list = []
    is_successful = False

    for zip_file_name in matched_zip_files_list:
        zip_file = zipfile.ZipFile(zip_file_name)
        is_successful = False
        for password in passwords_list:
            try:
                print(f"Cracking zip file {zip_file_name} using password `{password}`...")
                # Encode the password as from 
                zip_file.extractall(
                    path=target_folder,
                    pwd=password.encode()
                )

                print(f"Successfully cracked zip file {zip_file_name}!")
                print(f"The password is `{password}`")

                is_successful = True
                cracked_zip_files_list.append(zip_file_name)
            except:
                print(f"Cannot crack zip file {zip_file_name} using password `{password}`, continue...")
                pass
        if not is_successful:
            print(f"All the passwords in the dictionaries have been used, but still cannot crack zip file {zip_file_name}")

    if len(cracked_zip_files_list) == 0:
        print("Bad luck! No zip files can be cracked! Try it next time!")
    else:
        print(f"Congratulations! You have cracked {len(cracked_zip_files_list)} files!")
        print("The files are:")
        for file in cracked_zip_files_list:
            print(file)
        
        print(f"You can file all the extract files under {target_folder} folder!")

if __name__ == '__main__':
    print("Step 1: read and validate all the input arguments \n")
    source_folder, pattern, dictionaries_folder, target_folder = read_and_validate_args()

    print("Step 2: find all zip files that match the given pattern \n")
    matched_zip_files_list = get_matched_zip_file(source_folder, pattern)

    print("Step 3: file all password files from dictionary folder \n")
    password_files_list = get_password_files(dictionaries_folder)

    print("Step 4: extract all password from dictionary files \n")
    passwords_list = get_passwords(password_files_list)

    print("Step 5: crack all the zip files using the passwords from dictionary files \n")
    batch_crack_zip_files(matched_zip_files_list, passwords_list, target_folder)