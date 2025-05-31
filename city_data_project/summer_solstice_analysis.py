#!/usr/bin/env python3
"""
Standalone script to find top 20 cities with 200k+ population 
ranked by most daylight on Summer Solstice 2024 (June 20)
"""
import pandas as pd
import os
from datetime import date, datetime
from astral import LocationInfo
from astral.sun import sun
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_cities_data():
    """Load comprehensive city data with 200k+ population"""
    cities = [
        # Major world cities with populations over 200k, focusing on northern cities for solstice
        {"name": "Moscow", "latitude": 55.7558, "longitude": 37.6176, "population": 12506000, "country": "Russia"},
        {"name": "Saint Petersburg", "latitude": 59.9311, "longitude": 30.3609, "population": 5383000, "country": "Russia"},
        {"name": "Stockholm", "latitude": 59.3293, "longitude": 18.0686, "population": 975000, "country": "Sweden"},
        {"name": "Helsinki", "latitude": 60.1699, "longitude": 24.9384, "population": 658000, "country": "Finland"},
        {"name": "Oslo", "latitude": 59.9139, "longitude": 10.7522, "population": 697000, "country": "Norway"},
        {"name": "Copenhagen", "latitude": 55.6761, "longitude": 12.5683, "population": 1378000, "country": "Denmark"},
        {"name": "Edinburgh", "latitude": 55.9533, "longitude": -3.1883, "population": 540000, "country": "United Kingdom"},
        {"name": "Murmansk", "latitude": 68.9585, "longitude": 33.0827, "population": 295000, "country": "Russia"},
        {"name": "Anchorage", "latitude": 61.2181, "longitude": -149.9003, "population": 291000, "country": "United States"},
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
        {"name": "London", "latitude": 51.5074, "longitude": -0.1278, "population": 9304000, "country": "United Kingdom"},
        {"name": "Paris", "latitude": 48.8566, "longitude": 2.3522, "population": 10844000, "country": "France"},
        {"name": "Vancouver", "latitude": 49.2827, "longitude": -123.1207, "population": 2581000, "country": "Canada"},
        {"name": "Montreal", "latitude": 45.5017, "longitude": -73.5673, "population": 1780000, "country": "Canada"},
        {"name": "Toronto", "latitude": 43.6532, "longitude": -79.3832, "population": 2930000, "country": "Canada"},
        {"name": "Calgary", "latitude": 51.0447, "longitude": -114.0719, "population": 1336000, "country": "Canada"},
        {"name": "Edmonton", "latitude": 53.5461, "longitude": -113.4938, "population": 981000, "country": "Canada"},
        {"name": "Winnipeg", "latitude": 49.8951, "longitude": -97.1384, "population": 749000, "country": "Canada"},
        {"name": "Seattle", "latitude": 47.6062, "longitude": -122.3321, "population": 750000, "country": "United States"},
        {"name": "Portland", "latitude": 45.5152, "longitude": -122.6784, "population": 650000, "country": "United States"},
        {"name": "Minneapolis", "latitude": 44.9778, "longitude": -93.2650, "population": 430000, "country": "United States"},
        {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298, "population": 2700000, "country": "United States"},
        {"name": "New York", "latitude": 40.7128, "longitude": -74.0060, "population": 8400000, "country": "United States"},
        {"name": "Boston", "latitude": 42.3601, "longitude": -71.0589, "population": 685000, "country": "United States"},
        {"name": "Detroit", "latitude": 42.3314, "longitude": -83.0458, "population": 670000, "country": "United States"},
        {"name": "Amsterdam", "latitude": 52.3676, "longitude": 4.9041, "population": 872000, "country": "Netherlands"},
        {"name": "Brussels", "latitude": 50.8503, "longitude": 4.3517, "population": 1200000, "country": "Belgium"},
        {"name": "Dublin", "latitude": 53.3498, "longitude": -6.2603, "population": 1388000, "country": "Ireland"},
        {"name": "Manchester", "latitude": 53.4808, "longitude": -2.2426, "population": 547000, "country": "United Kingdom"},
        {"name": "Glasgow", "latitude": 55.8642, "longitude": -4.2518, "population": 635000, "country": "United Kingdom"},
        {"name": "Birmingham", "latitude": 52.4862, "longitude": -1.8904, "population": 1140000, "country": "United Kingdom"},
        {"name": "Leeds", "latitude": 53.8008, "longitude": -1.5491, "population": 793000, "country": "United Kingdom"},
        {"name": "Newcastle", "latitude": 54.9783, "longitude": -1.6178, "population": 300000, "country": "United Kingdom"},
        {"name": "Zurich", "latitude": 47.3769, "longitude": 8.5417, "population": 415000, "country": "Switzerland"},
        {"name": "Geneva", "latitude": 46.2044, "longitude": 6.1432, "population": 201000, "country": "Switzerland"},
        # Some global cities for comparison
        {"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503, "population": 37400068, "country": "Japan"},
        {"name": "Delhi", "latitude": 28.7041, "longitude": 77.1025, "population": 28514000, "country": "India"},
        {"name": "Shanghai", "latitude": 31.2304, "longitude": 121.4737, "population": 24256800, "country": "China"},
        {"name": "São Paulo", "latitude": -23.5505, "longitude": -46.6333, "population": 21650000, "country": "Brazil"},
        {"name": "Mexico City", "latitude": 19.4326, "longitude": -99.1332, "population": 21581000, "country": "Mexico"},
        {"name": "Cairo", "latitude": 30.0444, "longitude": 31.2357, "population": 20076000, "country": "Egypt"},
        {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777, "population": 19980000, "country": "India"},
        {"name": "Beijing", "latitude": 39.9042, "longitude": 116.4074, "population": 19618000, "country": "China"},
        {"name": "Istanbul", "latitude": 41.0082, "longitude": 28.9784, "population": 14751000, "country": "Turkey"},
        {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437, "population": 12448000, "country": "United States"},
    ]
    
    # Filter by minimum population of 200k
    filtered_cities = [city for city in cities if city['population'] >= 2000]
    return pd.DataFrame(filtered_cities)

def calculate_daylight_duration(lat, lng, target_date, city_name=""):
    """Calculate daylight duration for a given location and date"""
    try:
        location = LocationInfo(city_name, "", "", lat, lng)
        s = sun(location.observer, date=target_date)
        
        sunrise = s['sunrise']
        sunset = s['sunset']
        
        # Calculate daylight duration in hours
        daylight_duration = (sunset - sunrise).total_seconds() / 3600.0
        
        return {
            'sunrise': sunrise.strftime('%H:%M:%S'),
            'sunset': sunset.strftime('%H:%M:%S'),
            'daylight_hours': daylight_duration,
            'day_length': f"{int(daylight_duration)}:{int((daylight_duration % 1) * 60):02d}:{int(((daylight_duration % 1) * 60 % 1) * 60):02d}"
        }
    except Exception as e:
        logger.warning(f"Error calculating daylight for {city_name}: {e}")
        return {
            'sunrise': None,
            'sunset': None,
            'daylight_hours': 0.0,
            'day_length': "0:00:00"
        }

def main():
    """Main analysis function"""
    # Summer solstice 2024 date
    solstice_date = date(2024, 6, 20)
    
    logger.info("=== SUMMER SOLSTICE 2024 DAYLIGHT ANALYSIS ===")
    logger.info(f"Analyzing cities for {solstice_date}")
    logger.info("Minimum population: 200,000")
    
    # Load city data
    cities_df = get_cities_data()
    logger.info(f"Loaded {len(cities_df)} cities with 200k+ population")
    
    # Calculate daylight for each city
    logger.info("Calculating daylight duration for each city...")
    
    daylight_data = []
    for idx, row in cities_df.iterrows():
        city_name = row['name']
        country = row['country']
        lat = row['latitude']
        lng = row['longitude']
        population = row['population']
        
        logger.info(f"Processing {city_name}, {country} ({idx + 1}/{len(cities_df)})")
        
        daylight_info = calculate_daylight_duration(lat, lng, solstice_date, city_name)
        
        daylight_data.append({
            'name': city_name,
            'country': country,
            'latitude': lat,
            'longitude': lng,
            'population': population,
            'sunrise': daylight_info['sunrise'],
            'sunset': daylight_info['sunset'],
            'daylight_hours': daylight_info['daylight_hours'],
            'day_length': daylight_info['day_length']
        })
    
    # Create results dataframe
    results_df = pd.DataFrame(daylight_data)
    
    # Sort by daylight hours (descending) and then by population for ties
    results_df = results_df.sort_values(['daylight_hours', 'population'], ascending=[False, False])
    
    # Get top 20 cities
    top_20 = results_df.head(20)
    
    # Save to CSV
    output_file = f"summer_solstice_2024_top_20_cities_by_daylight.csv"
    top_20.to_csv(output_file, index=False)
    
    # Display results
    print("\n" + "="*120)
    print("TOP 20 CITIES WITH MOST DAYLIGHT ON SUMMER SOLSTICE 2024 (June 20)")
    print("="*120)
    
    display_df = top_20[['name', 'country', 'population', 'latitude', 'daylight_hours', 'sunrise', 'sunset']].copy()
    display_df['population'] = display_df['population'].apply(lambda x: f"{x:,}")
    display_df['daylight_hours'] = display_df['daylight_hours'].apply(lambda x: f"{x:.2f}h")
    display_df['latitude'] = display_df['latitude'].apply(lambda x: f"{x:.2f}°N")
    
    # Add rank column
    display_df.insert(0, 'rank', range(1, len(display_df) + 1))
    
    print(display_df.to_string(index=False, max_colwidth=15))
    
    print(f"\n🌞 WINNER: {top_20.iloc[0]['name']}, {top_20.iloc[0]['country']}")
    print(f"   Daylight: {top_20.iloc[0]['daylight_hours']:.2f} hours")
    print(f"   Sunrise: {top_20.iloc[0]['sunrise']}")
    print(f"   Sunset: {top_20.iloc[0]['sunset']}")
    print(f"   Population: {top_20.iloc[0]['population']:,}")
    print(f"   Latitude: {top_20.iloc[0]['latitude']:.2f}°N")
    
    print(f"\n📊 Results saved to: {output_file}")
    print(f"🌍 Total cities analyzed: {len(cities_df)}")
    
    # Show some interesting stats
    print(f"\n📈 DAYLIGHT STATISTICS:")
    print(f"   Longest day: {top_20.iloc[0]['daylight_hours']:.2f} hours ({top_20.iloc[0]['name']})")
    print(f"   Shortest day: {top_20.iloc[-1]['daylight_hours']:.2f} hours ({top_20.iloc[-1]['name']})")
    print(f"   Average: {top_20['daylight_hours'].mean():.2f} hours")
    print(f"   Difference: {top_20.iloc[0]['daylight_hours'] - top_20.iloc[-1]['daylight_hours']:.2f} hours")

if __name__ == "__main__":
    main()