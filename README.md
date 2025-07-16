# Constellation Viewer 🌟

A Python program that generates beautiful images of constellations in the night sky based on your geographical location and time. See exactly what stars and constellations are visible from anywhere on Earth at any time!

![Night Sky Example](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features ✨

- 🌍 **Location-based sky calculation** - Enter any latitude/longitude or use predefined cities
- 🕒 **Time-based rendering** - View the sky at any date and time (past, present, or future)
- ⭐ **Accurate star positions** - Uses Hipparcos catalog for precise star data
- 🔗 **Constellation lines** - Connect stars to show traditional constellation patterns
- 🧭 **Horizon and cardinal directions** - Clear orientation with N/S/E/W markers
- 📏 **Altitude circles** - 30° and 60° altitude reference circles
- 🎨 **Beautiful visualization** - Dark sky theme with appropriately sized stars
- 💾 **Save or display** - Export images or view interactively

## Installation 🚀

1. Clone this repository:
```bash
git clone https://github.com/yourusername/constellation-viewer.git
cd constellation-viewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 📖

### Basic Examples

```bash
# View current sky from New York
python main.py --location new_york

# Custom location with coordinates
python main.py --lat 40.7128 --lon -74.0060 --city "New York"

# Specific date and time
python main.py --location london --time "2024-12-25 00:00:00"

# Save to file
python main.py --location tokyo --output sky_view.png
```

### Available Predefined Locations

```bash
# List all available locations
python main.py --list-locations
```

Current locations include:
- new_york: New York City
- london: London
- tokyo: Tokyo
- sydney: Sydney
- paris: Paris
- cairo: Cairo
- reykjavik: Reykjavik
- anchorage: Anchorage

### Command Line Options

```
--location LOCATION     Use a predefined location
--lat LATITUDE         Latitude in degrees (use with --lon)
--lon LONGITUDE        Longitude in degrees (required with --lat)
--city CITY_NAME       City name for display (optional)
--time "YYYY-MM-DD HH:MM:SS"  Time in UTC (default: now)
--output PATH          Save image to file (default: display on screen)
--width WIDTH          Figure width in inches (default: 12)
--height HEIGHT        Figure height in inches (default: 12)
--dpi DPI              Resolution in DPI (default: 100)
--list-locations       List available predefined locations
```

## How It Works 🔬

The program uses several key astronomical concepts:

1. **Coordinate Systems**: Converts between celestial coordinates (Right Ascension/Declination) and horizontal coordinates (Altitude/Azimuth)

2. **Earth's Rotation**: Accounts for your location's rotation relative to the stars

3. **Stereographic Projection**: Projects the 3D sky onto a 2D circular plot

4. **Star Catalogs**: Uses the Hipparcos catalog for accurate star positions and magnitudes

5. **Constellation Data**: Connects stars using traditional constellation line patterns

## Project Structure 📁

```
constellation_viewer/
├── main.py              # Main application script
├── star_catalog.py      # Star and constellation data management
├── sky_calculator.py    # Astronomical calculations
├── sky_renderer.py      # Visualization and plotting
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Dependencies 📦

- **astropy** (≥5.0.0): Astronomical calculations and coordinate transformations
- **skyfield** (≥1.45): Precise celestial mechanics and star catalogs
- **matplotlib** (≥3.5.0): Plotting and visualization
- **numpy** (≥1.20.0): Numerical operations
- **requests** (≥2.25.0): HTTP requests for data downloads
- **cartopy** (≥0.21.0): Geographic projections

## Examples 🖼️

The program generates circular star maps showing:
- Stars sized by brightness (magnitude)
- Constellation lines connecting related stars
- Horizon circle and altitude references
- Cardinal directions (N, S, E, W)
- Location and time information

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Future Enhancements 🔮

- [ ] Add planet positions
- [ ] Include Moon phases
- [ ] Add more constellations
- [ ] Interactive web interface
- [ ] Real-time light pollution data
- [ ] Mobile app version
- [ ] Animation for time progression

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [Hipparcos Catalog](https://www.cosmos.esa.int/web/hipparcos) for star data
- [Astropy](https://www.astropy.org/) for astronomical calculations
- [Skyfield](https://rhodesmill.org/skyfield/) for precise celestial mechanics
- Traditional constellation patterns from various astronomical sources

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.

---

*"We are all made of star stuff."* - Carl Sagan

