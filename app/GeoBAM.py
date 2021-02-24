# Third party imports
import rpy2.robjects as robjects
from rpy2.robjects import numpy2ri
from rpy2.robjects.packages import importr

# Print R warnings
robjects.r['options'](warn=1)

class GeoBAM:
    """Class that represents a run of geoBAM to extract priors.

    Serves as an API to geoBAM functions which are written in R.
    
    Attributes
    ----------
        input_data: dictionary
            dictionary of formatted input data
    """

    GEOBAM = importr("geoBAMr")

    def __init__(self, input_data):
        self.input_data = input_data
        self.geobam_data = None
        self.priors = None

    def bam_data(self):
        """Runs geoBAMr::bam_data function using swot_data attribute.
        
        Returns bam_data object.
        """

        # Activate automatic conversion of numpy objects to rpy2 objects
        numpy2ri.activate()

        # Format input data for geoBAM::bam_data function
        nrows_node = self.input_data["width"].shape[0]
        nrows_reach = self.input_data["slope2"].shape[0]
        width_matrix = robjects.r['matrix'](self.input_data["width"], nrow = nrows_node)
        slope_matrix = robjects.r['matrix'](self.input_data["slope2"], nrow = nrows_reach)
        d_x_a_matrix = robjects.r['matrix'](self.input_data["d_x_area"], nrow = nrows_node)
        qhat_vector = robjects.FloatVector(self.input_data["Qhat"])
        
        # Run bam_data
        data = self.GEOBAM.bam_data(w = width_matrix, 
            s = slope_matrix, dA = d_x_a_matrix, 
            Qhat = qhat_vector, variant = 'manning_amhg',
            max_xs = nrows_node)

        # Deactivate automatic conversion
        numpy2ri.deactivate()

        return data

    def bam_priors(self, geobam_data):
        """Runs geoBAMr::bam_priors function using geobam_data parameter.
        
        Returns priors object.
        """

        return self.GEOBAM.bam_priors(bamdata = geobam_data)