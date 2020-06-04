# Tutorial: https://www.w3schools.com/python/default.asp
# Read CSV file: https://cmdlinetips.com/2011/08/three-ways-to-read-a-text-file-line-by-line-in-python/
# Make DB connection: http://www.postgresqltutorial.com/postgresql-python/connect/
# Execute insert statement: http://initd.org/psycopg/docs/usage.html

# Opzet van script
import os
import psycopg2

CSV_FOLDER = 'C:/Users/yarad/Documents/school/Engineer 1 & 2/Eindopdracht/Data'
CSV_FILENAME = 'Immigratie cijfers per land 1995 tot 2018_utf8.csv'
DATABASE_CONNECTION = "dbname=immigratie_eindopdracht user=postgres password=postgres"

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
        migratieachtergrond = values[1]
        jaartal = values[3]
        print(jaartal)
        aantal = values[4]
        print(aantal)
        # Stap 5: Samenstellen geometrie
        # Stap 6: Opstellen insert statement
        # Stap 7: Uitvoeren insert statement
        if len(jaartal) == 4 and aantal != '\n' :
            print("insert")
            cur.execute("INSERT INTO public.immigratie(migratieachtergrond, jaartal, aantal) VALUES (%s, %s, %s)",(migratieachtergrond, jaartal, aantal))
        # Commit
        #conn.commit()
     # Stap 8: Ophalen volgende rij
    line = csv_file.readline()

# Stap 9: Print feedback

# Stap 10: Sluiten database
csv_file.close()
conn.close()