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
        data_dir : Path
            Path to both SWOT and SWORD of Science NetCDFs
        reach_list : List
            List of all reaches
        valid_list : List
            List of reaches with valid data
        invalid_list : List
            List of reaches with invalid data
    """

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.reach_list = create_reach_list(data_dir)
        self.valid_list = []
        self.invalid_list = []

    def append(self):
        """Extract priors from SWOT and SoS, extract priors via geoBAM, and 
        append them back to the SoS."""
        
        for reach in self.reach_list:
            
            # Get required geoBAM input data from each file
            #print(f"\nRetrieving input data for reach: {reach}")
            swot_path = self.data_dir / (reach + "_SWOT.nc")
            sword_path = self.data_dir / (reach + "_SWORD.nc")
            input = Input(swot_path, sword_path)
            input.format_data()

            # Extract priors from geoBAM R functions for valid data only
            geobam_priors = None
            if input.data:
                #print("\tValid data: Retrieving priors.")
                self.valid_list.append(reach)
                geobam = GeoBAM(input.data)
                geobam_data = geobam.bam_data()
                geobam_priors = geobam.bam_priors(geobam_data)
            else:
                #print("\tInvalid data: Priors set to fill value.")
                self.invalid_list.append(reach)
            
            # Append data to the SWORD of Scence NetCDF file
            #print("\tWriting output to NetCDF.")
            output = Output(sword_path, geobam_priors)
            output.append_priors_node()

def create_reach_list(data_dir):
    """ Create a list of unique reaches."""

    with scandir(data_dir) as entries:
        reach_list = [ entry.name.split('_')[0] + '_' + entry.name.split('_')[1] for entry in entries ]
    return list(set(reach_list))