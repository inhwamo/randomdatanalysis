#!/usr/bin/env python3
"""
North American cities ranked by daylight on Summer Solstice 2024 (June 20)
"""
import pandas as pd
from datetime import date
from astral import LocationInfo
from astral.sun import sun
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_north_american_cities():
    """Load comprehensive North American city data"""
    cities = [
        # CANADA - Major cities + northern settlements
        {"name": "Yellowknife", "latitude": 62.4540, "longitude": -114.3718, "population": 20000, "country": "Canada"},
        {"name": "Whitehorse", "latitude": 60.7212, "longitude": -135.0568, "population": 28000, "country": "Canada"},
        {"name": "Iqaluit", "latitude": 63.7467, "longitude": -68.5170, "population": 7740, "country": "Canada"},
        {"name": "Fort McMurray", "latitude": 56.7267, "longitude": -111.3790, "population": 68000, "country": "Canada"},
        {"name": "Grande Prairie", "latitude": 55.1707, "longitude": -118.8034, "population": 63000, "country": "Canada"},
        {"name": "Prince George", "latitude": 53.9171, "longitude": -122.7497, "population": 75000, "country": "Canada"},
        {"name": "Edmonton", "latitude": 53.5461, "longitude": -113.4938, "population": 981000, "country": "Canada"},
        {"name": "Saskatoon", "latitude": 52.1579, "longitude": -106.6702, "population": 317000, "country": "Canada"},
        {"name": "Regina", "latitude": 50.4452, "longitude": -104.6189, "population": 236000, "country": "Canada"},
        {"name": "Calgary", "latitude": 51.0447, "longitude": -114.0719, "population": 1336000, "country": "Canada"},
        {"name": "Winnipeg", "latitude": 49.8951, "longitude": -97.1384, "population": 749000, "country": "Canada"},
        {"name": "Vancouver", "latitude": 49.2827, "longitude": -123.1207, "population": 2581000, "country": "Canada"},
        {"name": "Thunder Bay", "latitude": 48.3809, "longitude": -89.2477, "population": 121000, "country": "Canada"},
        {"name": "Sudbury", "latitude": 46.4917, "longitude": -80.9930, "population": 166000, "country": "Canada"},
        {"name": "Quebec City", "latitude": 46.8139, "longitude": -71.2080, "population": 540000, "country": "Canada"},
        {"name": "Montreal", "latitude": 45.5017, "longitude": -73.5673, "population": 1780000, "country": "Canada"},
        {"name": "Ottawa", "latitude": 45.4215, "longitude": -75.6972, "population": 1017000, "country": "Canada"},
        {"name": "Halifax", "latitude": 44.6488, "longitude": -63.5752, "population": 348000, "country": "Canada"},
        {"name": "Toronto", "latitude": 43.6532, "longitude": -79.3832, "population": 2930000, "country": "Canada"},
        {"name": "Hamilton", "latitude": 43.2557, "longitude": -79.8711, "population": 693000, "country": "Canada"},
        {"name": "London", "latitude": 42.9849, "longitude": -81.2453, "population": 422000, "country": "Canada"},
        {"name": "Windsor", "latitude": 42.3149, "longitude": -83.0364, "population": 230000, "country": "Canada"},
        
        # UNITED STATES - All major cities including Alaska
        {"name": "Utqiagvik (Barrow)", "latitude": 71.2906, "longitude": -156.7886, "population": 5000, "country": "United States"},
        {"name": "Fairbanks", "latitude": 64.8378, "longitude": -147.7164, "population": 32000, "country": "United States"},
        {"name": "Anchorage", "latitude": 61.2181, "longitude": -149.9003, "population": 291000, "country": "United States"},
        {"name": "Juneau", "latitude": 58.3019, "longitude": -134.4197, "population": 32000, "country": "United States"},
        {"name": "Seattle", "latitude": 47.6062, "longitude": -122.3321, "population": 750000, "country": "United States"},
        {"name": "Portland", "latitude": 45.5152, "longitude": -122.6784, "population": 650000, "country": "United States"},
        {"name": "Spokane", "latitude": 47.6587, "longitude": -117.4260, "population": 220000, "country": "United States"},
        {"name": "Boise", "latitude": 43.6150, "longitude": -116.2023, "population": 230000, "country": "United States"},
        {"name": "Minneapolis", "latitude": 44.9778, "longitude": -93.2650, "population": 430000, "country": "United States"},
        {"name": "Milwaukee", "latitude": 43.0389, "longitude": -87.9065, "population": 590000, "country": "United States"},
        {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298, "population": 2700000, "country": "United States"},
        {"name": "Detroit", "latitude": 42.3314, "longitude": -83.0458, "population": 670000, "country": "United States"},
        {"name": "Cleveland", "latitude": 41.4993, "longitude": -81.6944, "population": 385000, "country": "United States"},
        {"name": "Buffalo", "latitude": 42.8864, "longitude": -78.8784, "population": 255000, "country": "United States"},
        {"name": "Boston", "latitude": 42.3601, "longitude": -71.0589, "population": 685000, "country": "United States"},
        {"name": "New York", "latitude": 40.7128, "longitude": -74.0060, "population": 8400000, "country": "United States"},
        {"name": "Philadelphia", "latitude": 39.9526, "longitude": -75.1652, "population": 1580000, "country": "United States"},
        {"name": "Pittsburgh", "latitude": 40.4406, "longitude": -79.9959, "population": 305000, "country": "United States"},
        {"name": "Denver", "latitude": 39.7392, "longitude": -104.9903, "population": 715000, "country": "United States"},
        {"name": "Salt Lake City", "latitude": 40.7608, "longitude": -111.8910, "population": 200000, "country": "United States"},
        {"name": "Las Vegas", "latitude": 36.1699, "longitude": -115.1398, "population": 650000, "country": "United States"},
        {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437, "population": 12448000, "country": "United States"},
        {"name": "San Diego", "latitude": 32.7157, "longitude": -117.1611, "population": 1410000, "country": "United States"},
        {"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194, "population": 875000, "country": "United States"},
        {"name": "Phoenix", "latitude": 33.4484, "longitude": -112.0740, "population": 1660000, "country": "United States"},
        {"name": "Tucson", "latitude": 32.2226, "longitude": -110.9747, "population": 550000, "country": "United States"},
        {"name": "Albuquerque", "latitude": 35.0844, "longitude": -106.6504, "population": 560000, "country": "United States"},
        {"name": "Dallas", "latitude": 32.7767, "longitude": -96.7970, "population": 1340000, "country": "United States"},
        {"name": "Houston", "latitude": 29.7604, "longitude": -95.3698, "population": 2300000, "country": "United States"},
        {"name": "San Antonio", "latitude": 29.4241, "longitude": -98.4936, "population": 1550000, "country": "United States"},
        {"name": "Austin", "latitude": 30.2672, "longitude": -97.7431, "population": 965000, "country": "United States"},
        {"name": "New Orleans", "latitude": 29.9511, "longitude": -90.0715, "population": 390000, "country": "United States"},
        {"name": "Atlanta", "latitude": 33.7490, "longitude": -84.3880, "population": 500000, "country": "United States"},
        {"name": "Miami", "latitude": 25.7617, "longitude": -80.1918, "population": 470000, "country": "United States"},
        {"name": "Tampa", "latitude": 27.9506, "longitude": -82.4572, "population": 385000, "country": "United States"},
        {"name": "Jacksonville", "latitude": 30.3322, "longitude": -81.6557, "population": 950000, "country": "United States"},
        {"name": "Orlando", "latitude": 28.5383, "longitude": -81.3792, "population": 285000, "country": "United States"},
        {"name": "Charlotte", "latitude": 35.2271, "longitude": -80.8431, "population": 875000, "country": "United States"},
        {"name": "Raleigh", "latitude": 35.7796, "longitude": -78.6382, "population": 470000, "country": "United States"},
        {"name": "Washington DC", "latitude": 38.9072, "longitude": -77.0369, "population": 705000, "country": "United States"},
        {"name": "Baltimore", "latitude": 39.2904, "longitude": -76.6122, "population": 585000, "country": "United States"},
        {"name": "Nashville", "latitude": 36.1627, "longitude": -86.7816, "population": 695000, "country": "United States"},
        {"name": "Memphis", "latitude": 35.1495, "longitude": -90.0490, "population": 650000, "country": "United States"},
        {"name": "Louisville", "latitude": 38.2527, "longitude": -85.7585, "population": 620000, "country": "United States"},
        {"name": "Cincinnati", "latitude": 39.1031, "longitude": -84.5120, "population": 310000, "country": "United States"},
        {"name": "Columbus", "latitude": 39.9612, "longitude": -82.9988, "population": 895000, "country": "United States"},
        {"name": "Indianapolis", "latitude": 39.7684, "longitude": -86.1581, "population": 875000, "country": "United States"},
        {"name": "Kansas City", "latitude": 39.0997, "longitude": -94.5786, "population": 495000, "country": "United States"},
        {"name": "St. Louis", "latitude": 38.6270, "longitude": -90.1994, "population": 305000, "country": "United States"},
        {"name": "Oklahoma City", "latitude": 35.4676, "longitude": -97.5164, "population": 695000, "country": "United States"},
        
        # MEXICO - Major cities
        {"name": "Mexico City", "latitude": 19.4326, "longitude": -99.1332, "population": 21581000, "country": "Mexico"},
        {"name": "Guadalajara", "latitude": 20.6597, "longitude": -103.3496, "population": 5023000, "country": "Mexico"},
        {"name": "Monterrey", "latitude": 25.6866, "longitude": -100.3161, "population": 4689000, "country": "Mexico"},
        {"name": "Puebla", "latitude": 19.0414, "longitude": -98.2063, "population": 3344000, "country": "Mexico"},
        {"name": "Tijuana", "latitude": 32.5027, "longitude": -117.0039, "population": 1810000, "country": "Mexico"},
        {"name": "León", "latitude": 21.1619, "longitude": -101.6921, "population": 1238000, "country": "Mexico"},
        {"name": "Juárez", "latitude": 31.6904, "longitude": -106.4245, "population": 1512000, "country": "Mexico"},
        {"name": "Chihuahua", "latitude": 28.6353, "longitude": -106.0889, "population": 925000, "country": "Mexico"},
        {"name": "Cancún", "latitude": 21.1619, "longitude": -86.8515, "population": 888000, "country": "Mexico"},
        {"name": "Mérida", "latitude": 20.9674, "longitude": -89.5926, "population": 973000, "country": "Mexico"},
        {"name": "Veracruz", "latitude": 19.1738, "longitude": -96.1342, "population": 607000, "country": "Mexico"},
        {"name": "Acapulco", "latitude": 16.8531, "longitude": -99.8237, "population": 779000, "country": "Mexico"},
    ]
    
    return pd.DataFrame(cities)

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
            'day_length': f"{int(daylight_duration)}:{int((daylight_duration % 1) * 60):02d}:{int(((daylight_duration % 1) * 60 % 1) * 60):02d}",
            'status': 'success'
        }
    except Exception as e:
        error_msg = str(e)
        logger.warning(f"Error calculating daylight for {city_name}: {error_msg}")
        
        # Handle polar day/night situations manually
        if "never reaches" in error_msg.lower():
            if lat > 60:  # High northern latitude during summer solstice
                logger.info(f"Assuming polar day (24h daylight) for {city_name} at {lat:.2f}°N")
                return {
                    'sunrise': "00:00:00",
                    'sunset': "23:59:59", 
                    'daylight_hours': 24.0,
                    'day_length': "24:00:00",
                    'status': 'polar_day'
                }
        
        # For other errors, return zero
        return {
            'sunrise': None,
            'sunset': None,
            'daylight_hours': 0.0,
            'day_length': "0:00:00",
            'status': f'error: {error_msg}'
        }

def main():
    """Main analysis function"""
    # Summer solstice 2024 date
    solstice_date = date(2024, 6, 20)
    
    logger.info("=== NORTH AMERICAN SUMMER SOLSTICE 2024 DAYLIGHT ANALYSIS ===")
    logger.info(f"Analyzing North American cities for {solstice_date}")
    
    # Load city data
    cities_df = get_north_american_cities()
    logger.info(f"Loaded {len(cities_df)} North American cities")
    
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
            'day_length': daylight_info['day_length'],
            'status': daylight_info.get('status', 'unknown')
        })
    
    # Create results dataframe
    results_df = pd.DataFrame(daylight_data)
    
    # Sort by daylight hours (descending) and then by population for ties
    results_df = results_df.sort_values(['daylight_hours', 'population'], ascending=[False, False])
    
    # Save to CSV
    output_file = f"north_america_summer_solstice_2024_all_cities.csv"
    results_df.to_csv(output_file, index=False)
    
    # Display results
    print("\n" + "="*130)
    print("NORTH AMERICAN CITIES RANKED BY DAYLIGHT ON SUMMER SOLSTICE 2024 (June 20)")
    print("="*130)
    
    display_df = results_df[['name', 'country', 'population', 'latitude', 'daylight_hours', 'sunrise', 'sunset', 'status']].copy()
    display_df['population'] = display_df['population'].apply(lambda x: f"{x:,}")
    display_df['daylight_hours'] = display_df['daylight_hours'].apply(lambda x: f"{x:.2f}h")
    display_df['latitude'] = display_df['latitude'].apply(lambda x: f"{x:.2f}°N")
    
    # Add rank column
    display_df.insert(0, 'rank', range(1, len(display_df) + 1))
    
    print(display_df.to_string(index=False, max_colwidth=20))
    
    print(f"\n🌞 WINNER: {results_df.iloc[0]['name']}, {results_df.iloc[0]['country']}")
    print(f"   Daylight: {results_df.iloc[0]['daylight_hours']:.2f} hours")
    print(f"   Latitude: {results_df.iloc[0]['latitude']:.2f}°N")
    print(f"   Population: {results_df.iloc[0]['population']:,}")
    print(f"   Status: {results_df.iloc[0]['status']}")
    
    print(f"\n📊 Results saved to: {output_file}")
    print(f"🌍 Total North American cities analyzed: {len(cities_df)}")
    
    # Show breakdown by country
    print(f"\n🌎 BREAKDOWN BY COUNTRY:")
    for country in ['Canada', 'United States', 'Mexico']:
        country_cities = results_df[results_df['country'] == country]
        if len(country_cities) > 0:
            print(f"\n🏁 TOP {country.upper()} CITIES:")
            for idx, row in country_cities.head(10).iterrows():
                rank = results_df.index.get_loc(idx) + 1
                print(f"   #{rank}: {row['name']} - {row['daylight_hours']:.2f}h (lat: {row['latitude']:.2f}°N)")
    
    # Show polar day cities
    polar_cities = results_df[results_df['status'] == 'polar_day']
    if len(polar_cities) > 0:
        print(f"\n☀️ POLAR DAY CITIES (24h daylight):")
        for idx, row in polar_cities.iterrows():
            rank = results_df.index.get_loc(idx) + 1
            print(f"   #{rank}: {row['name']}, {row['country']} (lat: {row['latitude']:.2f}°N)")

if __name__ == "__main__":
    main()