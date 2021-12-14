# Description

`batch_zip_files_cracker.py` is a command-line program to crack zip files in batch. It requires the Python interpreter, version 3. It has been developed and tested on Windows 10.

# Installation

To install it, you will need to install Python 3 in your Windows 10 matchine. Then copy and save `batch_zip_files_cracker.py` in a folder.

# How to run it

There are a few arguments that are required to pass to the program.

```
-h, --help                 show this help message and exit
-s, --source_folder        the source folder to search zip files
-p, --pattern              the pattern of zip files
-d, --dictionaries_folder  the password dictionaries
-t, --target_folder        the target folder for unzipped files
```

Below is an example:

```
python batch_zip_files_cracker.py -s "C:\Users\Lenovo\Desktop\batch_zip_files_cracker\source" -p important -t "C:\Users\Lenovo\Desktop\batch_zip_files_cracker\target" -d "C:\Users\Lenovo\Desktop\batch_zip_files_cracker\password_dictionary"
```
