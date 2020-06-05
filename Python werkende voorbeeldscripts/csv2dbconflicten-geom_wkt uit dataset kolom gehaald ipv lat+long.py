import os
import psycopg2

CSV_FOLDER = 'C:/Users/yarad/Documents/school/Engineer 1 & 2/Eindopdracht/Data'
CSV_FILENAME = 'Individuele evenementen v georganiseerd geweld_20191127.csv'
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
        id = values[0]
        print(values[0])
#         x = float(values[20].replace(',','.'))
#         print(x)
#         y = float(values[19].replace(',','.'))
#         print(y)
        geom = values[21]
        print
        landnaam = values[23]
        conflictnaam = values[5]
        waar_land = values[16]
        jaartal = values[1]
        aantal_doden = values[35]
        # Stap 5: Samenstellen geometrie
        # Stap 6: Opstellen insert statement
        # Stap 7: Uitvoeren insert statement
        print(str(line_nr))
        cur.execute("INSERT INTO public.conflicten(id, geom, landnaam, conflictnaam, jaartal, aantal_doden, waar_land) VALUES (%s, ST_SetSRID(ST_GeomFromText(%s),4326), %s, %s, %s, %s, %s )",(id, geom, landnaam, conflictnaam, jaartal, aantal_doden, waar_land ))
        # Commit
        conn.commit()
    # Stap 8: Ophalen volgende rij
    line = csv_file.readline()

# Stap 9: Print feedback

# Stap 10: Sluiten database
csv_file.close()
conn.close()