# GPG File Checker

A Python script to check directories for GPG-encrypted files and generate reports.

## Features

- Recursively or non-recursively checks directories for files.
- Detects GPG-encrypted files and their recipients.
- Outputs results as a table or saves to a CSV file.

## Requirements

- Python 3.6+
- Required libraries: `gnupg` and `tabulate`.

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 

`python script.py -d <directory_path> [-r] [-s] [-o <output_file>] [-a]`

Arguments:
- `-d, --directory: (Required) The directory to scan.`
- `-r, --recursive: Enable recursive file scanning.`
- `-s, --supress_output: Suppress terminal output (useful when writing to a file).`
- `-o, --out_file: Path to save the CSV file.`
- `-a, --allow_clobber: Allow overwriting existing output files.`

## Example 
`python script.py -d ./files -r -o results.csv -a`

### Result 

A Csv file is created and a table is printed to StdOut

```
File Path                      Recipient UID     Is Encrypted
-----------------------------  ----------------  --------------
encrypted_files/file4.txt                        False
encrypted_files/file5.txt                        False
encrypted_files/file6.txt                        False
encrypted_files/file8.txt                        False
encrypted_files/file9.txt                        False
encrypted_files/file1.txt.gpg  92462E476CCBC7D7  True
encrypted_files/file2.txt.gpg  92462E476CCBC7D7  True
encrypted_files/file3.txt.gpg  92462E476CCBC7D7  True
```
