import requests 
from logger import setup_logger
import os 
from dotenv import load_dotenv
import json
import csv
from typing import Optional, Dict, Any
import io
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()

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
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.content}")
        response.raise_for_status()

        data = response.json()
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
def write_file_to_blob(data: Dict[str, Any], base: str, container_name) -> Optional[str]:

    current_time = datetime.now()
    formatted_time = current_time.strftime("%y%m%d%H%M%S")

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
        

        csv_content = output.getvalue()

        #This part works to upload the data to the blob storage. 

        account_url = os.getenv("account_url")
        sas_token = os.getenv("sas_token")

        blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)
        blob_name = f'historical_rates_{base}_{date}_{formatted_time}.csv'

        try:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            blob_client.upload_blob(csv_content, overwrite=True)
            logger.info(f'File {blob_name} uploaded with historical rates of {date} and {base} to ')
            return True
        except Exception as e: 
            logger.error(f"An error occurred: {e}", exc_info=True)
            return None