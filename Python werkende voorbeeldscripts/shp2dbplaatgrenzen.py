# Tutorial: https://www.w3schools.com/python/default.asp
# Read SHP file: https://pcjericks.github.io/py-gdalogr-cookbook/
# Make DB connection: http://www.postgresqltutorial.com/postgresql-python/connect/
# Execute insert statement: http://initd.org/psycopg/docs/usage.html

# Opzet van script
import os
import psycopg2
import ogr

SHP_FOLDER = 'C:/Users/yarad/Documents/school/Engineer herkansing/Testdata'
SHP_FILENAME = 'indonesie_plaatgrenzen.shp'
DATABASE_CONNECTION = "dbname=oefen1 user=postgres password=postgres"

# Inlezen shp bestand in database
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

    haz_plates = feature.GetField('HAZ_PLATES')
    haz_plat_1 = feature.GetField('HAZ_PLAT_1')
    haz_plat_2 = feature.GetField('HAZ_PLAT_2')
    shape_lengte = feature.GetField('Shape_Leng')

    print(haz_plates)
    print(haz_plat_1)
    print(haz_plat_2)
    print(shape_lengte)
    geom_wkt = feature.GetGeometryRef().ExportToWkt()
    print(geom_wkt)
    # Stap 5: Samenstellen geometrie
    # Stap 6: Opstellen insert statement
    # Stap 7: Uitvoeren insert statement
    cur.execute("INSERT INTO public.plaatgrenzen(haz_plates, haz_plat_1, haz_plat_2, shape_lengte, geom) VALUES (%s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s),4326))",(haz_plates, haz_plat_1, haz_plat_2, shape_lengte, geom_wkt))
    # Stap 8: Ophalen volgende rij
    feature = layer.GetNextFeature()

# Stap 9: Print feedback


# Stap 10: Sluiten database
shp_file.Destroy()
conn.commit()
conn.close() 