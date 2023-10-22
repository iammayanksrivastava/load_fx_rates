import logging
import sys 

def setup_logger(name): 

    """
    Creates a logger configured to output to stdout.

    Parameters:
    name (str): The name of the logger.

    Returns:
    logging.Logger: a configured instance of a logger.
    """
    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    if not custom_logger.handlers:
        custom_logger.addHandler(console_handler)

    return custom_logger


