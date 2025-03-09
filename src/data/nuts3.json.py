import geopandas as gpd
from utils.wrappers import get_cluster_geom
import s3fs
import os
# Initialize S3 filesystem connection
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": f"https://{os.environ['AWS_S3_ENDPOINT']}"},
    key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# Remplacez par le chemin exact vers votre fichier .gpkg sur S3
gpkg_s3_path = "projet-hackathon-ntts-2025/NUTS_RG_01M_2021_4326_LEVL_3.gpkg"

# Téléchargement local du GeoPackage depuis S3
local_gpkg = "/tmp/NUTS_RG_01M_2021_4326_LEVL_3.gpkg"
with fs.open(gpkg_s3_path, "rb") as remote_file:
    with open(local_gpkg, "wb") as f:
        f.write(remote_file.read())

# Lecture du fichier GeoPackage avec GeoPandas
gdf = gpd.read_file(local_gpkg)

# Conversion du GeoDataFrame en JSON
geojson_str = gdf.to_json()

print(geojson_str)