
import logging

import logging.handlers
import queue

def setup_logger(level: int = logging.DEBUG):
    
    # Get the logger.
    logger = logging.getLogger(__name__)
    logger.setLevel(level)  # adjust level as needed
    
    # Create async queue.
    log_queue     = queue.Queue()
    queue_handler = logging.handlers.QueueHandler(log_queue)
    
    # Set format.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    queue_handler.setFormatter(formatter)

    # Create a file handler and set the formatter
    file_handler = logging.FileHandler('hackmud_sim.log')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    
    listener = logging.handlers.QueueListener(log_queue, logging.StreamHandler())
    listener.start()

    return logger