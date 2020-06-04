# Tutorial: https://www.w3schools.com/python/default.asp
# Read CSV file: https://cmdlinetips.com/2011/08/three-ways-to-read-a-text-file-line-by-line-in-python/
# Make DB connection: http://www.postgresqltutorial.com/postgresql-python/connect/
# Execute insert statement: http://initd.org/psycopg/docs/usage.html

# Opzet van script
import os
import psycopg2

CSV_FOLDER = 'C:/Users/yarad/Documents/school/Engineer herkansing/Testdata'
CSV_FILENAME = 'test_aardbevingen.csv'
DATABASE_CONNECTION = "dbname=oefen1 user=postgres password=postgres"

# Inlezen csv bestand in database
os.chdir(CSV_FOLDER)

# Stap 1: Openen bestand
csv_file = open(CSV_FILENAME, "r")

# Stap 2: Openen database
conn = psycopg2.connect(DATABASE_CONNECTION)
cur = conn.cursor()

# Stap 3: Ophalen rij uit bestand
line_nr = 0
line = csv_file.readline()
while line:
    line_nr = line_nr + 1
    print(line)
    # Stap 4: Ophalen waardes uit rij
    
    if line_nr > 1 :
        values = line.split(';')
        
        id = values[0]
        jaar = values[1]
        maand = values[2]
        dag = values[3]
        magnitude = values[4]
        if values[6] != '' and values[5] != '' : #Wanneer deze kolommen waardes hebben, maak de x en y floats van deze kollommen. 
            x = float(values[6])
            y = float(values[5])
        if maand != '' and len(maand) == 1 and magnitude != '' and dag != '' and x != '' and y != '' : #Checkt of kollommen waardes hebben, dan insert uitvoeren van die kolommen. 
            cur.execute("INSERT INTO public.aardbevingen(id, jaar, maand, dag, geom, magnitude) VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s),4326), %s )",(id, jaar, maand, dag, x, y, magnitude ))
        # Met len(kolom) == getal bepaal je dat alleen data rijen insert worden die binnen genoemde kolom de lengte hebben van genoemd getal.
        # De if kolom != '' zegt dus: gebruik alleen de waardes uit een kolom en negeer lege cellen.
        # '' is dus een waarde. Als je bijv alleen aardbevingen uit december wilt inserten, gebruik je "maand != '12'.
        # Commit
        conn.commit()
    # Stap 8: Ophalen volgende rij
    line = csv_file.readline()

# Stap 9: Print feedback

# Stap 10: Sluiten database
csv_file.close()
conn.close() 