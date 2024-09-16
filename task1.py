import pandas as pd
import zipfile
import os

zip_file_path = '/Users/aimanahamed/Desktop/Software Now/your_zipped_folder.zip'
output_text_file = '/Users/aimanahamed/Desktop/Software Now/output_text_file.txt'
extracted_folder = '/Users/aimanahamed/Desktop/Software Now/extracted_files'


with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

all_texts = ""

for file_name in os.listdir(extracted_folder):
    if file_name.endswith('.csv'):
        csv_file_path = os.path.join(extracted_folder, file_name)
        print(f"Processing file: {csv_file_path}") 
        df = pd.read_csv(csv_file_path)
        
        
        if 'TEXT' in df.columns:
            print(f"Found 'TEXT' column in {file_name}")  
            text_column = df['TEXT'].dropna().tolist() 
            if text_column:
                all_texts += '\n'.join(text_column) + '\n'
            else:
                print(f"No text found in 'TEXT' column of {file_name}") 
        
    
        if 'SHORT-TEXT' in df.columns:
            print(f"Found 'SHORT-TEXT' column in {file_name}") 
            short_text_column = df['SHORT-TEXT'].dropna().tolist()  
            if short_text_column:
                all_texts += '\n'.join(short_text_column) + '\n'
            else:
                print(f"No text found in 'SHORT-TEXT' column of {file_name}") 
                
with open(output_text_file, 'w', encoding='utf-8') as f:
    f.write(all_texts)

print(f"Texts from all CSV files have been written to {output_text_file}")
