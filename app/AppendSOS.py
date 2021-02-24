# Standard imports
from os import scandir

# Local imports
from app.GeoBAM import GeoBAM
from app.Input import Input
from app.Output import Output

class AppendSOS:
    """Class that represents data and operations needed to append prior data to
    the SWORD of Science.

    Attributes
    ----------
        logger: Logger
            logger object to log messages to
        reach_list : List
            List of all reaches
        valid_list : List
            List of reaches with valid data
        invalid_list : List
            List of reaches with invalid data
    """

    def __init__(self, data_dir, logger, reach_list):
        self.data_dir = data_dir
        self.logger = logger
        self.reach_list = reach_list
        self.valid_list = []
        self.invalid_list = []

    def append(self):
        """Extract priors from SWOT and SoS, extract priors via geoBAM, and 
        append them back to the SoS."""
        
        for reach in self.reach_list:
            # Get required geoBAM input data from each file
            self.logger.info(f"Retrieving input data for reach: {reach}")
            swot_path = self.data_dir / (reach + "_SWOT.nc")
            sos_path = self.data_dir / (reach + "_SOS.nc")
            input = Input(swot_path, sos_path)
            input.format_data()

            # Extract priors from geoBAM R functions for valid data only
            geobam_priors = None
            if input.data:
                self.valid_list.append(reach)
                geobam = GeoBAM(input.data)
                geobam_data = geobam.bam_data()
                geobam_priors = geobam.bam_priors(geobam_data)
            else:
                self.invalid_list.append(reach)
            
            # Append data to the SWORD of Scence NetCDF file
            output = Output(sos_path, geobam_priors)
            output.append_priors_node()