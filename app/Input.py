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
        sos_path: Path
            Path to SWORD of Science NetCDF
    """

    def __init__(self, swot_path, sos_path):
        self.data = {}
        self.swot_path = swot_path
        self.sos_path = sos_path

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
        sword_dataset = nc.Dataset(self.sos_path)
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
        - Each time step and node has at least 5 valid floating point values
    
    Returns empty dictionary if invalid data detected.
    """

    # Test validity of data
    qhat[qhat < 0] = np.NAN 
    slope2[slope2 < 0] = np.NaN
    width[width < 0] = np.NaN
 
    # Qhat
    if np.isnan(qhat[0]):
        return {}

    # slope2
    slope_dict = is_valid(slope2)
    if not slope_dict["valid"]:
        return {}

    # width
    width_dict = is_valid(width)
    if not width_dict["valid"]:
        return {}

    # d_x_area
    dA_dict = is_valid(d_x_area)
    if not dA_dict["valid"]:
        return {}

    # Remove invalid node (row) observations
    invalid_node_indexes = np.unique(np.concatenate((slope_dict["invalid_nodes"][0], 
        width_dict["invalid_nodes"][0], dA_dict["invalid_nodes"][0])))
    slope2 = np.delete(slope2, invalid_node_indexes, axis = 0)
    width = np.delete(width, invalid_node_indexes, axis = 0)
    d_x_area = np.delete(d_x_area, invalid_node_indexes, axis = 0)
    
    # Remove invalid time (column) indexes
    invalid_time_indexes = np.unique(np.concatenate((slope_dict["invalid_times"][0], 
        width_dict["invalid_times"][0], dA_dict["invalid_times"][0])))
    slope2 = np.delete(slope2, invalid_time_indexes, axis = 1)
    width = np.delete(width, invalid_time_indexes, axis = 1)
    d_x_area = np.delete(d_x_area, invalid_time_indexes, axis = 1)
    
    # Valid data is returned
    return {
            "slope2" : slope2,
            "width" : width,
            "d_x_area" : d_x_area,
            "Qhat" : qhat,
            "invalid_indexes" : invalid_node_indexes
        }

def is_valid(obs):
    """Checks if there are atleast 5 valid nx values for each nt.

    Returns dictionary of whether the observations are valid, and if they are 
    valid includes invalid node and time step indexes.
    """

    # Gather a count of valid values per nx (across nt) returns nt vector
    time = np.apply_along_axis(lambda obs: np.count_nonzero(~np.isnan(obs)),
        axis = 0, arr = obs)

    # Are there enough valid nx per nt
    valid_time = time[time >= 5]

    # Gather a count of valid values per nt (across nx) returns nx vector
    nodes = np.apply_along_axis(lambda obs: np.count_nonzero(~np.isnan(obs)),
        axis = 1, arr = obs)
    
    # Are there enough valid nt per nx
    valid_nodes = nodes[nodes >= 5]

    if valid_time.size >= 5 and valid_nodes.size >= 5:
        return {
            "valid" : True,
            "invalid_nodes" : np.nonzero(nodes < 5),
            "invalid_times" : np.nonzero(time < 5)
            }
    else:
        return {
            "valid" : False,
            "invalid_nodes" : None,
            "invalid_times" : None
            }