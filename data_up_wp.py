import pandas as pd

# Load the Excel file
df = pd.read_excel("data.xls")   # use read_csv for CSV if needed

# Print column names (headers)
print("Columns:", df.columns.tolist())

# Loop through rows WITH column titles
for index, row in df.iterrows():
    print(f"\nRow {index}:")
    for col in df.columns:
        print(f"  {col}: {row[col]}")
