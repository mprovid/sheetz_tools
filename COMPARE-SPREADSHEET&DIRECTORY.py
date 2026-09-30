from pathlib import Path
import pandas as pd


def audit_file_match(
    excel_path,
    sheet_name,
    column_name,
    directory_path,
    output_txt_path="audit_report.txt",
    match_by_name_only=True,
):
  """Compares files listed in an Excel column against files in a directory tree

  and writes the report to a text file.
  """
  # 1. Read the spreadsheet
  print("Reading Excel file...")
  df = pd.read_excel(excel_path, sheet_name=sheet_name)

  # Extract column data, drop empty rows, convert to string and strip whitespace
  excel_files = set(df[column_name].dropna().astype(str).str.strip())

  # 2. Scan the directory recursively
  print("Scanning directory and subfolders...")
  dir_path = Path(directory_path)

  if match_by_name_only:
    dir_files = set(f.name for f in dir_path.rglob("*") if f.is_file())
  else:
    dir_files = set(
        str(f.relative_to(dir_path)).replace("\\", "/")
        for f in dir_path.rglob("*")
        if f.is_file()
    )

  # 3. Perform set comparisons to find mismatches
  missing_from_dir = excel_files - dir_files
  missing_from_excel = dir_files - excel_files

  # 4. Build the report content
  report_lines = []
  report_lines.append("=" * 50)
  report_lines.append("AUDIT SUMMARY REPORT")
  report_lines.append("=" * 50)
  report_lines.append(f"Total entries in Excel column : {len(excel_files)}")
  report_lines.append(f"Total files found in directory: {len(dir_files)}")

  if not missing_from_dir and not missing_from_excel:
    report_lines.append(
        "\nSuccess! There is a flawless one-to-one match between the"
        " spreadsheet and directory."
    )
  else:
    if missing_from_dir:
      report_lines.append(
          f"\n[!] {len(missing_from_dir)} files listed in Excel but MISSING"
          " from the directory:"
      )
      for f in sorted(missing_from_dir):
        report_lines.append(f"    - {f}")

    if missing_from_excel:
      report_lines.append(
          f"\n[!] {len(missing_from_excel)} files found in the directory but"
          " MISSING from Excel:"
      )
      for f in sorted(missing_from_excel):
        report_lines.append(f"    - {f}")
  report_lines.append("=" * 50)

  # Join all lines into a single text block
  report_text = "\n".join(report_lines)

  # Print to terminal
  print(report_text)

  # Save to text file
  with open(output_txt_path, "w", encoding="utf-8") as f:
    f.write(report_text)

  print(f"\n[+] Report successfully saved to: {Path(output_txt_path).resolve()}")


# --- Configuration ---
EXCEL_FILE = r"C:\Users\ [**PATH TO XLSX OR CSV**] .xlsx"
SHEET_NAME = 0  # Can be an integer (0 for first sheet) or string name
COLUMN_NAME = "Filename"  # Exact name of your column header in Excel
TARGET_DIRECTORY = r"C:\Users\ [**PATH TO DIRECTORY**] "
OUTPUT_FILE = r"C:\Users\ [**PATH TO OUTPUT FILE**] .txt"

# Run the audit
audit_file_match(
    EXCEL_FILE, SHEET_NAME, COLUMN_NAME, TARGET_DIRECTORY, OUTPUT_FILE
)