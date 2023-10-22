import os 
from api_util import fetch_config, fetch_historical_rates, write_file_to_blob
from logger import setup_logger
from datetime import datetime


#Initialize Logger
logger  = setup_logger(__name__)

def load_check_user_config(config_path): 
    config = fetch_config(config_path)

    if config is None: 
        logger.error("Failed to load the configuration. Exiting the application...")
        return None
    
    required_config = ["base", "date", "base_url", "containername", "blob_name"]
    missing_config = [cfg for cfg in required_config if not config.get(cfg)]

    if missing_config: 
        logger.error(f"Missing Configuration {missing_config}. Please ensure you have update the configuration file with all details")
        return None


    if not all(config in required_config for config in required_config):
        logger.error("Missing Configuration. Please ensure you have updated the configuration file with all details")
        return None
    
    return config


def main(): 
    logger.info("Starting the application")

    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'api_config.json')
    config = load_check_user_config(config_path)

    if config is None: 
        return


    current_time = datetime.now()
    formatted_time = current_time.strftime("%y%m%d%H%M%S")
    base = config.get("base")
    date = config.get("date")
    base_url= config.get("base_url")  
    container_name=config.get("containername")
    blob_name_template = config.get("blob_name", '')
    blob_name=blob_name_template.format(base=base, date=date, formatted_time=formatted_time)


    # Call your function with the test parameters
    logger.info(f"Fetching the Historical rates for {base} on {date}")
    historical_rates = fetch_historical_rates(base, date, base_url)

    if historical_rates: 
        success = write_file_to_blob(historical_rates, base, container_name, blob_name)
        if success:
            logger.info("Historical rates fetched succesfully")
    else: 
        logger.error("Failed to fetch Historical rates found")

    # Print the results to the console

if __name__ == "__main__":
    main()