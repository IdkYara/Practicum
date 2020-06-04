# Tutorial: https://www.w3schools.com/python/default.asp
# Read SHP file: https://pcjericks.github.io/py-gdalogr-cookbook/
# Make DB connection: http://www.postgresqltutorial.com/postgresql-python/connect/
# Execute insert statement: http://initd.org/psycopg/docs/usage.html

# Opzet van script
import os
import psycopg2
import ogr

SHP_FOLDER = 'C:/Users/yarad/Documents/school/bo Delphy/Datasets'
SHP_FILENAME = 'gewaspercelenZeeBra.shp'
DATABASE_CONNECTION = "dbname=Delphybo user=postgres password=postgres"

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
    
    objectid = feature.GetField('OBJECTID')
    cat_gewascategorie = feature.GetField('CAT_GEWASC')
    gws_gewascode = feature.GetField('GWS_GEWASC')
    gws_gewas = feature.GetField('GWS_GEWAS')
    shape_area = feature.GetField('AREA')

    print(objectid)
    print(cat_gewascategorie)
    print(gws_gewascode)
    print(gws_gewas)
    print(shape_area)
    geom_wkt = feature.GetGeometryRef().ExportToWkt()
    print(geom_wkt)
    # Stap 5: Samenstellen geometrie
    # Stap 6: Opstellen insert statement
    # Stap 7: Uitvoeren insert statement
    cur.execute("INSERT INTO public.percelen(objectid, cat_gewascategorie, gws_gewascode, gws_gewas, shape_area, geom) VALUES (%s, %s, %s, %s, %s, ST_Transform(ST_SetSRID(ST_GeomFromText(%s),28992),4326))",(objectid, cat_gewascategorie, gws_gewascode, gws_gewas, shape_area, geom_wkt))
    # Stap 8: Ophalen volgende rij
    feature = layer.GetNextFeature()

    # Stap 9: Print feedback
    conn.commit()

# Stap 10: Sluiten database
shp_file.Destroy()
conn.close()