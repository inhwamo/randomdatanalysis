#!/usr/bin/env python3
"""
Asian cities ranked by daylight on Summer Solstice 2024 (June 20)
"""
import pandas as pd
from datetime import date
from astral import LocationInfo
from astral.sun import sun
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_asian_cities():
    """Load comprehensive Asian city data"""
    cities = [
        # RUSSIA (Asian part) - Siberian cities
        {"name": "Yakutsk", "latitude": 62.0397, "longitude": 129.7322, "population": 269000, "country": "Russia (Siberia)"},
        {"name": "Magadan", "latitude": 59.5684, "longitude": 150.8048, "population": 95000, "country": "Russia (Siberia)"},
        {"name": "Norilsk", "latitude": 69.3558, "longitude": 88.1893, "population": 175000, "country": "Russia (Siberia)"},
        {"name": "Surgut", "latitude": 61.2500, "longitude": 73.4167, "population": 360000, "country": "Russia (Siberia)"},
        {"name": "Nizhnevartovsk", "latitude": 60.9344, "longitude": 76.5531, "population": 251000, "country": "Russia (Siberia)"},
        {"name": "Khanty-Mansiysk", "latitude": 61.0042, "longitude": 69.0019, "population": 83000, "country": "Russia (Siberia)"},
        {"name": "Omsk", "latitude": 54.9885, "longitude": 73.3242, "population": 1154000, "country": "Russia (Siberia)"},
        {"name": "Novosibirsk", "latitude": 55.0084, "longitude": 82.9357, "population": 1612000, "country": "Russia (Siberia)"},
        {"name": "Krasnoyarsk", "latitude": 56.0184, "longitude": 92.8672, "population": 1083000, "country": "Russia (Siberia)"},
        {"name": "Irkutsk", "latitude": 52.2978, "longitude": 104.2964, "population": 623000, "country": "Russia (Siberia)"},
        {"name": "Ulan-Ude", "latitude": 51.8272, "longitude": 107.6063, "population": 432000, "country": "Russia (Siberia)"},
        {"name": "Chita", "latitude": 52.0307, "longitude": 113.5006, "population": 324000, "country": "Russia (Siberia)"},
        {"name": "Vladivostok", "latitude": 43.1056, "longitude": 131.8735, "population": 606000, "country": "Russia (Far East)"},
        {"name": "Khabarovsk", "latitude": 48.4827, "longitude": 135.0839, "population": 618000, "country": "Russia (Far East)"},
        {"name": "Yuzhno-Sakhalinsk", "latitude": 46.9588, "longitude": 142.7386, "population": 181000, "country": "Russia (Far East)"},
        
        # CHINA - Major cities
        {"name": "Harbin", "latitude": 45.8038, "longitude": 126.5349, "population": 5878000, "country": "China"},
        {"name": "Changchun", "latitude": 43.8171, "longitude": 125.3235, "population": 4413000, "country": "China"},
        {"name": "Shenyang", "latitude": 41.8057, "longitude": 123.4315, "population": 6921000, "country": "China"},
        {"name": "Dalian", "latitude": 38.9140, "longitude": 121.6147, "population": 3990000, "country": "China"},
        {"name": "Beijing", "latitude": 39.9042, "longitude": 116.4074, "population": 19618000, "country": "China"},
        {"name": "Tianjin", "latitude": 39.3434, "longitude": 117.3616, "population": 13215000, "country": "China"},
        {"name": "Jinan", "latitude": 36.6512, "longitude": 117.1201, "population": 4335000, "country": "China"},
        {"name": "Qingdao", "latitude": 36.0986, "longitude": 120.3719, "population": 4346000, "country": "China"},
        {"name": "Xi'an", "latitude": 34.3416, "longitude": 108.9398, "population": 8505000, "country": "China"},
        {"name": "Zhengzhou", "latitude": 34.7466, "longitude": 113.6253, "population": 4253000, "country": "China"},
        {"name": "Nanjing", "latitude": 32.0603, "longitude": 118.7969, "population": 8505000, "country": "China"},
        {"name": "Shanghai", "latitude": 31.2304, "longitude": 121.4737, "population": 24256800, "country": "China"},
        {"name": "Hangzhou", "latitude": 30.2741, "longitude": 120.1551, "population": 7236000, "country": "China"},
        {"name": "Wuhan", "latitude": 30.5928, "longitude": 114.3055, "population": 11081000, "country": "China"},
        {"name": "Chengdu", "latitude": 30.5728, "longitude": 104.0668, "population": 10704000, "country": "China"},
        {"name": "Chongqing", "latitude": 29.4316, "longitude": 106.9123, "population": 14838000, "country": "China"},
        {"name": "Changsha", "latitude": 28.2282, "longitude": 112.9388, "population": 4074000, "country": "China"},
        {"name": "Nanchang", "latitude": 28.6820, "longitude": 115.8581, "population": 2357000, "country": "China"},
        {"name": "Fuzhou", "latitude": 26.0745, "longitude": 119.2965, "population": 2824000, "country": "China"},
        {"name": "Guangzhou", "latitude": 23.1291, "longitude": 113.2644, "population": 13858000, "country": "China"},
        {"name": "Shenzhen", "latitude": 22.5431, "longitude": 114.0579, "population": 12356000, "country": "China"},
        {"name": "Hong Kong", "latitude": 22.3193, "longitude": 114.1694, "population": 7496000, "country": "Hong Kong"},
        {"name": "Macau", "latitude": 22.1987, "longitude": 113.5439, "population": 650000, "country": "Macau"},
        
        # MONGOLIA
        {"name": "Ulaanbaatar", "latitude": 47.8864, "longitude": 106.9057, "population": 1372000, "country": "Mongolia"},
        
        # JAPAN - Major cities
        {"name": "Sapporo", "latitude": 43.0642, "longitude": 141.3469, "population": 1973000, "country": "Japan"},
        {"name": "Sendai", "latitude": 38.2682, "longitude": 140.8694, "population": 1096000, "country": "Japan"},
        {"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503, "population": 37400068, "country": "Japan"},
        {"name": "Yokohama", "latitude": 35.4437, "longitude": 139.6380, "population": 3748000, "country": "Japan"},
        {"name": "Nagoya", "latitude": 35.1815, "longitude": 136.9066, "population": 2296000, "country": "Japan"},
        {"name": "Kyoto", "latitude": 35.0116, "longitude": 135.7681, "population": 1475000, "country": "Japan"},
        {"name": "Osaka", "latitude": 34.6937, "longitude": 135.5023, "population": 19281000, "country": "Japan"},
        {"name": "Kobe", "latitude": 34.6901, "longitude": 135.1956, "population": 1518000, "country": "Japan"},
        {"name": "Hiroshima", "latitude": 34.3853, "longitude": 132.4553, "population": 1194000, "country": "Japan"},
        {"name": "Fukuoka", "latitude": 33.5904, "longitude": 130.4017, "population": 1581000, "country": "Japan"},
        
        # SOUTH KOREA
        {"name": "Seoul", "latitude": 37.5665, "longitude": 126.9780, "population": 9776000, "country": "South Korea"},
        {"name": "Busan", "latitude": 35.1796, "longitude": 129.0756, "population": 3449000, "country": "South Korea"},
        {"name": "Incheon", "latitude": 37.4563, "longitude": 126.7052, "population": 2954000, "country": "South Korea"},
        {"name": "Daegu", "latitude": 35.8714, "longitude": 128.6014, "population": 2466000, "country": "South Korea"},
        {"name": "Daejeon", "latitude": 36.3504, "longitude": 127.3845, "population": 1539000, "country": "South Korea"},
        {"name": "Gwangju", "latitude": 35.1595, "longitude": 126.8526, "population": 1469000, "country": "South Korea"},
        
        # NORTH KOREA
        {"name": "Pyongyang", "latitude": 39.0392, "longitude": 125.7625, "population": 3038000, "country": "North Korea"},
        
        # TAIWAN
        {"name": "Taipei", "latitude": 25.0330, "longitude": 121.5654, "population": 2646000, "country": "Taiwan"},
        {"name": "Kaohsiung", "latitude": 22.6273, "longitude": 120.3014, "population": 2773000, "country": "Taiwan"},
        {"name": "Taichung", "latitude": 24.1477, "longitude": 120.6736, "population": 2817000, "country": "Taiwan"},
        
        # CENTRAL ASIA
        {"name": "Almaty", "latitude": 43.2220, "longitude": 76.8512, "population": 1916000, "country": "Kazakhstan"},
        {"name": "Nur-Sultan (Astana)", "latitude": 51.1801, "longitude": 71.4460, "population": 1136000, "country": "Kazakhstan"},
        {"name": "Tashkent", "latitude": 41.2995, "longitude": 69.2401, "population": 2506000, "country": "Uzbekistan"},
        {"name": "Samarkand", "latitude": 39.6542, "longitude": 66.9597, "population": 509000, "country": "Uzbekistan"},
        {"name": "Bishkek", "latitude": 42.8746, "longitude": 74.5698, "population": 1012000, "country": "Kyrgyzstan"},
        {"name": "Dushanbe", "latitude": 38.5598, "longitude": 68.7870, "population": 846000, "country": "Tajikistan"},
        {"name": "Ashgabat", "latitude": 37.9601, "longitude": 58.3261, "population": 1031000, "country": "Turkmenistan"},
        
        # SOUTH ASIA
        {"name": "Islamabad", "latitude": 33.7294, "longitude": 73.0931, "population": 1061000, "country": "Pakistan"},
        {"name": "Lahore", "latitude": 31.5204, "longitude": 74.3587, "population": 11126000, "country": "Pakistan"},
        {"name": "Karachi", "latitude": 24.8607, "longitude": 67.0011, "population": 15400000, "country": "Pakistan"},
        {"name": "Faisalabad", "latitude": 31.4504, "longitude": 73.1350, "population": 3204000, "country": "Pakistan"},
        {"name": "Rawalpindi", "latitude": 33.5651, "longitude": 73.0169, "population": 2098000, "country": "Pakistan"},
        {"name": "Peshawar", "latitude": 34.0151, "longitude": 71.5249, "population": 1970000, "country": "Pakistan"},
        {"name": "Delhi", "latitude": 28.7041, "longitude": 77.1025, "population": 28514000, "country": "India"},
        {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777, "population": 19980000, "country": "India"},
        {"name": "Kolkata", "latitude": 22.5726, "longitude": 88.3639, "population": 14681000, "country": "India"},
        {"name": "Bangalore", "latitude": 12.9716, "longitude": 77.5946, "population": 12765000, "country": "India"},
        {"name": "Chennai", "latitude": 13.0827, "longitude": 80.2707, "population": 10971000, "country": "India"},
        {"name": "Hyderabad", "latitude": 17.3850, "longitude": 78.4867, "population": 9746000, "country": "India"},
        {"name": "Ahmedabad", "latitude": 23.0225, "longitude": 72.5714, "population": 7692000, "country": "India"},
        {"name": "Pune", "latitude": 18.5204, "longitude": 73.8567, "population": 6629000, "country": "India"},
        {"name": "Surat", "latitude": 21.1702, "longitude": 72.8311, "population": 6564000, "country": "India"},
        {"name": "Jaipur", "latitude": 26.9124, "longitude": 75.7873, "population": 3046000, "country": "India"},
        {"name": "Lucknow", "latitude": 26.8467, "longitude": 80.9462, "population": 2902000, "country": "India"},
        {"name": "Kanpur", "latitude": 26.4499, "longitude": 80.3319, "population": 2767000, "country": "India"},
        {"name": "Nagpur", "latitude": 21.1458, "longitude": 79.0882, "population": 2405000, "country": "India"},
        {"name": "Indore", "latitude": 22.7196, "longitude": 75.8577, "population": 2170000, "country": "India"},
        {"name": "Dhaka", "latitude": 23.8103, "longitude": 90.4125, "population": 19578000, "country": "Bangladesh"},
        {"name": "Chittagong", "latitude": 22.3569, "longitude": 91.7832, "population": 2592000, "country": "Bangladesh"},
        {"name": "Khulna", "latitude": 22.8456, "longitude": 89.5403, "population": 664000, "country": "Bangladesh"},
        {"name": "Colombo", "latitude": 6.9271, "longitude": 79.8612, "population": 753000, "country": "Sri Lanka"},
        {"name": "Kathmandu", "latitude": 27.7172, "longitude": 85.3240, "population": 1442000, "country": "Nepal"},
        {"name": "Thimphu", "latitude": 27.4728, "longitude": 89.6390, "population": 115000, "country": "Bhutan"},
        {"name": "Kabul", "latitude": 34.5553, "longitude": 69.2075, "population": 4434550, "country": "Afghanistan"},
        
        # SOUTHEAST ASIA
        {"name": "Bangkok", "latitude": 13.7563, "longitude": 100.5018, "population": 10156000, "country": "Thailand"},
        {"name": "Chiang Mai", "latitude": 18.7883, "longitude": 98.9853, "population": 131000, "country": "Thailand"},
        {"name": "Hanoi", "latitude": 21.0285, "longitude": 105.8542, "population": 4377000, "country": "Vietnam"},
        {"name": "Ho Chi Minh City", "latitude": 10.8231, "longitude": 106.6297, "population": 8993000, "country": "Vietnam"},
        {"name": "Da Nang", "latitude": 16.0544, "longitude": 108.2022, "population": 1007000, "country": "Vietnam"},
        {"name": "Phnom Penh", "latitude": 11.5564, "longitude": 104.9282, "population": 1731000, "country": "Cambodia"},
        {"name": "Vientiane", "latitude": 17.9757, "longitude": 102.6331, "population": 240000, "country": "Laos"},
        {"name": "Yangon", "latitude": 16.8661, "longitude": 96.1951, "population": 5209000, "country": "Myanmar"},
        {"name": "Naypyidaw", "latitude": 19.7633, "longitude": 96.1292, "population": 924000, "country": "Myanmar"},
        {"name": "Manila", "latitude": 14.5995, "longitude": 120.9842, "population": 13482000, "country": "Philippines"},
        {"name": "Quezon City", "latitude": 14.6760, "longitude": 121.0437, "population": 2936000, "country": "Philippines"},
        {"name": "Cebu City", "latitude": 10.3157, "longitude": 123.8854, "population": 922000, "country": "Philippines"},
        {"name": "Davao", "latitude": 7.0731, "longitude": 125.6128, "population": 1776000, "country": "Philippines"},
        {"name": "Jakarta", "latitude": -6.2088, "longitude": 106.8456, "population": 10560000, "country": "Indonesia"},
        {"name": "Surabaya", "latitude": -7.2575, "longitude": 112.7521, "population": 2874000, "country": "Indonesia"},
        {"name": "Bandung", "latitude": -6.9175, "longitude": 107.6191, "population": 2444000, "country": "Indonesia"},
        {"name": "Medan", "latitude": 3.5952, "longitude": 98.6722, "population": 2210624, "country": "Indonesia"},
        {"name": "Semarang", "latitude": -6.9666, "longitude": 110.4167, "population": 1653524, "country": "Indonesia"},
        {"name": "Kuala Lumpur", "latitude": 3.1390, "longitude": 101.6869, "population": 1768000, "country": "Malaysia"},
        {"name": "George Town", "latitude": 5.4164, "longitude": 100.3327, "population": 708127, "country": "Malaysia"},
        {"name": "Johor Bahru", "latitude": 1.4927, "longitude": 103.7414, "population": 497067, "country": "Malaysia"},
        {"name": "Singapore", "latitude": 1.3521, "longitude": 103.8198, "population": 5850000, "country": "Singapore"},
        {"name": "Bandar Seri Begawan", "latitude": 4.9031, "longitude": 114.9398, "population": 100700, "country": "Brunei"},
        
        # MIDDLE EAST (Asian part)
        {"name": "Tehran", "latitude": 35.6892, "longitude": 51.3890, "population": 8693706, "country": "Iran"},
        {"name": "Mashhad", "latitude": 36.2605, "longitude": 59.6168, "population": 3001184, "country": "Iran"},
        {"name": "Isfahan", "latitude": 32.6546, "longitude": 51.6680, "population": 1961260, "country": "Iran"},
        {"name": "Tabriz", "latitude": 38.0962, "longitude": 46.2738, "population": 1558693, "country": "Iran"},
        {"name": "Shiraz", "latitude": 29.5918, "longitude": 52.5837, "population": 1565572, "country": "Iran"},
        {"name": "Baghdad", "latitude": 33.3152, "longitude": 44.3661, "population": 6719477, "country": "Iraq"},
        {"name": "Basra", "latitude": 30.5085, "longitude": 47.7804, "population": 2600000, "country": "Iraq"},
        {"name": "Riyadh", "latitude": 24.7136, "longitude": 46.6753, "population": 7231447, "country": "Saudi Arabia"},
        {"name": "Jeddah", "latitude": 21.4858, "longitude": 39.1925, "population": 4697000, "country": "Saudi Arabia"},
        {"name": "Mecca", "latitude": 21.3891, "longitude": 39.8579, "population": 1675368, "country": "Saudi Arabia"},
        {"name": "Medina", "latitude": 24.5247, "longitude": 39.5692, "population": 1300000, "country": "Saudi Arabia"},
        {"name": "Dubai", "latitude": 25.2048, "longitude": 55.2708, "population": 3355000, "country": "UAE"},
        {"name": "Abu Dhabi", "latitude": 24.4539, "longitude": 54.3773, "population": 1482000, "country": "UAE"},
        {"name": "Kuwait City", "latitude": 29.3759, "longitude": 47.9774, "population": 2989000, "country": "Kuwait"},
        {"name": "Doha", "latitude": 25.2854, "longitude": 51.5310, "population": 2382000, "country": "Qatar"},
        {"name": "Manama", "latitude": 26.2285, "longitude": 50.5860, "population": 329510, "country": "Bahrain"},
        {"name": "Muscat", "latitude": 23.5859, "longitude": 58.4059, "population": 1560330, "country": "Oman"},
        {"name": "Sanaa", "latitude": 15.3694, "longitude": 44.1910, "population": 2957000, "country": "Yemen"},
        {"name": "Amman", "latitude": 31.9539, "longitude": 35.9106, "population": 4007526, "country": "Jordan"},
        {"name": "Damascus", "latitude": 33.5138, "longitude": 36.2765, "population": 1711000, "country": "Syria"},
        {"name": "Aleppo", "latitude": 36.2021, "longitude": 37.1343, "population": 2098210, "country": "Syria"},
        {"name": "Beirut", "latitude": 33.8938, "longitude": 35.5018, "population": 361366, "country": "Lebanon"},
        {"name": "Tel Aviv", "latitude": 32.0853, "longitude": 34.7818, "population": 460613, "country": "Israel"},
        {"name": "Jerusalem", "latitude": 31.7683, "longitude": 35.2137, "population": 874186, "country": "Israel"},
        {"name": "Yerevan", "latitude": 40.1792, "longitude": 44.4991, "population": 1086000, "country": "Armenia"},
        {"name": "Baku", "latitude": 40.4093, "longitude": 49.8671, "population": 2303000, "country": "Azerbaijan"},
        {"name": "Tbilisi", "latitude": 41.7151, "longitude": 44.8271, "population": 1118000, "country": "Georgia"},
        
        # MALDIVES
        {"name": "Malé", "latitude": 4.1755, "longitude": 73.5093, "population": 133412, "country": "Maldives"},
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
    
    logger.info("=== ASIAN SUMMER SOLSTICE 2024 DAYLIGHT ANALYSIS ===")
    logger.info(f"Analyzing Asian cities for {solstice_date}")
    
    # Load city data
    cities_df = get_asian_cities()
    logger.info(f"Loaded {len(cities_df)} Asian cities")
    
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
    output_file = f"asia_summer_solstice_2024_all_cities.csv"
    results_df.to_csv(output_file, index=False)
    
    # Display results
    print("\n" + "="*130)
    print("ASIAN CITIES RANKED BY DAYLIGHT ON SUMMER SOLSTICE 2024 (June 20)")
    print("="*130)
    
    display_df = results_df[['name', 'country', 'population', 'latitude', 'daylight_hours', 'sunrise', 'sunset', 'status']].copy()
    display_df['population'] = display_df['population'].apply(lambda x: f"{x:,}")
    display_df['daylight_hours'] = display_df['daylight_hours'].apply(lambda x: f"{x:.2f}h")
    display_df['latitude'] = display_df['latitude'].apply(lambda x: f"{x:.2f}°{'N' if x >= 0 else 'S'}")
    
    # Add rank column
    display_df.insert(0, 'rank', range(1, len(display_df) + 1))
    
    print(display_df.to_string(index=False, max_colwidth=20))
    
    print(f"\n🌞 WINNER: {results_df.iloc[0]['name']}, {results_df.iloc[0]['country']}")
    print(f"   Daylight: {results_df.iloc[0]['daylight_hours']:.2f} hours")
    print(f"   Latitude: {results_df.iloc[0]['latitude']:.2f}°{'N' if results_df.iloc[0]['latitude'] >= 0 else 'S'}")
    print(f"   Population: {results_df.iloc[0]['population']:,}")
    print(f"   Status: {results_df.iloc[0]['status']}")
    
    print(f"\n📊 Results saved to: {output_file}")
    print(f"🌍 Total Asian cities analyzed: {len(cities_df)}")
    
    # Show breakdown by major regions
    print(f"\n🌎 BREAKDOWN BY REGION:")
    regions = {
        'China': ['China', 'Hong Kong', 'Macau'],
        'Russia (Siberia/Far East)': ['Russia (Siberia)', 'Russia (Far East)'],
        'South Asia': ['India', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Nepal', 'Bhutan', 'Afghanistan'],
        'Southeast Asia': ['Thailand', 'Vietnam', 'Cambodia', 'Laos', 'Myanmar', 'Philippines', 'Indonesia', 'Malaysia', 'Singapore', 'Brunei'],
        'East Asia': ['Japan', 'South Korea', 'North Korea', 'Taiwan', 'Mongolia'],
        'Central Asia': ['Kazakhstan', 'Uzbekistan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan'],
        'Middle East': ['Iran', 'Iraq', 'Saudi Arabia', 'UAE', 'Kuwait', 'Qatar', 'Bahrain', 'Oman', 'Yemen', 'Jordan', 'Syria', 'Lebanon', 'Israel', 'Armenia', 'Azerbaijan', 'Georgia']
    }
    
    for region_name, countries in regions.items():
        region_cities = results_df[results_df['country'].isin(countries)]
        if len(region_cities) > 0:
            top_city = region_cities.iloc[0]
            rank = results_df.index.get_loc(region_cities.index[0]) + 1
            print(f"\n🏁 TOP {region_name.upper()} CITY:")
            print(f"   #{rank}: {top_city['name']}, {top_city['country']} - {top_city['daylight_hours']:.2f}h (lat: {top_city['latitude']:.2f}°{'N' if top_city['latitude'] >= 0 else 'S'})")
            
            # Show top 5 in region
            top_5_region = region_cities.head(5)
            if len(top_5_region) > 1:
                print(f"   Top 5 in {region_name}:")
                for idx, row in top_5_region.iterrows():
                    rank = results_df.index.get_loc(idx) + 1
                    print(f"     #{rank}: {row['name']} - {row['daylight_hours']:.2f}h")
    
    # Show polar day cities
    polar_cities = results_df[results_df['status'] == 'polar_day']
    if len(polar_cities) > 0:
        print(f"\n☀️ POLAR DAY CITIES (24h daylight):")
        for idx, row in polar_cities.iterrows():
            rank = results_df.index.get_loc(idx) + 1
            print(f"   #{rank}: {row['name']}, {row['country']} (lat: {row['latitude']:.2f}°N)")

if __name__ == "__main__":
    main()