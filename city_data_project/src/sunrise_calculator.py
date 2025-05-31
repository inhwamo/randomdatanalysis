"""
Sunrise and sunset calculation utilities
"""
import requests
import time
from datetime import datetime, date
from typing import Dict, Optional, Tuple
import logging
from astral import LocationInfo
from astral.sun import sun
from .config import SUNRISE_SUNSET_API, RATE_LIMIT

logger = logging.getLogger(__name__)

class SunriseSunsetCalculator:
    def __init__(self):
        self.session = requests.Session()
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < (1.0 / RATE_LIMIT):
            time.sleep((1.0 / RATE_LIMIT) - elapsed)
        self.last_request_time = time.time()
    
    def get_sunrise_sunset_api(self, lat: float, lng: float, target_date: date = None) -> Dict[str, str]:
        """
        Get sunrise/sunset times using online API
        """
        if target_date is None:
            target_date = date.today()
        
        self._rate_limit()
        
        params = {
            'lat': lat,
            'lng': lng,
            'date': target_date.strftime('%Y-%m-%d'),
            'formatted': 0  # Get times in ISO format
        }
        
        try:
            response = self.session.get(SUNRISE_SUNSET_API, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                results = data['results']
                return {
                    'sunrise': results['sunrise'],
                    'sunset': results['sunset'],
                    'solar_noon': results['solar_noon'],
                    'day_length': results['day_length'],
                    'civil_twilight_begin': results['civil_twilight_begin'],
                    'civil_twilight_end': results['civil_twilight_end'],
                    'nautical_twilight_begin': results['nautical_twilight_begin'],
                    'nautical_twilight_end': results['nautical_twilight_end'],
                    'astronomical_twilight_begin': results['astronomical_twilight_begin'],
                    'astronomical_twilight_end': results['astronomical_twilight_end']
                }
            else:
                logger.warning(f"API returned status: {data['status']}")
                return {}
                
        except requests.RequestException as e:
            logger.error(f"Error calling sunrise-sunset API: {e}")
            return {}
    
    def get_sunrise_sunset_local(self, lat: float, lng: float, city_name: str = "", 
                                target_date: date = None) -> Dict[str, str]:
        """
        Calculate sunrise/sunset times using local astral library
        """
        if target_date is None:
            target_date = date.today()
        
        try:
            # Create location info
            location = LocationInfo(city_name, "", "", lat, lng)
            
            # Calculate sun times
            s = sun(location.observer, date=target_date)
            
            return {
                'sunrise': s['sunrise'].isoformat(),
                'sunset': s['sunset'].isoformat(),
                'solar_noon': s['noon'].isoformat(),
                'dawn': s['dawn'].isoformat(),
                'dusk': s['dusk'].isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating local sunrise/sunset for {city_name}: {e}")
            return {}
    
    def get_sunrise_sunset(self, lat: float, lng: float, city_name: str = "", 
                          use_api: bool = True, target_date: date = None) -> Dict[str, str]:
        """
        Get sunrise/sunset times, trying API first, then falling back to local calculation
        """
        if use_api:
            result = self.get_sunrise_sunset_api(lat, lng, target_date)
            if result:
                return result
            
            logger.info(f"API failed for {city_name}, falling back to local calculation")
        
        return self.get_sunrise_sunset_local(lat, lng, city_name, target_date)
    
    def format_time_for_timezone(self, iso_time: str, timezone_offset: int = 0) -> str:
        """
        Format ISO time string for display
        """
        try:
            dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
            return dt.strftime('%H:%M:%S')
        except Exception as e:
            logger.error(f"Error formatting time {iso_time}: {e}")
            return iso_time