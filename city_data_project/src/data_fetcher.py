"""
Data fetching utilities for city information
"""
import requests
import time
import pandas as pd
from typing import Dict, Optional, List
import logging
from .config import GEONAMES_USERNAME, GEONAMES_BASE_URL, RATE_LIMIT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CityDataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < (1.0 / RATE_LIMIT):
            time.sleep((1.0 / RATE_LIMIT) - elapsed)
        self.last_request_time = time.time()
    
    def get_geonames_cities(self, country_code: str = "", max_rows: int = 1000) -> List[Dict]:
        """
        Fetch cities from GeoNames API
        """
        if GEONAMES_USERNAME == 'demo' or not GEONAMES_USERNAME:
            logger.warning("Using demo username or no username set. Please register at geonames.org and set GEONAMES_USERNAME in .env file")
            logger.warning("Demo account has severe rate limits and should not be used for real applications")
        
        self._rate_limit()
        
        params = {
            'username': GEONAMES_USERNAME,
            'featureClass': 'P',  # Populated places
            'maxRows': max_rows,
            'type': 'json'
        }
        
        if country_code:
            params['country'] = country_code
        
        try:
            response = self.session.get(f"{GEONAMES_BASE_URL}/searchJSON", params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'geonames' in data:
                return data['geonames']
            else:
                logger.warning(f"No geonames data found. Response: {data}")
                if 'status' in data:
                    logger.error(f"GeoNames API error: {data['status']}")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Error fetching GeoNames data: {e}")
            return []
    
    def download_world_cities_csv(self, url: str, output_path: str) -> bool:
        """
        Download world cities CSV file
        """
        try:
            logger.info(f"Downloading world cities data from {url}")
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded cities data to {output_path}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Error downloading cities data: {e}")
            return False
    
    def load_cities_from_csv(self, csv_path: str, min_population: int = 0) -> pd.DataFrame:
        """
        Load cities from CSV file and filter by population
        """
        try:
            df = pd.read_csv(csv_path)
            
            # Standardize column names
            column_mapping = {
                'city': 'name',
                'city_ascii': 'name_ascii', 
                'lat': 'latitude',
                'lng': 'longitude',
                'pop': 'population',
                'country': 'country_name',
                'iso2': 'country_code'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Filter by population
            if min_population > 0:
                df = df[df['population'] >= min_population]
            
            # Remove rows with missing coordinates
            df = df.dropna(subset=['latitude', 'longitude'])
            
            logger.info(f"Loaded {len(df)} cities from {csv_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading cities from CSV: {e}")
            return pd.DataFrame()