import psycopg2
import json

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host='172.16.34.1',
    database="mimic",
    user="mimic_demo",
    password="mimic_demo",
    port=5432,
)
cur = conn.cursor()

# Query for the necessary information from the database
cur.execute(
    """
    SELECT ne.row_id, ne.chartdate, ne.text, a.hospital_expire_flag, 
    array_agg(di.icd9_code) as icd9_codes
    FROM mimiciii.noteevents ne
    JOIN mimiciii.admissions a ON ne.hadm_id = a.hadm_id
    JOIN mimiciii.diagnoses_icd di ON a.hadm_id = di.hadm_id
    WHERE ne.category = 'Discharge summary'
    GROUP BY ne.row_id, ne.chartdate, ne.text, a.hospital_expire_flag
    """
)

# Convert the query result into JSON format for indexing in Solr
data = []
for row in cur.fetchall():
    note_id = row[0]
    chart_date = row[1].strftime("%Y-%m-%dT%H:%M:%SZ")
    note_text = row[2]
    hospital_expire_flag = row[3]
    icd9_codes = row[4]

    doc = {
        "id": str(note_id),
        "chart_date": chart_date,
        "note_text": note_text,
        "hospital_expire_flag": hospital_expire_flag,
        "icd9_codes": icd9_codes,
    }
    data.append(doc)

# Write the data into a JSON file
with open("mimic_discharge_summary.json", "w") as f:
    json.dump(data, f)

# Close the database connection
cur.close()
conn.close()
