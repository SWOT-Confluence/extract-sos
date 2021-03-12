# Standard library imports
from shutil import copyfile
import unittest

# Third party imports
import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np
from numpy.testing import assert_almost_equal

# Local imports
from app.Input import Input
from app.GeoBAM import GeoBAM
from app.Output import Output, insert_invalid

class TestOutput(unittest.TestCase):
    """Tests methods from Output class."""

    def test_output(self):
        """Sort of integration test for append priors output."""

        # Get input data
        input = Input("tests/test_data/001_1_SWOT.nc", "tests/test_data/001_1_SOS.nc")
        input.format_data()

        # Pass input data to bam_data
        geobam = GeoBAM(input.data)
        data = geobam.bam_data()
        priors = geobam.bam_priors(data)

        # Copy output file so it is not overwritten
        copyfile("tests/test_data/001_1_SOS.nc", "tests/test_data/001_1_SOS_append.nc")
        
        # Write output
        output = Output("tests/test_data/001_1_SOS_append.nc", priors, [])
        output.append_priors()

        # Assert priors exist in file
        sos = Dataset("tests/test_data/001_1_SOS_append.nc")
        self.assertEqual("SoS of Science data for reach ID: 001_1", sos.title)
        self.assertEqual(1, getattr(sos, "valid"))
        self.assertTrue(isinstance(sos["reach/Qhat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/Qsd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["node/river_type"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_A0"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_A0"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_logn"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_logn"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_b"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_b"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_logWb"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_logWb"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_logDb"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_logDb"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_logr"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_logr"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logA0_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logn_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/b_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logWb_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logDb_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logr_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logA0_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logn_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/b_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logWb_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logDb_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logr_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_logQ"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_logQ"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_logWc"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_logWc"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/lowerbound_logQc"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/upperbound_logQc"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logWc_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logQc_hat"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logQ_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logWc_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/logQc_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/Werr_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/Serr_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/dAerr_sd"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/sigma_man"], nc._netCDF4.Variable))
        self.assertTrue(isinstance(sos["reach/sigma_amhg"], nc._netCDF4.Variable))

    def test_concatenate_invalid(self):
        
        # Create river type array
        river_types = np.array([7, 10, 11, 11, 10, 7, 11, 10, 7, 7], dtype=float)

        # Remove invalid nodes
        invalid_node_indexes = [1, 3, 7]
        river_types = np.delete(river_types, invalid_node_indexes, axis = 0)

        # Insert NaN for invalid nodes
        for index in invalid_node_indexes:
            river_types = np.insert(river_types, index, np.nan)
        
        # Assert expected result
        expected = np.array([7, np.nan, 11, np.nan, 10, 7, 11, np.nan, 7, 7])
        assert_almost_equal(expected, river_types)

    def test_insert_invalid(self):

        # Invalid indexes
        invalid_indexes = [5, 9, 11, 14, 17, 18, 19, 20, 21, 22, 23, 25, 28, 31,
            32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50]

        # River types (including numpy representation of R's NA values)
        river_types = np.array([7,10,11,7,11,11,10,10,-2147483648,-2147483648,
            -2147483648,-2147483648,-2147483648,-2147483648,-2147483648,
            -2147483648,-2147483648,-2147483648,-2147483648,-2147483648,
            -2147483648,7,-2147483648])
        
        expected = [7,10,11,7,11,-9999,
        11,10,10,-9999,-9999,-9999,-9999,
            -9999,-9999,-9999,-9999,-9999,-9999,-9999,
            -9999,-9999,-9999,-9999,-9999,-9999,-9999,
            -9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999,
            -9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999,-9999,
            -9999,-9999,-9999,-9999,-9999,-9999,
            -9999,7,-9999]

        # Execute function and assert result
        actual = insert_invalid(river_types, invalid_indexes)
        assert_almost_equal(expected, actual)