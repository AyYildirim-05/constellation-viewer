import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, timezone
from star_catalog import StarCatalog
from sky_calculator import SkyCalculator

class SkyRenderer:
    def __init__(self, width=12, height=12, dpi=100):
        """
        Initialize sky renderer
        
        Args:
            width: Figure width in inches
            height: Figure height in inches
            dpi: Dots per inch for resolution
        """
        self.width = width
        self.height = height
        self.dpi = dpi
        
        # Color scheme
        self.colors = {
            'background': '#000011',
            'horizon': '#444444',
            'stars': '#ffffff',
            'constellation_lines': '#888888',
            'cardinal_text': '#cccccc',
            'altitude_circles': '#333333'
        }
        
        # Star size mapping (based on magnitude)
        self.star_sizes = {
            'min_size': 1,
            'max_size': 8,
            'magnitude_range': 6  # Magnitude 0 to 6
        }
    
    def create_figure(self):
        """
        Create and setup the matplotlib figure
        
        Returns:
            tuple: (fig, ax) matplotlib objects
        """
        fig, ax = plt.subplots(
            figsize=(self.width, self.height),
            dpi=self.dpi,
            facecolor=self.colors['background']
        )
        
        # Set up the plot
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.set_facecolor(self.colors['background'])
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        return fig, ax
    
    def draw_horizon_and_grid(self, ax, sky_calc):
        """
        Draw horizon circle and altitude grid
        
        Args:
            ax: matplotlib axes object
            sky_calc: SkyCalculator instance
        """
        # Draw horizon circle
        horizon_circle = patches.Circle(
            (0, 0), 1, 
            fill=False, 
            edgecolor=self.colors['horizon'],
            linewidth=2
        )
        ax.add_patch(horizon_circle)
        
        # Draw altitude circles (30°, 60°)
        for alt in [30, 60]:
            # Calculate radius for this altitude
            alt_rad = np.radians(alt)
            zenith_distance = np.pi/2 - alt_rad
            r = np.tan(zenith_distance / 2)
            
            if r < 2:  # Only draw if within plot limits
                alt_circle = patches.Circle(
                    (0, 0), r,
                    fill=False,
                    edgecolor=self.colors['altitude_circles'],
                    linewidth=1,
                    linestyle='--',
                    alpha=0.5
                )
                ax.add_patch(alt_circle)
        
        # Draw cardinal directions
        cardinal_dirs = sky_calc.get_cardinal_directions()
        for direction, azimuth in cardinal_dirs.items():
            x, y = sky_calc.project_to_stereographic(0, azimuth)
            # Adjust position slightly outside horizon
            x *= 1.1
            y *= 1.1
            
            ax.text(
                x, y, direction,
                ha='center', va='center',
                color=self.colors['cardinal_text'],
                fontsize=12,
                fontweight='bold'
            )
    
    def calculate_star_size(self, magnitude):
        """
        Calculate star size based on magnitude
        
        Args:
            magnitude: Star magnitude
            
        Returns:
            float: Star size for plotting
        """
        # Brighter stars (lower magnitude) should be larger
        # Clamp magnitude to reasonable range
        mag = max(0, min(magnitude, self.star_sizes['magnitude_range']))
        
        # Linear mapping from magnitude to size (inverted)
        size_range = self.star_sizes['max_size'] - self.star_sizes['min_size']
        size = self.star_sizes['max_size'] - (mag / self.star_sizes['magnitude_range']) * size_range
        
        return size
    
    def draw_stars(self, ax, star_positions):
        """
        Draw stars on the sky plot
        
        Args:
            ax: matplotlib axes object
            star_positions: Dictionary of star positions from SkyCalculator
        """
        for star_id, star_data in star_positions.items():
            if not star_data['visible']:
                continue
                
            # Get plot coordinates
            x, y = self.project_star_position(
                star_data['altitude'], 
                star_data['azimuth']
            )
            
            # Skip if outside plot area
            if x*x + y*y > 4:  # 2*2 = 4 (plot limit)
                continue
            
            # Calculate star size
            size = self.calculate_star_size(star_data['magnitude'])
            
            # Draw star
            ax.scatter(
                x, y,
                s=size**2,  # matplotlib uses area, so square the size
                c=self.colors['stars'],
                marker='*',
                alpha=0.9,
                edgecolors='none'
            )
    
    def draw_constellation_lines(self, ax, star_positions, catalog):
        """
        Draw constellation lines
        
        Args:
            ax: matplotlib axes object
            star_positions: Dictionary of star positions from SkyCalculator
            catalog: StarCatalog instance
        """
        for constellation_name in catalog.get_all_constellations():
            lines = catalog.get_constellation_lines(constellation_name)
            
            for line in lines:
                star1_id, star2_id = line
                
                # Check if both stars exist and are visible
                if (star1_id in star_positions and star2_id in star_positions and
                    star_positions[star1_id]['visible'] and star_positions[star2_id]['visible']):
                    
                    # Get coordinates for both stars
                    x1, y1 = self.project_star_position(
                        star_positions[star1_id]['altitude'],
                        star_positions[star1_id]['azimuth']
                    )
                    x2, y2 = self.project_star_position(
                        star_positions[star2_id]['altitude'],
                        star_positions[star2_id]['azimuth']
                    )
                    
                    # Draw line
                    ax.plot(
                        [x1, x2], [y1, y2],
                        color=self.colors['constellation_lines'],
                        linewidth=1,
                        alpha=0.7
                    )
    
    def project_star_position(self, altitude, azimuth):
        """
        Project star position using stereographic projection
        
        Args:
            altitude: Altitude in degrees
            azimuth: Azimuth in degrees
            
        Returns:
            tuple: (x, y) coordinates
        """
        # Convert to radians
        alt_rad = np.radians(altitude)
        az_rad = np.radians(azimuth)
        
        # Stereographic projection
        zenith_distance = np.pi/2 - alt_rad
        r = np.tan(zenith_distance / 2)
        
        # Convert to cartesian coordinates
        x = r * np.sin(az_rad)
        y = r * np.cos(az_rad)
        
        return x, y
    
    def add_title_and_info(self, ax, latitude, longitude, time, city_name=None):
        """
        Add title and location information to the plot
        
        Args:
            ax: matplotlib axes object
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            time: datetime object
            city_name: Optional city name
        """
        # Format time
        time_str = time.strftime('%Y-%m-%d %H:%M UTC')
        
        # Create title
        location_str = f"Lat: {latitude:.2f}°, Lon: {longitude:.2f}°"
        if city_name:
            location_str = f"{city_name} ({location_str})"
        
        title = f"Night Sky View\n{location_str}\n{time_str}"
        
        # Add title above the plot
        ax.text(
            0, 2.3, title,
            ha='center', va='top',
            color=self.colors['cardinal_text'],
            fontsize=14,
            fontweight='bold'
        )
        
        # Add zenith marker
        ax.scatter(
            0, 0, s=20, c=self.colors['cardinal_text'],
            marker='+', alpha=0.8
        )
        ax.text(
            0, -0.1, 'Zenith',
            ha='center', va='top',
            color=self.colors['cardinal_text'],
            fontsize=10
        )
    
    def render_sky(self, latitude, longitude, time=None, city_name=None, save_path=None):
        """
        Main method to render the complete sky view
        
        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            time: datetime object (default: now)
            city_name: Optional city name for title
            save_path: Optional path to save the image
            
        Returns:
            tuple: (fig, ax) matplotlib objects
        """
        if time is None:
            time = datetime.now(timezone.utc)
        
        # Initialize components
        catalog = StarCatalog()
        sky_calc = SkyCalculator(latitude, longitude)
        
        # Create figure
        fig, ax = self.create_figure()
        
        # Draw horizon and grid
        self.draw_horizon_and_grid(ax, sky_calc)
        
        # Calculate star positions
        stars = catalog.get_all_stars()
        star_positions = sky_calc.calculate_star_positions(stars, time)
        
        # Draw stars
        self.draw_stars(ax, star_positions)
        
        # Draw constellation lines
        self.draw_constellation_lines(ax, star_positions, catalog)
        
        # Add title and info
        self.add_title_and_info(ax, latitude, longitude, time, city_name)
        
        # Save if requested
        if save_path:
            plt.savefig(
                save_path,
                dpi=self.dpi,
                bbox_inches='tight',
                facecolor=self.colors['background']
            )
        
        return fig, ax

