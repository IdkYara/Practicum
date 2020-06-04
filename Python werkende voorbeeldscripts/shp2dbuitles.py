# Tutorial: https://www.w3schools.com/python/default.asp
# Read SHP file: https://pcjericks.github.io/py-gdalogr-cookbook/
# Make DB connection: http://www.postgresqltutorial.com/postgresql-python/connect/
# Execute insert statement: http://initd.org/psycopg/docs/usage.html

# Opzet van script
import os
import psycopg2
import ogr

SHP_FOLDER = 'C:/Users/yarad/Documents/school/Engineer 1'
SHP_FILENAME = '2018_Imergis_provinciegrenzen_met_water.shp'
DATABASE_CONNECTION = "dbname=engineer1920 user=postgres password=postgres"

# Inlezen csv bestand in database
os.chdir(SHP_FOLDER)

# Stap 1: Openen bestand
driver = ogr.GetDriverByName('ESRI Shapefile')
shp_file = driver.Open(SHP_FILENAME, 0)
layer = shp_file.GetLayer()

# Stap 2: Openen database
conn = psycopg2.connect(DATABASE_CONNECTION)
cur = conn.cursor()

# Stap 3: Ophalen rij uit bestand
feature_nr = 0
feature = layer.GetNextFeature()
while feature:
    feature_nr = feature_nr + 1
    # Stap 4: Ophalen waardes uit rij
    id = feature.GetField('id')
    provincienaam = feature.GetField('Provincien')
    print(id)
    print(provincienaam)
    geom_wkt = feature.GetGeometryRef().ExportToWkt()
    # Stap 5: Samenstellen geometrie
    # Stap 6: Opstellen insert statement
    # Stap 7: Uitvoeren insert statement
    cur.execute("INSERT INTO public.provincie(id, provnaam, geom) VALUES (%s, %s, ST_Transform(ST_SetSRID(ST_GeomFromText(%s),28992),4326))",(id, provincienaam, geom_wkt))
    # Stap 8: Ophalen volgende rij
    feature = layer.GetNextFeature()

# Stap 9: Print feedback


# Stap 10: Sluiten database
shp_file.Destroy()
conn.commit()
conn.close()