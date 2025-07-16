import requests
import json
import subprocess
import platform
import re

class LocationDetector:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.city = None
        self.country = None
        self.accuracy = None
    
    def get_location_macos_wifi(self):
        """
        Get location using macOS Core Location (WiFi/Bluetooth based)
        Requires macOS and location services enabled
        """
        try:
            # Use macOS's built-in location service
            result = subprocess.run(
                ['python3', '-c', '''
import CoreLocation
import time

class LocationDelegate:
    def __init__(self):
        self.location = None
        self.error = None
    
    def locationManager_didUpdateLocations_(self, manager, locations):
        if locations:
            self.location = locations.lastObject()
            manager.stopUpdatingLocation()
    
    def locationManager_didFailWithError_(self, manager, error):
        self.error = error
        manager.stopUpdatingLocation()

# Try to get location
from Foundation import NSObject
from CoreLocation import CLLocationManager

class LocationDelegate(NSObject):
    def locationManager_didUpdateLocations_(self, manager, locations):
        if locations:
            location = locations.lastObject()
            print(f"{location.coordinate().latitude},{location.coordinate().longitude}")
            manager.stopUpdatingLocation()
    
    def locationManager_didFailWithError_(self, manager, error):
        print(f"ERROR: {error}")
        manager.stopUpdatingLocation()

manager = CLLocationManager.alloc().init()
delegate = LocationDelegate.alloc().init()
manager.setDelegate_(delegate)
manager.setDesiredAccuracy_(100)  # 100 meters
manager.requestWhenInUseAuthorization()
manager.startUpdatingLocation()

# Wait for location
for i in range(50):  # Wait up to 5 seconds
    time.sleep(0.1)
    if delegate.location or delegate.error:
        break

if delegate.location:
    coord = delegate.location.coordinate()
    print(f"{coord.latitude},{coord.longitude}")
else:
    print("ERROR: Could not get location")
'''],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and ',' in result.stdout:
                coords = result.stdout.strip().split(',')
                if len(coords) == 2:
                    self.latitude = float(coords[0])
                    self.longitude = float(coords[1])
                    return True
                    
        except Exception as e:
            print(f"macOS location detection failed: {e}")
            
        return False
    
    def get_location_ip_geolocation(self):
        """
        Get approximate location using IP geolocation
        Less accurate but works without GPS
        """
        try:
            # Try multiple IP geolocation services
            services = [
                'http://ip-api.com/json',
                'https://ipapi.co/json',
                'https://ipinfo.io/json'
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Handle different API response formats
                        if service == 'http://ip-api.com/json':
                            if data.get('status') == 'success':
                                self.latitude = data.get('lat')
                                self.longitude = data.get('lon')
                                self.city = data.get('city')
                                self.country = data.get('country')
                                self.accuracy = "IP-based (~city level)"
                                return True
                        
                        elif service == 'https://ipapi.co/json':
                            if 'latitude' in data and 'longitude' in data:
                                self.latitude = data.get('latitude')
                                self.longitude = data.get('longitude')
                                self.city = data.get('city')
                                self.country = data.get('country_name')
                                self.accuracy = "IP-based (~city level)"
                                return True
                        
                        elif service == 'https://ipinfo.io/json':
                            if 'loc' in data:
                                coords = data['loc'].split(',')
                                if len(coords) == 2:
                                    self.latitude = float(coords[0])
                                    self.longitude = float(coords[1])
                                    self.city = data.get('city')
                                    self.country = data.get('country')
                                    self.accuracy = "IP-based (~city level)"
                                    return True
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"IP geolocation failed: {e}")
            
        return False
    
    def get_location_manual_input(self):
        """
        Fallback: Ask user for manual input
        """
        try:
            print("\nAutomatic location detection failed.")
            print("Please enter your location manually:")
            
            lat_input = input("Enter your latitude (e.g., 40.7128): ")
            lon_input = input("Enter your longitude (e.g., -74.0060): ")
            
            self.latitude = float(lat_input)
            self.longitude = float(lon_input)
            self.city = input("Enter your city name (optional): ") or "Manual Location"
            self.accuracy = "Manual input"
            
            return True
            
        except (ValueError, KeyboardInterrupt):
            return False
    
    def detect_location(self, fallback_to_manual=True):
        """
        Try multiple methods to detect location
        
        Args:
            fallback_to_manual: If True, ask user for manual input if auto-detection fails
            
        Returns:
            bool: True if location was successfully detected
        """
        print("Detecting your location...")
        
        # Method 1: Try macOS Core Location (most accurate)
        if platform.system() == 'Darwin':  # macOS
            print("Trying macOS location services...")
            if self.get_location_macos_wifi():
                self.accuracy = "GPS/WiFi-based (high accuracy)"
                print(f"✓ Location detected via macOS location services")
                return True
        
        # Method 2: Try IP geolocation (less accurate but works everywhere)
        print("Trying IP geolocation...")
        if self.get_location_ip_geolocation():
            print(f"✓ Location detected via IP geolocation")
            return True
        
        # Method 3: Manual input as fallback
        if fallback_to_manual:
            return self.get_location_manual_input()
        
        return False
    
    def get_location_info(self):
        """
        Get detected location information
        
        Returns:
            dict: Location information
        """
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'city': self.city,
            'country': self.country,
            'accuracy': self.accuracy
        }
    
    def print_location_info(self):
        """
        Print detected location information
        """
        if self.latitude is not None and self.longitude is not None:
            print(f"\n📍 Location Details:")
            print(f"  Latitude: {self.latitude:.4f}°")
            print(f"  Longitude: {self.longitude:.4f}°")
            if self.city:
                print(f"  City: {self.city}")
            if self.country:
                print(f"  Country: {self.country}")
            if self.accuracy:
                print(f"  Accuracy: {self.accuracy}")
        else:
            print("❌ No location detected")

