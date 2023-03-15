import xml.etree.ElementTree as ET
import json

# Read the notes file and convert to Solr input format
def convert_to_solr_input(input_file_path, output_file_path):
    with open(input_file_path, 'r') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        
        docs = []
        for note in root.findall('RECORD'):
            doc = {}
            doc['id'] = note.find('ROW_ID').text
            doc['chart_date'] = note.find('CHARTDATE').text
            doc['note_text'] = note.find('TEXT').text
            doc['hospital_expire_flag'] = note.find('HOSPITAL_EXPIRE_FLAG').text
            doc['icd9_codes'] = [code.text for code in note.findall('ICD9_CODE')]
            docs.append(doc)
    
    # Write to output file
    with open(output_file_path, 'w') as f:
        for doc in docs:
            f.write(json.dumps({'id': doc['id'], 'fields': doc}) + '\n')