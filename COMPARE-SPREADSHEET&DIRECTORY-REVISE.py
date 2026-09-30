from pathlib import Path
import pandas as pd


def audit_file_match(
    excel_path,
    sheet_name,
    column_name,
    directory_path,
    output_txt_path="audit_report.txt",
    match_by_name_only=True,
    update_excel=True,
):
  """Compares files listed in an Excel column against files in a directory tree,

  safely updates near-matches in the spreadsheet, and writes the report.
  """
  # 1. Resolve the actual sheet name safely (handles integer indices like 0)
  print("Reading Excel file...")
  xls = pd.ExcelFile(excel_path)
  if isinstance(sheet_name, int):
    actual_sheet_name = xls.sheet_names[sheet_name]
  else:
    actual_sheet_name = sheet_name
  xls.close()

  # Read the spreadsheet using the resolved sheet name
  df = pd.read_excel(excel_path, sheet_name=actual_sheet_name)

  # Clean up column names (strip whitespace)
  df.columns = df.columns.astype(str).str.strip()

  # Handle case-insensitive search for the target column
  actual_column = column_name
  if column_name not in df.columns:
    matched_cols = [c for c in df.columns if c.lower() == column_name.lower()]
    if matched_cols:
      actual_column = matched_cols[0]
      print(f"[Note] Using column '{actual_column}' (case-insensitive match).")
    else:
      print(f"[Error] Column '{column_name}' not found in Excel spreadsheet.")
      print(f"Available columns are: {list(df.columns)}")
      raise KeyError(
          f"Column '{column_name}' does not exist in the Excel file."
      )

  # 2. Scan the directory recursively
  print("Scanning directory and subfolders...")
  dir_path = Path(directory_path)

  if match_by_name_only:
    dir_files_map = {f.name: f.name for f in dir_path.rglob("*") if f.is_file()}
  else:
    dir_files_map = {
        str(f.relative_to(dir_path)).replace("\\", "/"): str(
            f.relative_to(dir_path)
        ).replace("\\", "/")
        for f in dir_path.rglob("*")
        if f.is_file()
    }

  dir_files = set(dir_files_map.keys())

  # Helper function to normalize strings for structural matching
  def normalize_str(s):
    if pd.isna(s):
      return ""
    return "".join(c.lower() for c in str(s) if c.isalnum())

  # Build a lookup map of normalized directory names to actual directory filenames
  norm_dir_map = {normalize_str(f): f for f in dir_files if normalize_str(f)}

  # Track updates made
  updated_rows_count = 0
  excel_files_processed = []

  # 3. Iterate through DataFrame rows to check and fix near-matches
  for idx, val in df[actual_column].items():
    if pd.isna(val):
      continue

    original_val = str(val).strip()

    if original_val in dir_files:
      excel_files_processed.append(original_val)
    else:
      norm_val = normalize_str(original_val)
      if norm_val in norm_dir_map:
        corrected_name = norm_dir_map[norm_val]
        df.at[idx, actual_column] = corrected_name
        excel_files_processed.append(corrected_name)
        updated_rows_count += 1
        print(f"[Auto-Correct] '{original_val}' -> updated to '{corrected_name}'")
      else:
        excel_files_processed.append(original_val)

  excel_files_set = set(excel_files_processed)

  # Save updated Excel file safely using ExcelWriter (preserves other sheets if any)
  if update_excel and updated_rows_count > 0:
    with pd.ExcelWriter(
        excel_path, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
      df.to_excel(writer, sheet_name=actual_sheet_name, index=False)
    print(
        f"[+] Successfully updated {updated_rows_count} filename(s) in Excel"
        f" sheet '{actual_sheet_name}'"
    )

  # 4. Perform set comparisons to find remaining mismatches
  missing_from_dir = excel_files_set - dir_files
  missing_from_excel = dir_files - excel_files_set

  # 5. Build the report content
  report_lines = []
  report_lines.append("=" * 50)
  report_lines.append("AUDIT SUMMARY REPORT")
  report_lines.append("=" * 50)
  report_lines.append(f"Total entries in Excel column : {len(excel_files_set)}")
  report_lines.append(f"Total files found in directory: {len(dir_files)}")
  report_lines.append(f"Filenames auto-corrected in Excel: {updated_rows_count}")

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

  report_text = "\n".join(report_lines)

  print(report_text)

  with open(output_txt_path, "w", encoding="utf-8") as f:
    f.write(report_text)

  print(f"\n[+] Report successfully saved to: {Path(output_txt_path).resolve()}")


# --- Configuration ---
EXCEL_FILE = r"C:\Users\ [ **PATH TO SPREADSHEET** ].xlsx"
SHEET_NAME = 0  # Safely handled whether integer index or string name
COLUMN_NAME = "Filename"
TARGET_DIRECTORY = r"c:\Users\ [ **PATH TO DIRECTORY** ]"
OUTPUT_FILE = r"C:\Users\ [ **PATH TO AUDIT REPORT** ].txt"

# Run the audit
audit_file_match(
    EXCEL_FILE,
    SHEET_NAME,
    COLUMN_NAME,
    TARGET_DIRECTORY,
    OUTPUT_FILE,
    update_excel=True,
)