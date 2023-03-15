import psycopg2

# Connect to the default postgres database
conn = psycopg2.connect(dbname='mimic', user='mimi_demo', password='mimic_demo', host='localhost', port='5050')

# Create a new database
cur = conn.cursor()
cur.execute('CREATE DATABASE mydatabase;')
conn.commit()

# Close the connection
cur.close()
conn.close()
