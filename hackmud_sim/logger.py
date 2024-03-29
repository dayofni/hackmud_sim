
import logging

STND_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def setup_logger(name: str = __name__, level: int = logging.DEBUG, format: str = STND_FORMAT):
    
    # Get the logger.
    logger = logging.getLogger(name)
    logger.setLevel(level)  # adjust level as needed
    
    if not logger.handlers:
        
        # Set format.
        formatter = logging.Formatter(format)

        # Create a file handler and set the formatter
        file_handler = logging.FileHandler('hackmud_sim.log')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger