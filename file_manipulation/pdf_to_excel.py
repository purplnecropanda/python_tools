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

pdf_path = "compatibility.pdf"  # Change this to your PDF file name
output_excel = "output.xlsx"  # Change this to your desired output file name