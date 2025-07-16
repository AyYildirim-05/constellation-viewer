import numpy as np
import requests
from astropy.coordinates import SkyCoord
from astropy import units as u
from skyfield.api import Star, load
from skyfield.data import hipparcos
import json
import os

class StarCatalog:
    def __init__(self):
        self.stars = {}
        self.constellations = {}
        self.load_data()
    
    def load_data(self):
        """Load star catalog and constellation data"""
        try:
            # Load Hipparcos catalog
            self.load_hipparcos_catalog()
            # Load constellation data
            self.load_constellation_data()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.create_sample_data()
    
    def load_hipparcos_catalog(self):
        """Load stars from Hipparcos catalog"""
        try:
            ts = load.timescale()
            with load.open(hipparcos.URL) as f:
                df = hipparcos.load_dataframe(f)
            
            # Filter for bright stars (magnitude < 6.0)
            bright_stars = df[df['magnitude'] < 6.0]
            
            for index, star_data in bright_stars.iterrows():
                hip_id = star_data['hip']
                ra = star_data['ra_degrees']
                dec = star_data['dec_degrees']
                mag = star_data['magnitude']
                
                self.stars[hip_id] = {
                    'ra': ra,
                    'dec': dec,
                    'magnitude': mag,
                    'hip_id': hip_id
                }
                
        except Exception as e:
            print(f"Error loading Hipparcos catalog: {e}")
            self.create_sample_stars()
    
    def load_constellation_data(self):
        """Load constellation line data"""
        # Sample constellation data (you can expand this)
        self.constellations = {
            'Ursa Major': {
                'lines': [
                    [50801, 53910],  # Dubhe to Merak
                    [53910, 58001],  # Merak to Phecda
                    [58001, 59774],  # Phecda to Megrez
                    [59774, 62956],  # Megrez to Alioth
                    [62956, 65378],  # Alioth to Mizar
                    [65378, 67301],  # Mizar to Alkaid
                    [59774, 54061],  # Megrez to Dubhe (close the bowl)
                ]
            },
            'Orion': {
                'lines': [
                    [25336, 25930],  # Betelgeuse to Bellatrix
                    [27989, 28716],  # Rigel to Saiph
                    [25930, 26207],  # Bellatrix to Alnilam
                    [26207, 25336],  # Alnilam to Betelgeuse
                    [26207, 27989],  # Alnilam to Rigel
                ]
            },
            'Cassiopeia': {
                'lines': [
                    [3179, 6686],    # Caph to Schedar
                    [6686, 11415],   # Schedar to Gamma Cas
                    [11415, 14404],  # Gamma Cas to Ruchbah
                    [14404, 21609],  # Ruchbah to Segin
                ]
            }
        }
    
    def create_sample_stars(self):
        """Create sample star data if catalog loading fails"""
        sample_stars = {
            # Ursa Major stars
            50801: {'ra': 165.931, 'dec': 61.751, 'magnitude': 1.8},  # Dubhe
            53910: {'ra': 165.460, 'dec': 56.382, 'magnitude': 2.4},  # Merak
            58001: {'ra': 178.457, 'dec': 53.695, 'magnitude': 2.4},  # Phecda
            59774: {'ra': 183.856, 'dec': 57.032, 'magnitude': 3.3},  # Megrez
            62956: {'ra': 193.507, 'dec': 55.960, 'magnitude': 1.8},  # Alioth
            65378: {'ra': 200.981, 'dec': 54.925, 'magnitude': 2.3},  # Mizar
            67301: {'ra': 206.885, 'dec': 49.313, 'magnitude': 1.9},  # Alkaid
            54061: {'ra': 166.079, 'dec': 61.751, 'magnitude': 1.8},  # Dubhe (duplicate for drawing)
            
            # Orion stars
            25336: {'ra': 88.793, 'dec': 7.407, 'magnitude': 0.4},    # Betelgeuse
            25930: {'ra': 81.283, 'dec': 6.350, 'magnitude': 1.6},    # Bellatrix
            26207: {'ra': 84.053, 'dec': -1.202, 'magnitude': 1.7},   # Alnilam
            27989: {'ra': 78.634, 'dec': -8.202, 'magnitude': 0.1},   # Rigel
            28716: {'ra': 86.939, 'dec': -9.670, 'magnitude': 2.1},   # Saiph
            
            # Cassiopeia stars
            3179: {'ra': 9.182, 'dec': 59.150, 'magnitude': 2.3},     # Caph
            6686: {'ra': 14.177, 'dec': 56.537, 'magnitude': 2.2},    # Schedar
            11415: {'ra': 14.177, 'dec': 60.717, 'magnitude': 2.5},   # Gamma Cas
            14404: {'ra': 23.396, 'dec': 57.815, 'magnitude': 2.7},   # Ruchbah
            21609: {'ra': 28.599, 'dec': 63.670, 'magnitude': 3.4},   # Segin
        }
        
        for hip_id, data in sample_stars.items():
            self.stars[hip_id] = {
                'ra': data['ra'],
                'dec': data['dec'],
                'magnitude': data['magnitude'],
                'hip_id': hip_id
            }
    
    def get_star(self, hip_id):
        """Get star data by Hipparcos ID"""
        return self.stars.get(hip_id, None)
    
    def get_constellation_lines(self, constellation_name):
        """Get line data for a constellation"""
        return self.constellations.get(constellation_name, {}).get('lines', [])
    
    def get_all_stars(self):
        """Get all star data"""
        return self.stars
    
    def get_all_constellations(self):
        """Get all constellation names"""
        return list(self.constellations.keys())

