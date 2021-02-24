# Third party imports
import numpy as np
import netCDF4 as nc

class Output:
    """Class that represents SWORD of Science data obtained from geoBAM run.

    Attributes
    ----------
        prior_data: rpy2.robjects.vectors.ListVector
            ListVector of prior data from geoBAMr::bam_priors function
        sos_path: Path
            Path to SWORD of Science NetCDF
    """

    FILL_VALUE = float(-9999)

    def __init__(self, sos_path, prior_data):
        self.sos_path = sos_path
        self.prior_data = prior_data

    def append_priors_node(self):
        """Append prior data to sos_path file."""

        # Create prior dictionary
        prior_dict = create_prior_dict()

        # Test if valid data could be extracted
        if self.prior_data:
            extract_priors(prior_dict, self.prior_data)
        
        # Write prior dictionary to SWORD of Science file
        write_priors(self.sos_path, prior_dict)

def create_prior_dict():
    return {
        "river_type" : Output.FILL_VALUE,
        "lowerbound_A0" : Output.FILL_VALUE,
        "upperbound_A0" : Output.FILL_VALUE,
        "lowerbound_logn" : Output.FILL_VALUE,
        "upperbound_logn" : Output.FILL_VALUE,
        "lowerbound_b" : Output.FILL_VALUE,
        "upperbound_b" : Output.FILL_VALUE,
        "lowerbound_logWb" : Output.FILL_VALUE,
        "upperbound_logWb" : Output.FILL_VALUE,
        "lowerbound_logDb" : Output.FILL_VALUE,
        "upperbound_logDb" : Output.FILL_VALUE,
        "lowerbound_logr" : Output.FILL_VALUE,
        "upperbound_logr" : Output.FILL_VALUE,
        "logA0_hat" : Output.FILL_VALUE,
        "logn_hat" : Output.FILL_VALUE,
        "b_hat" : Output.FILL_VALUE,
        "logWb_hat" : Output.FILL_VALUE,
        "logDb_hat" : Output.FILL_VALUE,
        "logr_hat" : Output.FILL_VALUE,
        "logA0_sd" : Output.FILL_VALUE,
        "logn_sd" : Output.FILL_VALUE,
        "b_sd" : Output.FILL_VALUE,
        "logWb_sd" : Output.FILL_VALUE,
        "logDb_sd" : Output.FILL_VALUE,
        "logr_sd" : Output.FILL_VALUE,
        "lowerbound_logQ" : Output.FILL_VALUE,
        "upperbound_logQ" : Output.FILL_VALUE,
        "lowerbound_logWc" : Output.FILL_VALUE,
        "upperbound_logWc" : Output.FILL_VALUE,
        "lowerbound_logQc" : Output.FILL_VALUE,
        "upperbound_logQc" : Output.FILL_VALUE,
        "logWc_hat" : Output.FILL_VALUE,
        "logQc_hat" : Output.FILL_VALUE,
        "logQ_sd" : Output.FILL_VALUE,
        "logWc_sd" : Output.FILL_VALUE,
        "logQc_sd" : Output.FILL_VALUE,
        "Werr_sd" : Output.FILL_VALUE,
        "Serr_sd" : Output.FILL_VALUE,
        "dAerr_sd" : Output.FILL_VALUE,
        "sigma_man" : Output.FILL_VALUE,
        "sigma_amhg" : Output.FILL_VALUE
    }
    
def extract_priors(prior_dict, priors):
    """Extracts and stores priors in the prior_dict parameter."""

    prior_dict["river_type"] = priors.rx2("River_Type")[0]
    river_priors = priors.rx2("river_type_priors")
    prior_dict["lowerbound_A0"] = np.array(river_priors.rx2("lowerbound_A0"))[0]
    prior_dict["upperbound_A0"] = np.array(river_priors.rx2("upperbound_A0"))[0]
    prior_dict["lowerbound_logn"] = np.array(river_priors.rx2("lowerbound_logn"))[0]
    prior_dict["upperbound_logn"] = np.array(river_priors.rx2("upperbound_logn"))[0]
    prior_dict["lowerbound_b"] = np.array(river_priors.rx2("lowerbound_b"))[0]
    prior_dict["upperbound_b"] = np.array(river_priors.rx2("upperbound_b"))[0]
    prior_dict["lowerbound_logWb"] = np.array(river_priors.rx2("lowerbound_logWb"))[0]
    prior_dict["upperbound_logWb"] = np.array(river_priors.rx2("upperbound_logWb"))[0]
    prior_dict["lowerbound_logDb"] = np.array(river_priors.rx2("lowerbound_logDb"))[0]
    prior_dict["upperbound_logDb"] = np.array(river_priors.rx2("upperbound_logDb"))[0]
    prior_dict["lowerbound_logr"] = np.array(river_priors.rx2("lowerbound_logr"))[0]
    prior_dict["upperbound_logr"] = np.array(river_priors.rx2("upperbound_logr"))[0]
    prior_dict["logA0_hat"] = np.array(river_priors.rx2("logA0_hat"))[0]
    prior_dict["logn_hat"] = np.array(river_priors.rx2("logn_hat"))[0]
    prior_dict["b_hat"] = np.array(river_priors.rx2("b_hat"))[0]
    prior_dict["logWb_hat"] = np.array(river_priors.rx2("logWb_hat"))[0]
    prior_dict["logDb_hat"] = np.array(river_priors.rx2("logDb_hat"))[0]
    prior_dict["logr_hat"] = np.array(river_priors.rx2("logr_hat"))[0]
    prior_dict["logA0_sd"] = np.array(river_priors.rx2("logA0_sd"))[0]
    prior_dict["logn_sd"] = np.array(river_priors.rx2("logn_sd"))[0]
    prior_dict["b_sd"] = np.array(river_priors.rx2("b_sd"))[0]
    prior_dict["logWb_sd"] = np.array(river_priors.rx2("logWb_sd"))[0]
    prior_dict["logDb_sd"] = np.array(river_priors.rx2("logDb_sd"))[0]
    prior_dict["logr_sd"] = np.array(river_priors.rx2("logr_sd"))[0]

    other_priors = priors.rx2("other_priors")
    prior_dict["lowerbound_logQ"] = np.array(other_priors.rx2("lowerbound_logQ"))[0]
    prior_dict["upperbound_logQ"] = np.array(other_priors.rx2("upperbound_logQ"))[0]
    prior_dict["lowerbound_logWc"] = np.array(other_priors.rx2("lowerbound_logWc"))[0]
    prior_dict["upperbound_logWc"] = np.array(other_priors.rx2("upperbound_logWc"))[0]
    prior_dict["lowerbound_logQc"] = np.array(other_priors.rx2("lowerbound_logQc"))[0]
    prior_dict["upperbound_logQc"] = np.array(other_priors.rx2("upperbound_logQc"))[0]
    prior_dict["logWc_hat"] = np.array(other_priors.rx2("logWc_hat"))[0]
    prior_dict["logQc_hat"] = np.array(other_priors.rx2("logQc_hat"))[0]
    prior_dict["logQ_sd"] = np.array(other_priors.rx2("logQ_sd"))[0]
    prior_dict["logWc_sd"] = np.array(other_priors.rx2("logWc_sd"))[0]
    prior_dict["logQc_sd"] = np.array(other_priors.rx2("logQc_sd"))[0]
    prior_dict["Werr_sd"] = np.array(other_priors.rx2("Werr_sd"))[0]
    prior_dict["Serr_sd"] = np.array(other_priors.rx2("Serr_sd"))[0]
    prior_dict["dAerr_sd"] = np.array(other_priors.rx2("dAerr_sd"))[0]
    prior_dict["sigma_man"] = np.array(other_priors.rx2("sigma_man"))[0][0]
    prior_dict["sigma_amhg"] = np.array(other_priors.rx2("sigma_amhg"))[0][0]

def write_priors(sword_file, priors):
    """Appends priors to SWORD of Science file if valid parameter is True.
    
    Appends the fill value to priors if the valid parameters is False as prior
    data could not be determined.
    """

    # Retrieve NetCDF4 dataset
    dataset = nc.Dataset(sword_file, mode='a', format="NETCDF4")

    # Retrieve node group
    reach_grp = dataset["reach"]

    # Write priors to node group
    for key, value in priors.items():
        create_variable(reach_grp, key, value)

    # Close NetCDF4 dataset
    dataset.close()

def create_variable(group, name, value):
    """Create NetCDF4 variable and assign data to it."""

    netcdf_var = group.createVariable(name, "f8", fill_value = Output.FILL_VALUE)
    netcdf_var[np.isnan(netcdf_var)] = Output.FILL_VALUE
    netcdf_var.assignValue(value)