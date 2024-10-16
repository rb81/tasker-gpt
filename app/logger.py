import logging

def setup_logger():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)

    # Create console handler and set level to INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger

# Create and configure the central logger
logger = setup_logger()