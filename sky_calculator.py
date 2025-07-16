import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS
from astropy.time import Time
from astropy import units as u
from skyfield.api import load, wgs84
from skyfield.data import hipparcos
from datetime import datetime, timezone
import pytz

class SkyCalculator:
    def __init__(self, latitude, longitude, elevation=0):
        """
        Initialize sky calculator for a specific location
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees 
            elevation: Elevation in meters (default: 0)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        
        # Create location object
        self.location = EarthLocation(
            lat=latitude * u.deg,
            lon=longitude * u.deg,
            height=elevation * u.m
        )
        
        # Load timescale for skyfield
        self.ts = load.timescale()
        
        # Create skyfield location
        self.skyfield_location = wgs84.latlon(latitude, longitude, elevation_m=elevation)
    
    def celestial_to_horizontal(self, ra, dec, time=None):
        """
        Convert celestial coordinates (RA/Dec) to horizontal coordinates (Alt/Az)
        
        Args:
            ra: Right ascension in degrees
            dec: Declination in degrees
            time: datetime object (default: now)
            
        Returns:
            tuple: (altitude, azimuth) in degrees
        """
        if time is None:
            time = datetime.now(timezone.utc)
        
        # Convert to astropy time
        astropy_time = Time(time)
        
        # Create sky coordinate
        sky_coord = SkyCoord(
            ra=ra * u.deg,
            dec=dec * u.deg,
            frame='icrs'
        )
        
        # Transform to horizontal coordinates
        altaz_frame = AltAz(obstime=astropy_time, location=self.location)
        altaz_coord = sky_coord.transform_to(altaz_frame)
        
        return altaz_coord.alt.deg, altaz_coord.az.deg
    
    def is_visible(self, ra, dec, time=None, min_altitude=0):
        """
        Check if a star is visible (above horizon)
        
        Args:
            ra: Right ascension in degrees
            dec: Declination in degrees
            time: datetime object (default: now)
            min_altitude: Minimum altitude in degrees (default: 0)
            
        Returns:
            bool: True if star is visible
        """
        altitude, azimuth = self.celestial_to_horizontal(ra, dec, time)
        return altitude > min_altitude
    
    def get_local_sidereal_time(self, time=None):
        """
        Calculate local sidereal time
        
        Args:
            time: datetime object (default: now)
            
        Returns:
            float: Local sidereal time in hours
        """
        if time is None:
            time = datetime.now(timezone.utc)
        
        astropy_time = Time(time)
        lst = astropy_time.sidereal_time('apparent', longitude=self.longitude * u.deg)
        return lst.hour
    
    def get_zenith_ra_dec(self, time=None):
        """
        Get RA/Dec of zenith point
        
        Args:
            time: datetime object (default: now)
            
        Returns:
            tuple: (ra, dec) in degrees
        """
        if time is None:
            time = datetime.now(timezone.utc)
        
        # Zenith is at altitude 90°, azimuth can be any value (use 0)
        altaz_coord = SkyCoord(
            alt=90 * u.deg,
            az=0 * u.deg,
            frame=AltAz(obstime=Time(time), location=self.location)
        )
        
        # Transform to celestial coordinates
        icrs_coord = altaz_coord.transform_to('icrs')
        
        return icrs_coord.ra.deg, icrs_coord.dec.deg
    
    def calculate_star_positions(self, stars, time=None):
        """
        Calculate horizontal coordinates for multiple stars
        
        Args:
            stars: Dictionary of star data with 'ra' and 'dec' keys
            time: datetime object (default: now)
            
        Returns:
            dict: Star positions with altitude and azimuth
        """
        if time is None:
            time = datetime.now(timezone.utc)
        
        star_positions = {}
        
        for star_id, star_data in stars.items():
            ra = star_data['ra']
            dec = star_data['dec']
            
            altitude, azimuth = self.celestial_to_horizontal(ra, dec, time)
            
            star_positions[star_id] = {
                'ra': ra,
                'dec': dec,
                'altitude': altitude,
                'azimuth': azimuth,
                'magnitude': star_data.get('magnitude', 5.0),
                'visible': altitude > 0
            }
        
        return star_positions
    
    def get_cardinal_directions(self, time=None):
        """
        Get cardinal direction coordinates
        
        Args:
            time: datetime object (default: now)
            
        Returns:
            dict: Cardinal directions with their azimuth angles
        """
        return {
            'North': 0,
            'East': 90,
            'South': 180,
            'West': 270
        }
    
    def project_to_stereographic(self, altitude, azimuth):
        """
        Project altitude/azimuth to stereographic coordinates for plotting
        
        Args:
            altitude: Altitude in degrees
            azimuth: Azimuth in degrees
            
        Returns:
            tuple: (x, y) coordinates for plotting
        """
        # Convert to radians
        alt_rad = np.radians(altitude)
        az_rad = np.radians(azimuth)
        
        # Stereographic projection
        # Distance from center is related to zenith distance
        zenith_distance = np.pi/2 - alt_rad
        r = np.tan(zenith_distance / 2)
        
        # Convert to cartesian coordinates
        # Note: azimuth is measured from North, going East
        # We need to adjust for plotting (0° at top, increasing clockwise)
        x = r * np.sin(az_rad)
        y = r * np.cos(az_rad)
        
        return x, y
    
    def get_horizon_circle(self, num_points=360):
        """
        Generate points for horizon circle
        
        Args:
            num_points: Number of points to generate
            
        Returns:
            tuple: (x_coords, y_coords) for horizon circle
        """
        azimuths = np.linspace(0, 360, num_points)
        x_coords = []
        y_coords = []
        
        for az in azimuths:
            x, y = self.project_to_stereographic(0, az)  # 0° altitude = horizon
            x_coords.append(x)
            y_coords.append(y)
        
        return x_coords, y_coords

