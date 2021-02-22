# Standard imports
import logging
from os import scandir
from pathlib import Path
import sys
from time import time

# Third party imports
from mpi4py import MPI

# Local Imports
from app.AppendSOS import AppendSOS

"""Runs append sos program using data directory argument."""

COMM = MPI.COMM_WORLD

def run(data_dir):
    """Main method run append method."""

    start = time()
    rank = COMM.Get_rank()
    rank_logger = create_rank_logger(rank)

    # Create a dictionary of ranks assigned to reaches
    reach_dict = {}
    if rank == 0:
        reach_dict = get_reach_dict(data_dir)
        log_reaches(rank_logger, reach_dict)

    # Run append for each rank broadcasting reach list to each rank
    reach_dict = COMM.bcast(reach_dict, root=0)
    append = AppendSOS(Path(data_dir), rank_logger, reach_dict[rank])
    append.append()
    COMM.barrier()
    end = time()

    # Log results
    log_results(rank_logger, append, end - start)

def get_reach_dict(data_dir):
    """Creates a dictionary of rank keys and reach values."""

    size = COMM.Get_size()

    with scandir(data_dir) as entries:
        reach_list = [ entry.name.split('_')[0] + '_' + entry.name.split('_')[1] for entry in entries ]

    # Divide list up evenly amongst ranks and handle any overflow
    reach_list = list(set(reach_list))
    total_reaches = len(reach_list)
    reach_per_rank = total_reaches // size

    # Create a dictionary for rank keys and reach values
    reach_dict = {}
    reach_count = 0
    for i in range(size):
        start = reach_count
        end = reach_count + reach_per_rank
        reach_dict[i] = reach_list[start:end]
        reach_count += reach_per_rank

    # Spread remaining reaches over ranks
    if total_reaches % size != 0:
        remaining = total_reaches - reach_count
        i = 0
        for j in range(remaining):
            reach_dict[i].append(reach_list[reach_count])
            reach_count += 1
            i = 0 if i == (size - 1) else i + 1
    
    return reach_dict

def create_rank_logger(rank):
    """Creates a file logger for each rank to log to."""

    # Create a Logger object and set log level
    rank_logger = logging.getLogger(__name__)
    rank_logger.setLevel(logging.DEBUG)

    # Create a handler to file and set level
    filename = f"{rank}.log"
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handler
    file_format = logging.Formatter("%(message)s")
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    rank_logger.addHandler(file_handler)

    # Return logger
    return rank_logger

def log_reaches(logger, reach_dict):
    """Log the spread of reaches over ranks."""
    
    total_reaches = 0
    for key,value in reach_dict.items():
        reach_count = 0
        for element in value:
            reach_count += 1
        total_reaches += reach_count
        logger.info(f"key   Reach count:    {reach_count}")
    logger.info(f"Total reach count: {total_reaches}")

def log_results(logger, append, time):
    """Log results of append SoS run."""

    logger.info("valid reaches:")
    logger.info(', '.join(append.valid_list))
    logger.info("total valid: " + str(len(append.valid_list)))
    logger.info("invalid reaches:")
    logger.info(', '.join(append.invalid_list))
    logger.info("total invalid: " + str(len(append.invalid_list)))
    logger.info(f"Run time: {time}")

if __name__ == "__main__":
    try:
        path = sys.argv[1]
        run(path)
    except IndexError:
        raise SystemExit("Please enter a valid path to a directory that" 
            + "\ncontains SWOT and SoS data.")