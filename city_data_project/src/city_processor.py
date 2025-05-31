"""
Main city data processing pipeline
"""
import pandas as pd
import logging
from datetime import date
from typing import Optional
from .data_fetcher import CityDataFetcher
from .sunrise_calculator import SunriseSunsetCalculator
from .config import MIN_POPULATION, OUTPUT_CSV, DATA_DIR
import os

logger = logging.getLogger(__name__)

class CityDataProcessor:
    def __init__(self):
        self.data_fetcher = CityDataFetcher()
        self.sunrise_calculator = SunriseSunsetCalculator()
        
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
    
    def load_sample_cities(self, min_population: int = 200000) -> pd.DataFrame:
        """
        Create a comprehensive dataset of major world cities with 200k+ population
        """
        sample_cities = [
            # Major world cities with populations over 200k
            {"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503, "population": 37400068, "country": "Japan"},
            {"name": "Delhi", "latitude": 28.7041, "longitude": 77.1025, "population": 28514000, "country": "India"},
            {"name": "Shanghai", "latitude": 31.2304, "longitude": 121.4737, "population": 24256800, "country": "China"},
            {"name": "São Paulo", "latitude": -23.5505, "longitude": -46.6333, "population": 21650000, "country": "Brazil"},
            {"name": "Mexico City", "latitude": 19.4326, "longitude": -99.1332, "population": 21581000, "country": "Mexico"},
            {"name": "Cairo", "latitude": 30.0444, "longitude": 31.2357, "population": 20076000, "country": "Egypt"},
            {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777, "population": 19980000, "country": "India"},
            {"name": "Beijing", "latitude": 39.9042, "longitude": 116.4074, "population": 19618000, "country": "China"},
            {"name": "Dhaka", "latitude": 23.8103, "longitude": 90.4125, "population": 19578000, "country": "Bangladesh"},
            {"name": "Osaka", "latitude": 34.6937, "longitude": 135.5023, "population": 19281000, "country": "Japan"},
            {"name": "New York", "latitude": 40.7128, "longitude": -74.0060, "population": 18819000, "country": "United States"},
            {"name": "Karachi", "latitude": 24.8607, "longitude": 67.0011, "population": 15400000, "country": "Pakistan"},
            {"name": "Buenos Aires", "latitude": -34.6118, "longitude": -58.3960, "population": 14967000, "country": "Argentina"},
            {"name": "Chongqing", "latitude": 29.4316, "longitude": 106.9123, "population": 14838000, "country": "China"},
            {"name": "Istanbul", "latitude": 41.0082, "longitude": 28.9784, "population": 14751000, "country": "Turkey"},
            {"name": "Kolkata", "latitude": 22.5726, "longitude": 88.3639, "population": 14681000, "country": "India"},
            {"name": "Manila", "latitude": 14.5995, "longitude": 120.9842, "population": 13482000, "country": "Philippines"},
            {"name": "Lagos", "latitude": 6.5244, "longitude": 3.3792, "population": 13463000, "country": "Nigeria"},
            {"name": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729, "population": 13293000, "country": "Brazil"},
            {"name": "Tianjin", "latitude": 39.3434, "longitude": 117.3616, "population": 13215000, "country": "China"},
            {"name": "London", "latitude": 51.5074, "longitude": -0.1278, "population": 9304000, "country": "United Kingdom"},
            {"name": "Paris", "latitude": 48.8566, "longitude": 2.3522, "population": 10844000, "country": "France"},
            {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093, "population": 5312000, "country": "Australia"},
            {"name": "Vancouver", "latitude": 49.2827, "longitude": -123.1207, "population": 2581000, "country": "Canada"},
            {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437, "population": 12448000, "country": "United States"},
            # Additional northern cities for summer solstice analysis
            {"name": "Moscow", "latitude": 55.7558, "longitude": 37.6176, "population": 12506000, "country": "Russia"},
            {"name": "Saint Petersburg", "latitude": 59.9311, "longitude": 30.3609, "population": 5383000, "country": "Russia"},
            {"name": "Stockholm", "latitude": 59.3293, "longitude": 18.0686, "population": 975000, "country": "Sweden"},
            {"name": "Helsinki", "latitude": 60.1699, "longitude": 24.9384, "population": 658000, "country": "Finland"},
            {"name": "Oslo", "latitude": 59.9139, "longitude": 10.7522, "population": 697000, "country": "Norway"},
            {"name": "Copenhagen", "latitude": 55.6761, "longitude": 12.5683, "population": 1378000, "country": "Denmark"},
            {"name": "Edinburgh", "latitude": 55.9533, "longitude": -3.1883, "population": 540000, "country": "United Kingdom"},
            {"name": "Reykjavik", "latitude": 64.1466, "longitude": -21.9426, "population": 131000, "country": "Iceland"},
            {"name": "Anchorage", "latitude": 61.2181, "longitude": -149.9003, "population": 291000, "country": "United States"},
            {"name": "Fairbanks", "latitude": 64.8378, "longitude": -147.7164, "population": 32000, "country": "United States"},
            {"name": "Tromsø", "latitude": 69.6492, "longitude": 18.9553, "population": 76000, "country": "Norway"},
            {"name": "Murmansk", "latitude": 68.9585, "longitude": 33.0827, "population": 295000, "country": "Russia"},
            {"name": "Whitehorse", "latitude": 60.7212, "longitude": -135.0568, "population": 28000, "country": "Canada"},
            {"name": "Yellowknife", "latitude": 62.4540, "longitude": -114.3718, "population": 20000, "country": "Canada"},
            {"name": "Berlin", "latitude": 52.5200, "longitude": 13.4050, "population": 3669000, "country": "Germany"},
            {"name": "Hamburg", "latitude": 53.5511, "longitude": 9.9937, "population": 1900000, "country": "Germany"},
            {"name": "Munich", "latitude": 48.1351, "longitude": 11.5820, "population": 1488000, "country": "Germany"},
            {"name": "Vienna", "latitude": 48.2082, "longitude": 16.3738, "population": 1911000, "country": "Austria"},
            {"name": "Prague", "latitude": 50.0755, "longitude": 14.4378, "population": 1309000, "country": "Czech Republic"},
            {"name": "Warsaw", "latitude": 52.2297, "longitude": 21.0122, "population": 1793000, "country": "Poland"},
            {"name": "Kiev", "latitude": 50.4501, "longitude": 30.5234, "population": 2952000, "country": "Ukraine"},
            {"name": "Minsk", "latitude": 53.9045, "longitude": 27.5615, "population": 2009000, "country": "Belarus"},
            {"name": "Riga", "latitude": 56.9496, "longitude": 24.1052, "population": 633000, "country": "Latvia"},
            {"name": "Vilnius", "latitude": 54.6872, "longitude": 25.2797, "population": 574000, "country": "Lithuania"},
            {"name": "Tallinn", "latitude": 59.4370, "longitude": 24.7536, "population": 437000, "country": "Estonia"},
        ]
        
        df = pd.DataFrame(sample_cities)
        # Filter by minimum population
        df = df[df['population'] >= min_population]
        return df
    
    def add_sunrise_sunset_data(self, cities_df: pd.DataFrame, 
                               target_date: Optional[date] = None,
                               use_api: bool = True,
                               sample_size: Optional[int] = None) -> pd.DataFrame:
        """
        Add sunrise/sunset data to cities dataframe
        """
        if sample_size:
            cities_df = cities_df.head(sample_size)
        
        if target_date is None:
            target_date = date.today()
        
        logger.info(f"Processing {len(cities_df)} cities for date {target_date}")
        
        # Initialize new columns
        sunrise_data_columns = [
            'sunrise', 'sunset', 'solar_noon', 'day_length',
            'civil_twilight_begin', 'civil_twilight_end',
            'calculation_date', 'data_source'
        ]
        
        for col in sunrise_data_columns:
            cities_df[col] = None
        
        # Process each city
        for idx, row in cities_df.iterrows():
            city_name = row['name']
            lat = row['latitude']
            lng = row['longitude']
            
            logger.info(f"Processing {city_name} ({idx + 1}/{len(cities_df)})")
            
            # Get sunrise/sunset data
            sun_data = self.sunrise_calculator.get_sunrise_sunset(
                lat, lng, city_name, use_api, target_date
            )
            
            if sun_data:
                # Update dataframe with sun data
                for key, value in sun_data.items():
                    if key in cities_df.columns:
                        cities_df.at[idx, key] = value
                
                cities_df.at[idx, 'calculation_date'] = target_date.isoformat()
                cities_df.at[idx, 'data_source'] = 'api' if use_api else 'local'
            else:
                logger.warning(f"No sunrise/sunset data obtained for {city_name}")
        
        return cities_df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Save dataframe to CSV file
        """
        if filename is None:
            filename = OUTPUT_CSV
        
        filepath = os.path.join(DATA_DIR, filename) if not os.path.dirname(filename) else filename
        
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Saved {len(df)} cities data to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return ""
    
    def parse_day_length_to_hours(self, day_length_str: str) -> float:
        """
        Convert day_length string (like "16:30:45") to decimal hours
        """
        try:
            if pd.isna(day_length_str) or not day_length_str:
                return 0.0
            
            # Handle different formats
            if isinstance(day_length_str, (int, float)):
                return float(day_length_str)
            
            # Parse time format (HH:MM:SS or HH:MM)
            time_parts = str(day_length_str).split(':')
            hours = int(time_parts[0]) if len(time_parts) > 0 else 0
            minutes = int(time_parts[1]) if len(time_parts) > 1 else 0
            seconds = int(time_parts[2]) if len(time_parts) > 2 else 0
            
            return hours + minutes/60.0 + seconds/3600.0
        except Exception as e:
            logger.warning(f"Could not parse day length '{day_length_str}': {e}")
            return 0.0
    
    def rank_cities_by_daylight(self, df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
        """
        Rank cities by amount of daylight and return top N
        """
        # Parse day length to decimal hours for sorting
        df['daylight_hours'] = df['day_length'].apply(self.parse_day_length_to_hours)
        
        # Sort by daylight hours (descending) and then by population (descending) for ties
        ranked_df = df.sort_values(['daylight_hours', 'population'], ascending=[False, False])
        
        # Return top N cities
        return ranked_df.head(top_n)
    
    def process_summer_solstice_analysis(self, min_population: int = 200000, 
                                       top_cities: int = 20, 
                                       use_api: bool = True) -> pd.DataFrame:
        """
        Analyze cities for summer solstice (June 20, 2024) and rank by daylight
        """
        from datetime import date
        solstice_date = date(2024, 6, 20)
        
        logger.info(f"Loading cities with minimum population {min_population:,}...")
        cities_df = self.load_sample_cities(min_population)
        
        logger.info(f"Processing {len(cities_df)} cities for summer solstice {solstice_date}...")
        enriched_df = self.add_sunrise_sunset_data(cities_df, solstice_date, use_api)
        
        logger.info("Ranking cities by daylight hours...")
        top_cities_df = self.rank_cities_by_daylight(enriched_df, top_cities)
        
        return top_cities_df