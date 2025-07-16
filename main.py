#!/usr/bin/env python3
"""
Constellation Viewer - Generate night sky images based on location and time

Usage:
    python main.py --lat 40.7128 --lon -74.0060 --city "New York"
    python main.py --lat 51.5074 --lon -0.1278 --time "2024-07-15 22:00:00"
"""

import argparse
import sys
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from sky_renderer import SkyRenderer
from location_detector import LocationDetector

def parse_time(time_str):
    """
    Parse time string into datetime object
    
    Args:
        time_str: Time string in format "YYYY-MM-DD HH:MM:SS"
        
    Returns:
        datetime: Parsed datetime object in UTC
    """
    try:
        # Parse the time string
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        # Assume UTC timezone
        dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        print(f"Error: Invalid time format. Use 'YYYY-MM-DD HH:MM:SS'")
        sys.exit(1)

def get_sample_locations():
    """
    Get a dictionary of sample locations for testing
    
    Returns:
        dict: Sample locations with coordinates
    """
    return {
        'new_york': {'lat': 40.7128, 'lon': -74.0060, 'name': 'New York City'},
        'london': {'lat': 51.5074, 'lon': -0.1278, 'name': 'London'},
        'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'name': 'Tokyo'},
        'sydney': {'lat': -33.8688, 'lon': 151.2093, 'name': 'Sydney'},
        'paris': {'lat': 48.8566, 'lon': 2.3522, 'name': 'Paris'},
        'cairo': {'lat': 30.0444, 'lon': 31.2357, 'name': 'Cairo'},
        'reykjavik': {'lat': 64.1466, 'lon': -21.9426, 'name': 'Reykjavik'},
        'anchorage': {'lat': 61.2181, 'lon': -149.9003, 'name': 'Anchorage'},
    }

def main():
    parser = argparse.ArgumentParser(
        description='Generate constellation images based on location and time',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --lat 40.7128 --lon -74.0060 --city "New York"
  %(prog)s --lat 51.5074 --lon -0.1278 --time "2024-07-15 22:00:00"
  %(prog)s --location new_york
  %(prog)s --location tokyo --time "2024-12-25 00:00:00"
        """
    )
    
    # Location options
    location_group = parser.add_mutually_exclusive_group(required=False)
    location_group.add_argument(
        '--location', 
        choices=get_sample_locations().keys(),
        help='Use a predefined location'
    )
    location_group.add_argument(
        '--lat', 
        type=float,
        help='Latitude in degrees (use with --lon)'
    )
    
    parser.add_argument(
        '--lon', 
        type=float,
        help='Longitude in degrees (required with --lat)'
    )
    
    parser.add_argument(
        '--city', 
        type=str,
        help='City name for display (optional)'
    )
    
    parser.add_argument(
        '--time', 
        type=str,
        help='Time in UTC format: "YYYY-MM-DD HH:MM:SS" (default: now)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: display on screen)'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=12,
        help='Figure width in inches (default: 12)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=12,
        help='Figure height in inches (default: 12)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=100,
        help='Resolution in DPI (default: 100)'
    )
    
    parser.add_argument(
        '--list-locations',
        action='store_true',
        help='List available predefined locations'
    )
    
    parser.add_argument(
        '--auto-location',
        action='store_true',
        help='Automatically detect current location'
    )
    
    args = parser.parse_args()
    
    # Handle list locations
    if args.list_locations:
        print("Available locations:")
        for key, loc in get_sample_locations().items():
            print(f"  {key}: {loc['name']} ({loc['lat']:.4f}, {loc['lon']:.4f})")
        return
    
    # Determine location
    if args.auto_location:
        # Auto-detect current location
        detector = LocationDetector()
        if detector.detect_location():
            detector.print_location_info()
            info = detector.get_location_info()
            latitude = info['latitude']
            longitude = info['longitude']
            city_name = info['city'] or 'Auto-detected Location'
        else:
            print("Error: Could not detect location automatically")
            sys.exit(1)
    
    elif args.location:
        # Use predefined location
        locations = get_sample_locations()
        location_data = locations[args.location]
        latitude = location_data['lat']
        longitude = location_data['lon']
        city_name = location_data['name']
    
    elif args.lat is not None:
        # Use custom coordinates
        if args.lon is None:
            print("Error: --lon is required when using --lat")
            sys.exit(1)
        latitude = args.lat
        longitude = args.lon
        city_name = args.city or 'Custom Location'
    
    else:
        # No location specified, default to auto-detection
        print("No location specified. Attempting to auto-detect...")
        detector = LocationDetector()
        if detector.detect_location():
            detector.print_location_info()
            info = detector.get_location_info()
            latitude = info['latitude']
            longitude = info['longitude']
            city_name = info['city'] or 'Auto-detected Location'
        else:
            print("Error: Could not detect location automatically")
            print("Please specify a location using --location, --lat/--lon, or --auto-location")
            sys.exit(1)
    
    # Parse time
    if args.time:
        time = parse_time(args.time)
    else:
        time = datetime.now(timezone.utc)
    
    # Create renderer
    renderer = SkyRenderer(width=args.width, height=args.height, dpi=args.dpi)
    
    print(f"Generating sky view for:")
    print(f"  Location: {city_name or 'Custom location'}")
    print(f"  Coordinates: {latitude:.4f}°, {longitude:.4f}°")
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("")
    
    try:
        # Render the sky
        fig, ax = renderer.render_sky(
            latitude=latitude,
            longitude=longitude,
            time=time,
            city_name=city_name,
            save_path=args.output
        )
        
        if args.output:
            print(f"Sky view saved to: {args.output}")
        else:
            print("Displaying sky view... (close window to exit)")
            plt.show()
            
    except Exception as e:
        print(f"Error generating sky view: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

