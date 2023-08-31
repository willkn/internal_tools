import os
import re
import pandas as pd
import csv

def createArticleDictionary():
    # Define the regex pattern to match the desired string format
    pattern = r'\d{3}\.\d{3}\.\d{2}'

    # Find the text file in the current directory
    text_file = None
    for filename in os.listdir():
        if filename.endswith('.txt'):
            text_file = filename
            break

    if text_file is None:
        print("No text file found in the directory.")
        return {}

    # Open the text file and read its lines
    with open(text_file, 'r') as file:
        lines = file.readlines()

    # Find and collect strings matching the pattern
    matched_strings = []
    for line in lines:
        match = re.search(pattern, line)
        if match:
            # Remove dots (,) from the matched string and add it to the list
            matched_string = match.group().replace('.', '')
            matched_strings.append(matched_string)

    if matched_strings:
        # Create a dictionary with matched strings as keys and initial values as zero
        price_changes_dict = {string: 0 for string in matched_strings}
    else:
        print("No matching strings found in the text file.")
        price_changes_dict = {}

    return price_changes_dict
    

def crossReference(price_changes_dict, ARTNOS):
    # Creates a list of articles to check 
    artnos_to_check = list(price_changes_dict.keys())

    for article in artnos_to_check:
        price_changes_dict[article] = ARTNOS.count(article)


    return price_changes_dict


def renameHeaders():
    slm03_file = 'SLM03.csv'  # Replace with your actual CSV file

    if os.path.exists(slm03_file):
        try:
            temp_file = 'SLM03_temp.csv'  # Temporary file to write updated data

            df = pd.read_csv(slm03_file, sep='\t')
            new_headers = [
                'DIV', 'SPECSHOP_UNICODE', 'RANGEGROUP_UNICODE', 'HFB', 'PA', 'ARTNO', 'ARTNAME_UNICODE',
                'SLID', 'LOCTYP', 'PICK_LOCATIONS', 'ACTIVE', 'PLANNED', 'RANGECODE1', 'SRP', 'FCST',
                'ASSQ', 'SSQ', 'DTFP', 'DTFP_PLUS', 'MIN_SSQ', 'MAX_SSQ', 'RSSQ', 'RSSQ_LTV',
                'FLEX_OVER_ASSQ', 'FLEX%', 'RPP', 'MOH', 'PDOM', 'COMQTY', 'L_MPQ', 'C_MPQ',
                'C_PALQ', 'MSOLSTATUS', 'DT', 'FLOWTYPE', 'TM', 'COUNT_HANDL', 'SOLD_M3', 'HANDL',
                'SSD', 'EDS', 'DISTMODE', 'AVGSALES', 'AVAILSTOCK', 'QTYSGF', 'FILLRATEART', 'VOL'
            ]

            df.to_csv(temp_file, sep='\t', index=False, header=new_headers)

            print(f"'{slm03_file}' headers have been updated.")

            return temp_file  # Return the temporary file
        except UnicodeDecodeError:
            print(f"Could not decode '{slm03_file}' using UTF-8 encoding.")
    else:
        print(f"'{slm03_file}' not found.")
    return None  # Return None if headers were not updated

def listAllHeaders(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep='\t')
        headers = df.columns.tolist()
        print("Headers from SLM03_temp.csv:")
        for header in headers:
            print(header)
    else:
        print(f"'{file_path}' not found.")

def getARTNOColumnValues(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep='\t', dtype={'ARTNO': 'str'})
        if 'ARTNO' in df.columns:
            slid_values = df['ARTNO'].tolist()
            return slid_values
        else:
            print("'ARTNO' column not found.")
            return []
    else:
        print(f"'{file_path}' not found.")
        return []

def writeDictionaryToCSV(articleDictionary, output_filename):
    sorted_dict = {key: articleDictionary[key] for key in sorted(articleDictionary)}
    
    with open(output_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for artno, count in sorted_dict.items():
            if count >= 2:
                csv_writer.writerow([artno, count])

def main():
    # List of all the ARTNOS from SLM03
    ARTNOS = list(getARTNOColumnValues(renameHeaders()))
    
    # Creates an dictionary containing all the articles
    articleDictionary = createArticleDictionary()
    articleDictionary = crossReference(articleDictionary, ARTNOS)

    writeDictionaryToCSV(articleDictionary, 'priceChanges.csv')
    print(f"Article counts written to 'priceChanges.csv'")
    

if __name__ == "__main__":
    main()
