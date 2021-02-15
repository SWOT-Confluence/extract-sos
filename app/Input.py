# Third party imports
import netCDF4 as nc
import numpy as np

class Input:
    """Class that represents SWOT and SWORD of Science data obtain from NetCDFs.

    Attributes
    ----------
        data: Dictionary
            Dictionary of formatted input data
        swot_path: Path
            Path to SWOT NetCDF
        sword_path: Path
            Path to SWORD of Science NetCDF
    """

    def __init__(self, swot_path, sword_path):
        self.data = {}
        self.swot_path = swot_path
        self.sword_path = sword_path

    def format_data(self):
        """Format SWOT and SWORD OS data to match input requirments of geoBAM.
        
        Builds a dictionary of formatted input data in data attribute. Replaces
        missing values in numpy.masked_array with NaN values.
        """

        # Node-level width, d_x_area; Reach-level slope (geoBAM requires matrices)
        swot_dataset = nc.Dataset(self.swot_path)
        width = swot_dataset["node/width"][:].filled(np.nan)
        d_x_area = swot_dataset["node/d_x_area"][:].filled(np.nan)
        slope = swot_dataset["node/slope2"][:].filled(np.nan)

        # Reach-level Qhat value (geoBAM requires a vector)
        sword_dataset = nc.Dataset(self.sword_path)
        qhat = sword_dataset["reach/Qhat"][:].filled(np.nan)
        qhat = np.repeat(qhat, width.shape[0])

        # Close datasets
        swot_dataset.close()
        sword_dataset.close()

        self.data = check_observations(width, d_x_area, slope, qhat)

def check_observations(width, d_x_area, slope2, qhat):
    """Checks for valid observation data (parameter values).

    Valid data includes:
        - Non-negative values for Qhat, width, and slope
        - Each time step has at least 5 valid floating point values
    
    Returns empty dictionary if invalid data detected.
    """

    # Test validity of data
    qhat[qhat < 0] = np.NAN 
    slope2[slope2 < 0] = np.NaN
    width[width < 0] = np.NaN
    if np.isnan(qhat[0]) or is_invalid(slope2) or is_invalid(width) or is_invalid(d_x_area):
        return {}
    
    # Data is valid
    else:
        return {
            "slope2" : slope2,
            "width" : width,
            "d_x_area" : d_x_area,
            "Qhat" : qhat
        }

def is_invalid(obs):
    """Checks if there are atleast 5 valid nx values for each nt.

    Returns boolean based on validity of obs parameter.
    """

    # Gather a count of valid values per nx
    valid_nodes = np.apply_along_axis(lambda obs: np.count_nonzero(~np.isnan(obs)),
        axis = 1, arr = obs)
    
    # Evaluate whether there are enough valid values per nt
    valid_days = valid_nodes[valid_nodes > (obs.shape[1] - 5)]
    if valid_days.size > 5:
        return False
    else:
        return True