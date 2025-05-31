import os
from dotenv import load_dotenv

load_dotenv()

# API URLs
GEONAMES_BASE_URL = "http://api.geonames.org"
SUNRISE_SUNSET_API = "https://api.sunrise-sunset.org/json"
WORLDCITIES_URL = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75.zip"

# GeoNames username (free account required)
GEONAMES_USERNAME = os.getenv('GEONAMES_USERNAME', 'demo')

# File paths
DATA_DIR = "data"
CITIES_CSV = os.path.join(DATA_DIR, "world_cities.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "cities_with_sunrise_sunset.csv")

# API rate limiting (requests per second)
RATE_LIMIT = 1

# Minimum population threshold for cities
MIN_POPULATION = 100000