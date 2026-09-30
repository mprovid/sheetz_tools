import pandas as pd
import numpy as np

# 1. Load the spreadsheets (.xls or .xlsx)
toc_file = r"C:\Users\ [ **PATH TO TOC** ].xlsx"
pdf_file = r"C:\Users\ [ **PATH TO SECOND XLSX** ].xlsx"

toc_df = pd.read_excel(toc_file)
pdf_df = pd.read_excel(pdf_file)

# Strip whitespace from column names to prevent matching errors
toc_df.columns = toc_df.columns.str.strip()
pdf_df.columns = pdf_df.columns.str.strip()

# 2. Convert page columns to numeric values (ignoring any text/errors gracefully)
toc_df['First Page'] = pd.to_numeric(toc_df['First Page'], errors='coerce')
toc_df['Last Page'] = pd.to_numeric(toc_df['Last Page'], errors='coerce')
pdf_df['First Page'] = pd.to_numeric(pdf_df['First Page'], errors='coerce')
pdf_df['Last Page'] = pd.to_numeric(pdf_df['Last Page'], errors='coerce')

# Initialize the new 'Abstracts' column if it doesn't exist
if 'Abstracts' not in pdf_df.columns:
    pdf_df['Abstracts'] = ""

# 3. Process each row in the PDF spreadsheet
for idx, pdf_row in pdf_df.iterrows():
    pdf_vol = pdf_row.get('Volume')
    pdf_start = pdf_row.get('First Page')
    pdf_end = pdf_row.get('Last Page')
    
    # Skip if volume or pages are missing
    if pd.isna(pdf_vol) or pd.isna(pdf_start) or pd.isna(pdf_end):
        continue
        
    # Find matching TOC entries where Edition matches Volume 
    # and the TOC article falls within or overlaps the PDF's page range
    match_mask = (
        (toc_df['Edition'] == pdf_vol) & 
        (toc_df['First Page'] >= pdf_start) & 
        (toc_df['Last Page'] <= pdf_end)
    )
    matching_toc = toc_df[match_mask]
    
    if len(matching_toc) == 1:
        # --- CASE 1: One-to-One Match ---
        # Replace/fill Title Keywords and Contributor Lastname with full details
        match_row = matching_toc.iloc[0]
        pdf_df.at[idx, 'Title KEYWORDS'] = match_row.get('Title of article')
        pdf_df.at[idx, 'Contributor LASTNAME'] = match_row.get('Contributor (Author)')
        
    elif len(matching_toc) > 1:
        # --- CASE 2: Multi-Article Match (e.g., Poetry Section) ---
        # Build a combined text summary for the 'Abstracts' column
        abstract_items = []
        for _, t_row in matching_toc.iterrows():
            title = t_row.get('Title of article', '')
            author = t_row.get('Contributor (Author)', '')
            start_p = t_row.get('First Page', '')
            end_p = t_row.get('Last Page', '')
            item_str = f"\"{title}\" by {author} (pp. {start_p}-{end_p})"
            abstract_items.append(item_str)
            
        # Join them into a clean string
        pdf_df.at[idx, 'Abstracts'] = " | ".join(abstract_items)
        
        # Optional: You can also set a general title indicator if desired, 
        # but leaving keywords/author or updating them to reflect a section header can be done here.

# 4. Save the updated PDF spreadsheet to a new file
# Change this line in your script:
import re

# Function to clean strings of illegal XML/control characters
def clean_text(val):
    if isinstance(val, str):
        # Remove control characters except standard tabs/newlines
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', val)
    return val

# Apply cleaning across all string columns in your dataframe
pdf_df = pdf_df.map(clean_text) # Note: use .applymap(clean_text) if your pandas version is older than 2.1.0

# Then save
output_file = r"C:\Users\ [ **PATH TO MERGED FILE** ] .xlsx"
pdf_df.to_excel(output_file, index=False)

print(f"Processing complete! Saved updated file as '{output_file}'.")