import requests 
from logger import setup_logger
import os 
from dotenv import load_dotenv
import json
import csv
from typing import Optional, Dict, Any
import io
from datetime import datetime


load_dotenv()

current_time = datetime.now()
formatted_time = current_time.strftime("%y%m%d%H%M%S")


#Initialize logger
logger  = setup_logger(__name__)

##Function to fetch Historical fx rates from the API. 
def fetch_historical_rates(base, date, base_url):
    """
    Fetch historical FX rates for a given base currency and date.
    :param base: the three-letter currency code of your preferred base currency.
    :param date: the date for which you want to fetch historical rates.
    """

    api_key = os.getenv("api_key")

    if not api_key: 
        logger.error("API Key Not Found")
        return None
    
    url = f"{base_url}{date}?base={base}&access_key={api_key}"

    try: 
        response = requests.get(url)
        print(response)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        response.raise_for_status()

        data = response.json()
        print(f"Data received: {data}")  # Print the data to the console.
        logger.info(f"Historical rates fetched successfully for {base} on {date}")
        return data 
    
    except requests.exceptions.HTTPError as http_err: 
        logger.error(f"HTTP error occurred: {http_err}", exc_info=True)
        return None
    
    except Exception as e: 
        logger.error(f"An error occurred: {e}", exc_info=True)
        return None

## Fetch parameters from the configuration file. 
def fetch_config(config_path):
    with open(config_path, 'r') as file: 
        config = json.load(file)
    return config

#Write the rates to csv file
def write_to_csv(data: Dict[str, Any], base: str) -> Optional[str]:

    if not data or 'rates' not in data: 
        logger.error("Invalid Data: Rates are missing")
        return None
    
    with io.StringIO() as output: 
        fieldnames = ['date','base','target_currency', 'rate']

        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()

        rates = data.get('rates', {})
        date = data.get('date', 'Unknown Date')

        for target_currency, rate in rates.items():
            writer.writerow({
                'date': date,
                'base': base,
                'target_currency': target_currency,
                'rate': rate
            })
        
        file = None
        
        try: 
            with(open(f'../data/historical_rates_{base}_{date}_{formatted_time}.csv', 'w', newline='')) as file:
                file.write(output.getvalue())
                logger.info(f'File extracted with historical rates of {date} and {base}')
        
        except Exception as e: 
            logger.error(f"An error occurred: {e}", exc_info=True)
            return False
        finally: 
            output.close()