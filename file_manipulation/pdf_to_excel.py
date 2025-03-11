import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path, output_excel):
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            extracted_tables = page.extract_tables()
            for table_idx, table in enumerate(extracted_tables):
                if table:  # Ensure table is not empty
                    df = pd.DataFrame(table)
                    df.columns = [f"Column_{i+1}" for i in range(len(df.columns))]  # Assign generic column names
                    sheet_name = f"Page_{page_num+1}_Table_{table_idx+1}"
                    all_tables.append((sheet_name, df))
    
    with pd.ExcelWriter(output_excel) as writer:
        for name, df in all_tables:
            df.to_excel(writer, sheet_name=name, index=False)
    
    print(f"Extraction complete. Tables saved to {output_excel}")

def extract_and_merge_tables(pdf_path, output_excel, header_rows_to_skip=0): #if the code is outputting the first row from multiple pages you can set header_rows_to_skip='number of rows you want to skip'
    all_data = []
    first_table = True
    column_headers = None  # Store consistent headers
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                if table:  # Ensure table is not empty
                    df = pd.DataFrame(table)
                    
                    # Set headers for the first table and enforce consistency for others
                    if first_table:
                        column_headers = df.iloc[0].tolist()  # Store first table's headers
                        df.columns = column_headers  # Set headers
                        df = df[1:].reset_index(drop=True)  # Drop first row
                        first_table = False
                    else:
                        df = df[header_rows_to_skip:].reset_index(drop=True)  # Skip headers
                        df.columns = column_headers[:len(df.columns)]  # Ensure alignment
                        df = df.iloc[:, :len(column_headers)]  # Trim extra columns if needed
                    
                    all_data.append(df)
    
    if all_data:
        merged_df = pd.concat(all_data, ignore_index=True)
        merged_df.to_excel(output_excel, index=False)
        print(f"Extraction complete. Merged table saved to {output_excel}")
    else:
        print("No tables found in the PDF.")

pdf_path = "compatibility.pdf"  # Change this to your PDF file name
output_excel = "output.xlsx"  # Change this to your desired output file name 
''' 
extract_tables_from_pdf:
    extracts all tables from a PDF file and extracts them into individual sheets, use if each table has different data.
extract_and_merge_tables:
    extracts all tables from a PDF file and outputs them to a single combined table which is great for tables spanning multiple pages containing same columns
uncomment the ones below
'''

#extract_tables_from_pdf(pdf_path, output_excel)
#extract_and_merge_tables(pdf_path, output_excel)