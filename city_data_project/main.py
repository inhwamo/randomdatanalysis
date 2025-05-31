#!/usr/bin/env python3
"""
Main script to gather city data with sunrise/sunset times and population
"""
import argparse
import logging
from datetime import date
from src.city_processor import CityDataProcessor

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('city_data.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Gather city data with sunrise/sunset times')
    parser.add_argument('--sample-size', type=int, default=10, 
                       help='Number of cities to process (default: 10)')
    parser.add_argument('--no-api', action='store_true', 
                       help='Use local calculation instead of API')
    parser.add_argument('--output', type=str, default='cities_with_sunrise_sunset.csv',
                       help='Output CSV filename')
    parser.add_argument('--date', type=str, 
                       help='Target date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--summer-solstice', action='store_true',
                       help='Analyze summer solstice 2024 (June 20) and rank by daylight')
    parser.add_argument('--min-population', type=int, default=200000,
                       help='Minimum city population (default: 200,000)')
    parser.add_argument('--top-cities', type=int, default=20,
                       help='Number of top cities to return (default: 20)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse target date
    target_date = date.today()
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            logger.error(f"Invalid date format: {args.date}. Use YYYY-MM-DD")
            return
    
    logger.info("Starting city data processing...")
    
    # Initialize processor
    processor = CityDataProcessor()
    
    try:
        if args.summer_solstice:
            # Special summer solstice analysis
            logger.info("=== SUMMER SOLSTICE 2024 ANALYSIS ===")
            logger.info(f"Minimum population: {args.min_population:,}")
            logger.info(f"Top cities to return: {args.top_cities}")
            logger.info(f"Use API: {not args.no_api}")
            
            cities_df = processor.process_summer_solstice_analysis(
                min_population=args.min_population,
                top_cities=args.top_cities,
                use_api=not args.no_api
            )
            
            output_filename = f"summer_solstice_2024_top_{args.top_cities}_cities.csv"
            
        else:
            # Regular processing
            logger.info(f"Sample size: {args.sample_size}")
            logger.info(f"Use API: {not args.no_api}")
            logger.info(f"Target date: {target_date}")
            logger.info(f"Output file: {args.output}")
            
            # Process cities
            cities_df = processor.process_sample_cities(
                sample_size=args.sample_size,
                use_api=not args.no_api
            )
            
            output_filename = args.output
        
        if len(cities_df) > 0:
            # Save results
            output_path = processor.save_to_csv(cities_df, output_filename)
            
            if output_path:
                logger.info(f"Successfully processed {len(cities_df)} cities")
                logger.info(f"Results saved to: {output_path}")
                
                # Display sample results
                print("\n" + "="*100)
                print("RESULTS SUMMARY")
                print("="*100)
                
                if args.summer_solstice:
                    display_cols = ['name', 'country', 'population', 'latitude', 
                                   'daylight_hours', 'sunrise', 'sunset', 'day_length']
                    print(f"Top {len(cities_df)} cities with most daylight on Summer Solstice 2024 (June 20):")
                else:
                    display_cols = ['name', 'country', 'population', 'latitude', 'longitude', 
                                   'sunrise', 'sunset', 'day_length']
                
                available_cols = [col for col in display_cols if col in cities_df.columns]
                
                # Format for better display
                display_df = cities_df[available_cols].copy()
                if 'population' in display_df.columns:
                    display_df['population'] = display_df['population'].apply(lambda x: f"{x:,}")
                if 'daylight_hours' in display_df.columns:
                    display_df['daylight_hours'] = display_df['daylight_hours'].apply(lambda x: f"{x:.2f}h")
                
                print(display_df.to_string(index=True, max_rows=25))
                
                if args.summer_solstice:
                    print(f"\n💡 The city with the most daylight was: {cities_df.iloc[0]['name']}, {cities_df.iloc[0]['country']}")
                    print(f"   Daylight hours: {cities_df.iloc[0]['daylight_hours']:.2f} hours")
                    print(f"   Population: {cities_df.iloc[0]['population']:,}")
                
            else:
                logger.error("Failed to save results")
        else:
            logger.error("No city data processed")
            
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()