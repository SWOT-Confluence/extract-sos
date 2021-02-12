# Standard imports
import logging
from pathlib import Path
from time import time

# Local Imports
from app.AppendSOS import AppendSOS

def create_logger():
    """Create a Logger object and set log level."""

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a handler to file and set level
    filename = f"append_sos.log"
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handler
    file_format = logging.Formatter("%(message)s")
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    logger.addHandler(file_handler)

    return logger

def main():
    """Main method run append method."""

    start = time()
    logger = create_logger()
    data_dir = Path("fill")
    append = AppendSOS(data_dir)
    append.append()
    end = time()
    logger.info("valid reaches:")
    logger.info(', '.join(append.valid_list))
    logger.info("total valid: " + str(len(append.valid_list)))
    logger.info("invalid reaches:")
    logger.info(', '.join(append.invalid_list))
    logger.info("total invalid: " + str(len(append.invalid_list)))
    logger.info(f"Run time: {end - start}")

if __name__ == "__main__":
    main()