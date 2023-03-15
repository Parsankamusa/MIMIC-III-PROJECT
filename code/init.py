import psycopg2
import pysolr

# Connect to the MIMIC-III database
conn = psycopg2.connect(dbname='mimic', user='mimic_demo', password='Mp6789', host='localhost', port='5432')
cur = conn.cursor()

# Connect to Solr
solr = pysolr.Solr('http://localhost:8983/solr/discharge_summary', always_commit=True)

# Query for all Discharge Summary notes
cur.execute("SELECT note.row_id, note.chartdate, note.text, admission.hospital_expire_flag, admission.admission_type, admission.diagnosis_icd9 FROM noteevents AS note INNER JOIN admissions AS admission ON note.hadm_id=admission.hadm_id WHERE note.category='Discharge summary'")

# Index the notes
for row in cur.fetchall():
    doc = {
        'id': str(row[0]),
        'chartdate': row[1].isoformat(),
        'text': row[2],
        'hospital_expire_flag': bool(row[3]),
        'admission_type': row[4],
        'diagnosis_icd9': row[5]
    }
    solr.add([doc])

# Close the database connection and Solr connection
cur.close()
conn.close()
solr.close()
