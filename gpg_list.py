#!/bin/python3
import os
import argparse
import sys
import gnupg
from tabulate import tabulate
import csv


def validate_and_sanitize_directory_path(path):
    """
    Validates and Sanitizes a Path
    Args:
        Path (str): Path to check.

    Returns:
        sanitized_path (str): A sanitized path
    """
    sanitized_path = os.path.normpath(path)
    
    # Check if the path exists and is a directory
    if not os.path.exists(sanitized_path):
        raise FileNotFoundError(f"Error: The path '{sanitized_path}' does not exist.")
    if not os.path.isdir(sanitized_path):
        raise NotADirectoryError(f"Error: The path '{sanitized_path}' is not a directory.")
    
    return sanitized_path

def list_all_files(directory, recursive=True):
    """
    List all files in a directory.

    Args:
        directory (str): Path to the directory.
        recursive (bool): Whether to include files in subdirectories.

    Returns:
        list: List of file paths.
    """
    files = []
    if recursive:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    else:
        # Non-recursive: List only files in the specified directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                files.append(file_path)
    return files

def get_encrypted_recipient(file_path):
    """
    Check the recipient of a file. 
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        bool: Returns the public key id if the file is encrypted, Returns nothing if it is not encrypted
    """
    gpg = gnupg.GPG()
    
    try:
        with open(file_path, 'rb') as f:
            ## Check to see if the file has an GPG recipients
            result = gpg.get_recipients_file(f)

            # If there is recipients get the value out of the array if not set the result to none
            result = result[0] if result else None

            return result
    except Exception as e:
        print(f"Error checking file: {e}")
        return False

def write_array_to_csv(data, headers, output_file, allow_clobber):
    """
    Writes an array of arrays to a CSV file.

    Args:
        data (list of list): The data to write to the CSV, where each sub-list is a row.
        headers (list): A list of column headers, must match the size of each row in `data`.
        output_file (str): The path to the output CSV file.
        allow_clobber (bool): Whether to overwrite the file if it already exists.

    Returns:
        bool: True if the file was written successfully, False otherwise.
    """
    try:
        # Validate input
        if not all(len(row) == len(headers) for row in data):
            raise ValueError("All rows in data must be the same size as the headers.")

        # Check if file exists and handle clobbering
        if os.path.exists(output_file) and not allow_clobber:
            raise FileExistsError(f"The file '{output_file}' already exists and clobbering is not allowed.")

        # Write to CSV
        with open(output_file, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)  # Write headers
            writer.writerows(data)    # Write data

        print(f"File successfully written to {output_file}")
        return True

    except FileExistsError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return False

def main():

    ## Lets get our args here before we pass them into main
    parser = argparse.ArgumentParser(description="Checks a Directory And Looks for any GPG encrypted files")
    parser.add_argument("-d", "--directory",help="The directory to check", required=True)
    parser.add_argument("-r", "--recursive", action="store_true", 
                        help="Enable recursive processing of files.")
    parser.add_argument("-s", "--supress_output", action="store_true", 
                        help="Does not output table to StdOut")
    parser.add_argument("-o", "--out_file",help="The path to where to save the CSV file")
    parser.add_argument("-a", "--allow_clobber", action="store_true", 
                        help="If writing output to a file allow clober")
    args = parser.parse_args()

    # Validation logic for the args
        # If you supress output to the terminal you have to set an outfile
    if args.supress_output and not args.out_file:
        print("Error: The -s/--supress_output flag requires the -o/--out_file flag to be set.")
        sys.exit(1)
        # If you allow clobber you have to be saving to an outfile
    if args.allow_clobber and not args.out_file:
        print("Error: The -a/--allow_clobber flag requires the -o/--out_file flag to be set.")
        sys.exit(1)

    # Set some of our constants that come from the args
    RECURSIVE = args.recursive
    SUPRESS = args.supress_output
    ALLOW_CLOBBER = args.allow_clobber
    PATH_TO_CHECK = validate_and_sanitize_directory_path(args.directory)
    OUTFILE_PATH = args.out_file
    

    # Get our list of files to check 
    files_to_check = list_all_files(PATH_TO_CHECK, RECURSIVE)


    # Array of file results 
    result_array = []
    # Interate through our files and see if they are encrypted
    for file in files_to_check:
        recipient = get_encrypted_recipient(file)
        is_encrypted = True if recipient else False
        result_array.append([file,recipient,is_encrypted])

    headers=["File Path","Recipient UID", "Is Encrypted"]

    # Print the table if we don't supress the output 
    if(not SUPRESS):
        print(tabulate(result_array, headers))
    if(OUTFILE_PATH):
        write_array_to_csv(result_array, headers, OUTFILE_PATH, ALLOW_CLOBBER)

if __name__ == "__main__":
    main()
