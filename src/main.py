import os 
from api_util import fetch_config, fetch_historical_rates, write_to_csv
from logger import setup_logger


#Initialize Logger
logger  = setup_logger(__name__)


def main(): 

    logger.info("Starting the application")
    
    # Fetch your parameters
    logger.info("Fetching conifguration from the config file")
    config = fetch_config("../configs/api_config.json")

    if config is None: 
        logger.error("Failed to load the configuration. Exiting the application...")
        return
    
    base = config.get("base")
    date = config.get("date")
    base_url= config.get("base_url")  

    if not all([base,date,base_url]):
        logger.error("Missing Configuration. Please ensure you have update the configuration file with all details")

    # Call your function with the test parameters
    logger.info(f"Fetching the Historical rates for {base} on {date}")
    historical_rates = fetch_historical_rates(base, date, base_url)

    if historical_rates: 
        csv_content = write_to_csv(historical_rates, base)
        print(csv_content)
        logger.info("Historical rates fetched succesfully")
    else: 
        logger.error("Failed to fetch Historical rates found")

    # Print the results to the console

if __name__ == "__main__":
    main()