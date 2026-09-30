import pandas as pd

# 1. Load your existing spreadsheet
# Replace 'input_file.csv' with your actual file name (supports .csv or .xlsx)
input_file = r"C:\Users\ [ **PATH TO ORIGINAL DOCUMENT** ].xlsx"
if input_file.endswith('.xlsx'):
    df = pd.read_excel(input_file)
else:
    df = pd.read_csv(input_file)

# 2. Define the complete list of target JSTOR template columns
jstor_columns = [
    'Filename', 'Identifier', 'Title', 'Alternate Title', 'Contributor', 
    'Date', 'Temporal Coverage', 'Precise Date', 'Description', 'Abstract', 
    'Subject', 'Creation Site', 'Discovery Site', 'Spatial Coverage', 
    'Publisher Location', 'Publisher', 'Language', 'Extent', 'Format', 
    'Measurements', 'Medium', 'Techniques', 'Source', 'Repository', 
    'Holding Institution', 'Rights Note', 'License', 'Rights', 'Volume', 
    'Issue Number', 'First Page', 'Last Page', 'Page Range', 'Edition', 
    'Series Designation', 'Culture', 'Period', 'Style', 'Style/Period', 
    'Image View Description', 'Work Type'
]

# 3. Create a mapping dictionary for columns that change names
# (e.g., your 'Abstracts' column maps to JSTOR's 'Abstract' column)
column_mapping = {
    'Abstracts': 'Abstract'
}
df = df.rename(columns=column_mapping)

# 4. Reindex the dataframe to match the JSTOR template 
# Missing columns will automatically be created and filled with empty values (NaN)
restructured_df = df.reindex(columns=jstor_columns)

# Optional: Replace NaN (empty cells) with empty strings if preferred for the export
restructured_df = restructured_df.fillna('')

# 5. Export to a new file
output_file = r"C:\Users\ [ **PATH TO NEW DOCUMENT BEING CREATED** ] .csv"
restructured_df.to_csv(output_file, index=False)

print(f"Success! Restructured file saved as: {output_file}")