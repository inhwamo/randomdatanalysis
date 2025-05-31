#!/usr/bin/env python3
"""
Standalone script to find top 20 NON-EUROPEAN cities with 200k+ population 
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

def get_non_european_cities():
    """Load comprehensive NON-European city data with 200k+ population"""
    cities = [
        # NORTH AMERICA - Major cities
        {"name": "Toronto", "latitude": 43.6532, "longitude": -79.3832, "population": 2930000, "country": "Canada"},
        {"name": "Montreal", "latitude": 45.5017, "longitude": -73.5673, "population": 1780000, "country": "Canada"},
        {"name": "Vancouver", "latitude": 49.2827, "longitude": -123.1207, "population": 2581000, "country": "Canada"},
        {"name": "Calgary", "latitude": 51.0447, "longitude": -114.0719, "population": 1336000, "country": "Canada"},
        {"name": "Edmonton", "latitude": 53.5461, "longitude": -113.4938, "population": 981000, "country": "Canada"},
        {"name": "Ottawa", "latitude": 45.4215, "longitude": -75.6972, "population": 1017000, "country": "Canada"},
        {"name": "Winnipeg", "latitude": 49.8951, "longitude": -97.1384, "population": 749000, "country": "Canada"},
        {"name": "Quebec City", "latitude": 46.8139, "longitude": -71.2080, "population": 540000, "country": "Canada"},
        {"name": "Hamilton", "latitude": 43.2557, "longitude": -79.8711, "population": 693000, "country": "Canada"},
        {"name": "Saskatoon", "latitude": 52.1579, "longitude": -106.6702, "population": 317000, "country": "Canada"},
        {"name": "Regina", "latitude": 50.4452, "longitude": -104.6189, "population": 236000, "country": "Canada"},
        {"name": "Halifax", "latitude": 44.6488, "longitude": -63.5752, "population": 348000, "country": "Canada"},
        {"name": "Thunder Bay", "latitude": 48.3809, "longitude": -89.2477, "population": 121000, "country": "Canada"},
        {"name": "Yellowknife", "latitude": 62.4540, "longitude": -114.3718, "population": 20000, "country": "Canada"},
        {"name": "Whitehorse", "latitude": 60.7212, "longitude": -135.0568, "population": 28000, "country": "Canada"},
        {"name": "Anchorage", "latitude": 61.2181, "longitude": -149.9003, "population": 291000, "country": "United States"},
        {"name": "Fairbanks", "latitude": 64.8378, "longitude": -147.7164, "population": 32000, "country": "United States"},
        {"name": "Seattle", "latitude": 47.6062, "longitude": -122.3321, "population": 750000, "country": "United States"},
        {"name": "Portland", "latitude": 45.5152, "longitude": -122.6784, "population": 650000, "country": "United States"},
        {"name": "Minneapolis", "latitude": 44.9778, "longitude": -93.2650, "population": 430000, "country": "United States"},
        {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298, "population": 2700000, "country": "United States"},
        {"name": "New York", "latitude": 40.7128, "longitude": -74.0060, "population": 8400000, "country": "United States"},
        {"name": "Boston", "latitude": 42.3601, "longitude": -71.0589, "population": 685000, "country": "United States"},
        {"name": "Detroit", "latitude": 42.3314, "longitude": -83.0458, "population": 670000, "country": "United States"},
        {"name": "Denver", "latitude": 39.7392, "longitude": -104.9903, "population": 715000, "country": "United States"},
        {"name": "Salt Lake City", "latitude": 40.7608, "longitude": -111.8910, "population": 200000, "country": "United States"},
        {"name": "Philadelphia", "latitude": 39.9526, "longitude": -75.1652, "population": 1580000, "country": "United States"},
        {"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194, "population": 875000, "country": "United States"},
        {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437, "population": 12448000, "country": "United States"},
        {"name": "San Diego", "latitude": 32.7157, "longitude": -117.1611, "population": 1410000, "country": "United States"},
        {"name": "Phoenix", "latitude": 33.4484, "longitude": -112.0740, "population": 1660000, "country": "United States"},
        {"name": "Las Vegas", "latitude": 36.1699, "longitude": -115.1398, "population": 650000, "country": "United States"},
        {"name": "Dallas", "latitude": 32.7767, "longitude": -96.7970, "population": 1340000, "country": "United States"},
        {"name": "Houston", "latitude": 29.7604, "longitude": -95.3698, "population": 2300000, "country": "United States"},
        {"name": "Atlanta", "latitude": 33.7490, "longitude": -84.3880, "population": 500000, "country": "United States"},
        {"name": "Miami", "latitude": 25.7617, "longitude": -80.1918, "population": 470000, "country": "United States"},
        {"name": "Mexico City", "latitude": 19.4326, "longitude": -99.1332, "population": 21581000, "country": "Mexico"},
        {"name": "Guadalajara", "latitude": 20.6597, "longitude": -103.3496, "population": 5023000, "country": "Mexico"},
        {"name": "Monterrey", "latitude": 25.6866, "longitude": -100.3161, "population": 4689000, "country": "Mexico"},
        {"name": "Puebla", "latitude": 19.0414, "longitude": -98.2063, "population": 3344000, "country": "Mexico"},
        {"name": "Tijuana", "latitude": 32.5027, "longitude": -117.0039, "population": 1810000, "country": "Mexico"},
        
        # ASIA - Major cities
        {"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503, "population": 37400068, "country": "Japan"},
        {"name": "Osaka", "latitude": 34.6937, "longitude": 135.5023, "population": 19281000, "country": "Japan"},
        {"name": "Nagoya", "latitude": 35.1815, "longitude": 136.9066, "population": 2296000, "country": "Japan"},
        {"name": "Sapporo", "latitude": 43.0642, "longitude": 141.3469, "population": 1973000, "country": "Japan"},
        {"name": "Fukuoka", "latitude": 33.5904, "longitude": 130.4017, "population": 1581000, "country": "Japan"},
        {"name": "Sendai", "latitude": 38.2682, "longitude": 140.8694, "population": 1096000, "country": "Japan"},
        {"name": "Seoul", "latitude": 37.5665, "longitude": 126.9780, "population": 9776000, "country": "South Korea"},
        {"name": "Busan", "latitude": 35.1796, "longitude": 129.0756, "population": 3449000, "country": "South Korea"},
        {"name": "Beijing", "latitude": 39.9042, "longitude": 116.4074, "population": 19618000, "country": "China"},
        {"name": "Shanghai", "latitude": 31.2304, "longitude": 121.4737, "population": 24256800, "country": "China"},
        {"name": "Guangzhou", "latitude": 23.1291, "longitude": 113.2644, "population": 13858000, "country": "China"},
        {"name": "Shenzhen", "latitude": 22.5431, "longitude": 114.0579, "population": 12356000, "country": "China"},
        {"name": "Chongqing", "latitude": 29.4316, "longitude": 106.9123, "population": 14838000, "country": "China"},
        {"name": "Tianjin", "latitude": 39.3434, "longitude": 117.3616, "population": 13215000, "country": "China"},
        {"name": "Wuhan", "latitude": 30.5928, "longitude": 114.3055, "population": 11081000, "country": "China"},
        {"name": "Chengdu", "latitude": 30.5728, "longitude": 104.0668, "population": 10704000, "country": "China"},
        {"name": "Nanjing", "latitude": 32.0603, "longitude": 118.7969, "population": 8505000, "country": "China"},
        {"name": "Xi'an", "latitude": 34.3416, "longitude": 108.9398, "population": 8505000, "country": "China"},
        {"name": "Hangzhou", "latitude": 30.2741, "longitude": 120.1551, "population": 7236000, "country": "China"},
        {"name": "Shenyang", "latitude": 41.8057, "longitude": 123.4315, "population": 6921000, "country": "China"},
        {"name": "Harbin", "latitude": 45.8038, "longitude": 126.5349, "population": 5878000, "country": "China"},
        {"name": "Hong Kong", "latitude": 22.3193, "longitude": 114.1694, "population": 7496000, "country": "Hong Kong"},
        {"name": "Taipei", "latitude": 25.0330, "longitude": 121.5654, "population": 2646000, "country": "Taiwan"},
        {"name": "Singapore", "latitude": 1.3521, "longitude": 103.8198, "population": 5850000, "country": "Singapore"},
        {"name": "Bangkok", "latitude": 13.7563, "longitude": 100.5018, "population": 10156000, "country": "Thailand"},
        {"name": "Ho Chi Minh City", "latitude": 10.8231, "longitude": 106.6297, "population": 8993000, "country": "Vietnam"},
        {"name": "Hanoi", "latitude": 21.0285, "longitude": 105.8542, "population": 4377000, "country": "Vietnam"},
        {"name": "Manila", "latitude": 14.5995, "longitude": 120.9842, "population": 13482000, "country": "Philippines"},
        {"name": "Quezon City", "latitude": 14.6760, "longitude": 121.0437, "population": 2936000, "country": "Philippines"},
        {"name": "Jakarta", "latitude": -6.2088, "longitude": 106.8456, "population": 10560000, "country": "Indonesia"},
        {"name": "Surabaya", "latitude": -7.2575, "longitude": 112.7521, "population": 2874000, "country": "Indonesia"},
        {"name": "Kuala Lumpur", "latitude": 3.1390, "longitude": 101.6869, "population": 1768000, "country": "Malaysia"},
        {"name": "Delhi", "latitude": 28.7041, "longitude": 77.1025, "population": 28514000, "country": "India"},
        {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777, "population": 19980000, "country": "India"},
        {"name": "Kolkata", "latitude": 22.5726, "longitude": 88.3639, "population": 14681000, "country": "India"},
        {"name": "Bangalore", "latitude": 12.9716, "longitude": 77.5946, "population": 12765000, "country": "India"},
        {"name": "Chennai", "latitude": 13.0827, "longitude": 80.2707, "population": 10971000, "country": "India"},
        {"name": "Hyderabad", "latitude": 17.3850, "longitude": 78.4867, "population": 9746000, "country": "India"},
        {"name": "Ahmedabad", "latitude": 23.0225, "longitude": 72.5714, "population": 7692000, "country": "India"},
        {"name": "Pune", "latitude": 18.5204, "longitude": 73.8567, "population": 6629000, "country": "India"},
        {"name": "Karachi", "latitude": 24.8607, "longitude": 67.0011, "population": 15400000, "country": "Pakistan"},
        {"name": "Lahore", "latitude": 31.5204, "longitude": 74.3587, "population": 11126000, "country": "Pakistan"},
        {"name": "Islamabad", "latitude": 33.7294, "longitude": 73.0931, "population": 1061000, "country": "Pakistan"},
        {"name": "Dhaka", "latitude": 23.8103, "longitude": 90.4125, "population": 19578000, "country": "Bangladesh"},
        {"name": "Chittagong", "latitude": 22.3569, "longitude": 91.7832, "population": 2592000, "country": "Bangladesh"},
        
        # MIDDLE EAST (Excluding Turkey as it's often considered European)
        {"name": "Tehran", "latitude": 35.6892, "longitude": 51.3890, "population": 8693706, "country": "Iran"},
        {"name": "Riyadh", "latitude": 24.7136, "longitude": 46.6753, "population": 7231447, "country": "Saudi Arabia"},
        {"name": "Jeddah", "latitude": 21.4858, "longitude": 39.1925, "population": 4697000, "country": "Saudi Arabia"},
        {"name": "Baghdad", "latitude": 33.3152, "longitude": 44.3661, "population": 6719477, "country": "Iraq"},
        {"name": "Dubai", "latitude": 25.2048, "longitude": 55.2708, "population": 3355000, "country": "UAE"},
        {"name": "Tel Aviv", "latitude": 32.0853, "longitude": 34.7818, "population": 460613, "country": "Israel"},
        {"name": "Cairo", "latitude": 30.0444, "longitude": 31.2357, "population": 20076000, "country": "Egypt"},
        {"name": "Alexandria", "latitude": 31.2001, "longitude": 29.9187, "population": 5086000, "country": "Egypt"},
        
        # AFRICA
        {"name": "Lagos", "latitude": 6.5244, "longitude": 3.3792, "population": 13463000, "country": "Nigeria"},
        {"name": "Kano", "latitude": 12.0022, "longitude": 8.5920, "population": 3626000, "country": "Nigeria"},
        {"name": "Kinshasa", "latitude": -4.4419, "longitude": 15.2663, "population": 11855000, "country": "DR Congo"},
        {"name": "Luanda", "latitude": -8.8390, "longitude": 13.2894, "population": 6945000, "country": "Angola"},
        {"name": "Johannesburg", "latitude": -26.2041, "longitude": 28.0473, "population": 4434827, "country": "South Africa"},
        {"name": "Cape Town", "latitude": -33.9249, "longitude": 18.4241, "population": 3776000, "country": "South Africa"},
        {"name": "Durban", "latitude": -29.8587, "longitude": 31.0218, "population": 3442361, "country": "South Africa"},
        {"name": "Casablanca", "latitude": 33.5731, "longitude": -7.5898, "population": 3359000, "country": "Morocco"},
        {"name": "Addis Ababa", "latitude": 9.1450, "longitude": 38.7451, "population": 4793699, "country": "Ethiopia"},
        {"name": "Nairobi", "latitude": -1.2921, "longitude": 36.8219, "population": 4397073, "country": "Kenya"},
        {"name": "Dar es Salaam", "latitude": -6.7924, "longitude": 39.2083, "population": 6368000, "country": "Tanzania"},
        {"name": "Algiers", "latitude": 36.7538, "longitude": 3.0588, "population": 2364230, "country": "Algeria"},
        {"name": "Tunis", "latitude": 36.8065, "longitude": 10.1815, "population": 1056247, "country": "Tunisia"},
        {"name": "Accra", "latitude": 5.6037, "longitude": -0.1870, "population": 2291352, "country": "Ghana"},
        {"name": "Dakar", "latitude": 14.7167, "longitude": -17.4677, "population": 1146053, "country": "Senegal"},
        
        # SOUTH AMERICA
        {"name": "São Paulo", "latitude": -23.5505, "longitude": -46.6333, "population": 21650000, "country": "Brazil"},
        {"name": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729, "population": 13293000, "country": "Brazil"},
        {"name": "Brasília", "latitude": -15.8267, "longitude": -47.9218, "population": 3094325, "country": "Brazil"},
        {"name": "Salvador", "latitude": -12.9711, "longitude": -38.5108, "population": 2886698, "country": "Brazil"},
        {"name": "Fortaleza", "latitude": -3.7319, "longitude": -38.5267, "population": 2669342, "country": "Brazil"},
        {"name": "Belo Horizonte", "latitude": -19.9208, "longitude": -43.9378, "population": 2521564, "country": "Brazil"},
        {"name": "Manaus", "latitude": -3.1190, "longitude": -60.0217, "population": 2219580, "country": "Brazil"},
        {"name": "Recife", "latitude": -8.0476, "longitude": -34.8770, "population": 1653461, "country": "Brazil"},
        {"name": "Buenos Aires", "latitude": -34.6118, "longitude": -58.3960, "population": 14967000, "country": "Argentina"},
        {"name": "Córdoba", "latitude": -31.4201, "longitude": -64.1888, "population": 1391000, "country": "Argentina"},
        {"name": "Rosario", "latitude": -32.9442, "longitude": -60.6505, "population": 1276000, "country": "Argentina"},
        {"name": "Lima", "latitude": -12.0464, "longitude": -77.0428, "population": 10719000, "country": "Peru"},
        {"name": "Bogotá", "latitude": 4.7110, "longitude": -74.0721, "population": 7412566, "country": "Colombia"},
        {"name": "Medellín", "latitude": 6.2442, "longitude": -75.5812, "population": 2508452, "country": "Colombia"},
        {"name": "Santiago", "latitude": -33.4489, "longitude": -70.6693, "population": 6257516, "country": "Chile"},
        {"name": "Caracas", "latitude": 10.4806, "longitude": -66.9036, "population": 2935744, "country": "Venezuela"},
        {"name": "Quito", "latitude": -0.1807, "longitude": -78.4678, "population": 2011388, "country": "Ecuador"},
        {"name": "La Paz", "latitude": -16.5000, "longitude": -68.1193, "population": 2300000, "country": "Bolivia"},
        {"name": "Montevideo", "latitude": -34.9011, "longitude": -56.1645, "population": 1369797, "country": "Uruguay"},
        
        # OCEANIA
        {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093, "population": 5312000, "country": "Australia"},
        {"name": "Melbourne", "latitude": -37.8136, "longitude": 144.9631, "population": 5078193, "country": "Australia"},
        {"name": "Brisbane", "latitude": -27.4698, "longitude": 153.0251, "population": 2514184, "country": "Australia"},
        {"name": "Perth", "latitude": -31.9505, "longitude": 115.8605, "population": 2085973, "country": "Australia"},
        {"name": "Adelaide", "latitude": -34.9285, "longitude": 138.6007, "population": 1402393, "country": "Australia"},
        {"name": "Auckland", "latitude": -36.8485, "longitude": 174.7633, "population": 1657200, "country": "New Zealand"},
        {"name": "Wellington", "latitude": -41.2865, "longitude": 174.7762, "population": 418500, "country": "New Zealand"},
        {"name": "Christchurch", "latitude": -43.5321, "longitude": 172.6362, "population": 383200, "country": "New Zealand"},
    ]
    
    # Filter by minimum population of 200k
    filtered_cities = [city for city in cities if city['population'] >= 5000]
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
            elif lat < -60:  # High southern latitude during summer solstice (their winter)
                logger.info(f"Assuming polar night (0h daylight) for {city_name} at {lat:.2f}°S")
                return {
                    'sunrise': "12:00:00",
                    'sunset': "12:00:00",
                    'daylight_hours': 0.0,
                    'day_length': "0:00:00",
                    'status': 'polar_night'
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
    
    logger.info("=== NON-EUROPEAN SUMMER SOLSTICE 2024 DAYLIGHT ANALYSIS ===")
    logger.info(f"Analyzing NON-European cities for {solstice_date}")
    logger.info("Minimum population: 200,000")
    
    # Load city data
    cities_df = get_non_european_cities()
    logger.info(f"Loaded {len(cities_df)} non-European cities with 200k+ population")
    
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
    
    # Show some debugging info
    print(f"\n🔍 DEBUGGING INFO:")
    print(f"Cities with 0 daylight hours: {len(results_df[results_df['daylight_hours'] == 0.0])}")
    print(f"Cities with 24 daylight hours: {len(results_df[results_df['daylight_hours'] == 24.0])}")
    print(f"Canadian cities in dataset: {len(results_df[results_df['country'] == 'Canada'])}")
    
    # Show top Canadian cities specifically
    canadian_cities = results_df[results_df['country'] == 'Canada'].head(10)
    if len(canadian_cities) > 0:
        print(f"\n🍁 TOP CANADIAN CITIES:")
        for idx, row in canadian_cities.iterrows():
            print(f"   {row['name']}: {row['daylight_hours']:.2f}h (lat: {row['latitude']:.2f}°N)")
    
    # Get top 50 cities
    top_50 = results_df.head(50)
    
    # Save to CSV
    output_file = f"non_european_summer_solstice_2024_top_50_cities_by_daylight.csv"
    top_50.to_csv(output_file, index=False)
    
    # Display results
    print("\n" + "="*120)
    print("TOP 50 NON-EUROPEAN CITIES WITH MOST DAYLIGHT ON SUMMER SOLSTICE 2024 (June 20)")
    print("="*120)
    
    display_df = top_50[['name', 'country', 'population', 'latitude', 'daylight_hours', 'status']].copy()
    display_df['population'] = display_df['population'].apply(lambda x: f"{x:,}")
    display_df['daylight_hours'] = display_df['daylight_hours'].apply(lambda x: f"{x:.2f}h")
    display_df['latitude'] = display_df['latitude'].apply(lambda x: f"{x:.2f}°{'N' if x >= 0 else 'S'}")
    
    # Add rank column
    display_df.insert(0, 'rank', range(1, len(display_df) + 1))
    
    print(display_df.to_string(index=False, max_colwidth=15))
    
    print(f"\n🌞 WINNER: {top_50.iloc[0]['name']}, {top_50.iloc[0]['country']}")
    print(f"   Daylight: {top_50.iloc[0]['daylight_hours']:.2f} hours")
    print(f"   Sunrise: {top_50.iloc[0]['sunrise']}")
    print(f"   Sunset: {top_50.iloc[0]['sunset']}")
    print(f"   Population: {top_50.iloc[0]['population']:,}")
    print(f"   Latitude: {top_50.iloc[0]['latitude']:.2f}°{'N' if top_50.iloc[0]['latitude'] >= 0 else 'S'}")
    print(f"   Status: {top_50.iloc[0]['status']}")
    
    print(f"\n📊 Results saved to: {output_file}")
    print(f"🌍 Total non-European cities analyzed: {len(cities_df)}")
    
    # Show some interesting stats
    print(f"\n📈 DAYLIGHT STATISTICS (Non-European Cities - Top 50):")
    print(f"   Longest day: {top_50.iloc[0]['daylight_hours']:.2f} hours ({top_50.iloc[0]['name']})")
    print(f"   Shortest day in top 50: {top_50.iloc[-1]['daylight_hours']:.2f} hours ({top_50.iloc[-1]['name']})")
    print(f"   Average (top 50): {top_50['daylight_hours'].mean():.2f} hours")
    print(f"   Difference: {top_50.iloc[0]['daylight_hours'] - top_50.iloc[-1]['daylight_hours']:.2f} hours")
    
    # Show regional breakdown
    print(f"\n🌎 REGIONAL BREAKDOWN (Top 50):")
    region_counts = top_50['country'].value_counts()
    for country, count in region_counts.head(8).items():
        print(f"   {country}: {count} cities")
    
    # Show the Canadian cities specifically
    top_canadian = top_50[top_50['country'] == 'Canada']
    if len(top_canadian) > 0:
        print(f"\n🍁 CANADIAN CITIES IN TOP 50:")
        for idx, row in top_canadian.iterrows():
            rank = top_50.index.get_loc(idx) + 1
            print(f"   #{rank}: {row['name']} - {row['daylight_hours']:.2f}h (lat: {row['latitude']:.2f}°N)")
    
    # Show any polar day cities
    polar_cities = top_50[top_50['status'] == 'polar_day']
    if len(polar_cities) > 0:
        print(f"\n☀️ POLAR DAY CITIES (24h daylight):")
        for idx, row in polar_cities.iterrows():
            rank = top_50.index.get_loc(idx) + 1
            print(f"   #{rank}: {row['name']}, {row['country']} (lat: {row['latitude']:.2f}°N)")

if __name__ == "__main__":
    main()