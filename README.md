# PYTHON:
Make sure you have a backup of your spreadsheets before running any these scripts. You will have to edit the location of your files on your PC in the scripts. Make sure you understand what these scripts are doing before you run them on your PC.

## The following scripts use PANDAS:

- **COMPARE-SPREADSHEET&DIRECTORY.py** Compares files listed in an Excel column against files in a directory tree and writes the report to a text file. Use the default "Sheet1" (which is 0, or start with a fresh spreadsheet) and make sure there is a header "Filename" in your spreadsheet.
- **COMPARE-SPREADSHEET&DIRECTORY-REVISE.py** Compares files listed in an Excel colum with the header "Filename" against files in a directory tree, updates near-matches in the spreadsheet, and writes the report.
- **REFORMAT-XLS_TO_JSTOR.py** This takes a spreadsheet that contains some of the headers found in the JSTOR spreadsheet template and fills in the others. The output is a CSV file to avoid XLSX glitches. Just open the CSV and convert to XLSX.

## The following scripts use PANDAS and NUMPY:

- **MERGE-TOC&DIR_SPREADSHEETS.py** Merges a spreadsheet based on a table of contents (e.g., title, author, first page, last page) with a spreadsheet that contains other related information about the items (e.g., filename, keywords, author last name, page range) from a directory of PDFs.

# POWERSHELL COMMANDS:

## edit folder names in a directory to replace spaces with underscores:

`Get-ChildItem -Directory -Recurse | Where-Object Name -like "* *" | Sort-Object FullName -Descending | Rename-Item -NewName { $_.Name -replace ' ', '_' }`

## edit filenames in a directory to replace spaces with underscores:

`Get-ChildItem -File | Where-Object Name -like "* *" | Rename-Item -NewName { $_.Name -replace ' ', '_' }`
