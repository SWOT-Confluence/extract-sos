# Standard library imports
import unittest

# Third party imports
import numpy as np
from numpy.testing import assert_allclose

# Local imports
from app.Input import Input, check_observations

class TestInput(unittest.TestCase):
    """Tests methods from Input class."""

    # Valid data
    VALID_WIDTH = np.reshape(np.arange(0, 50, dtype=float), (5, 10))
    VALID_DA = np.reshape(np.arange(0, 50, dtype=float), (5, 10))
    VALID_SLOPE = np.reshape(np.arange(0, 50, dtype=float), (5, 10))
    VALID_QHAT = np.repeat(2.3, 10)

    # Invalid negative data
    INVALID_WIDTH = np.reshape(np.arange(-51, -1, dtype=float), (5, 10))
    INVALID_SLOPE = np.reshape(np.arange(-51, -1, dtype=float), (5, 10))
    INVALID_QHAT = np.repeat(-1.0, 10)

    # Invalid NaN data
    NAN_WIDTH = np.reshape(np.arange(0, 80, dtype=float), (8, 10))
    NAN_WIDTH[NAN_WIDTH < 50] = np.NAN
    NAN_SLOPE = np.reshape(np.arange(0, 80, dtype=float), (8, 10))
    NAN_SLOPE[:, :6] = np.NAN
    NAN_DA = np.reshape(np.arange(0, 80, dtype=float), (8, 10))
    NAN_DA[NAN_DA < 50] = np.NAN
    NAN_DA[:, :6] = np.NAN
    NAN_QHAT = np.repeat(np.NaN, 10)

    def test_check_observations_valid(self):
        """Tests check_observations function on valid observation data."""

        # Execute function
        obs_dict = check_observations(self.VALID_WIDTH, self.VALID_DA, 
            self.VALID_SLOPE, self.VALID_QHAT)

        # Assert that observation values have not changed
        self.assertTrue(np.array_equal(obs_dict["width"], self.VALID_WIDTH))
        self.assertTrue(np.array_equal(obs_dict["d_x_area"], self.VALID_DA))
        self.assertTrue(np.array_equal(obs_dict["slope2"], self.VALID_SLOPE))
        self.assertTrue(np.array_equal(obs_dict["Qhat"], self.VALID_QHAT))
    
    def test_check_observations_invalid(self):
        """Tests check_observations function on invalid observation data."""

        # Execute function with invalid slope
        obs_dict = check_observations(self.VALID_WIDTH, self.VALID_DA, 
            self.INVALID_SLOPE, self.VALID_QHAT)
        self.assertFalse(obs_dict)

        # Execute function with invalid width
        obs_dict = check_observations(self.INVALID_WIDTH, self.VALID_DA, 
            self.VALID_SLOPE, self.VALID_QHAT)
        self.assertFalse(obs_dict)

        # Execute function with invalid qhat
        obs_dict = check_observations(self.VALID_WIDTH, self.VALID_DA, 
            self.VALID_SLOPE, self.INVALID_QHAT)
        self.assertFalse(obs_dict)

        # Execute function with invalid slope and width
        obs_dict = check_observations(self.INVALID_WIDTH, self.VALID_DA, 
            self.INVALID_SLOPE, self.INVALID_QHAT)
        self.assertFalse(obs_dict)

    def test_check_observations_nan(self):
        """Tests check_observations function on NaN values."""

        # Execute function with invalid slope - not enough time steps
        obs_dict = check_observations(self.VALID_WIDTH, self.VALID_DA, 
            self.NAN_SLOPE, self.VALID_QHAT)
        self.assertFalse(obs_dict)

        # Execute function with invalid width - not enough nodes
        obs_dict = check_observations(self.NAN_WIDTH, self.VALID_DA, 
            self.VALID_SLOPE, self.VALID_QHAT)
        self.assertFalse(obs_dict)

        # Execute function with invalid dA - not enough nodes and time steps
        obs_dict = check_observations(self.VALID_WIDTH, self.NAN_DA, 
            self.VALID_SLOPE, self.VALID_QHAT)
        self.assertFalse(obs_dict)

        # Execute function with invalid qhat
        obs_dict = check_observations(self.VALID_WIDTH, self.VALID_DA, 
            self.VALID_SLOPE, self.NAN_QHAT)
        self.assertFalse(obs_dict)

        # Execute function with all invalid observations
        obs_dict = check_observations(self.NAN_WIDTH, self.NAN_DA, 
            self.NAN_SLOPE, self.NAN_QHAT)
        self.assertFalse(obs_dict)

    def test_format_data(self):
        # Create Input object and run format method
        input = Input("tests/test_data/001_1_SWOT.nc", "tests/test_data/001_1_SOS.nc")
        input.format_data()
        
        # Create expected data
        dxa = np.array([358.2, 353.1, 274.5, 304.5, 309.9,
            159.6, 120.6, 129.0, 156.0, 150.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            -137.1, -153.9, -206.4, -193.2, -210.0,
            -360.0, -371.4, -459.9, -395.1, -410.4]).reshape(5,5)
        slope_reach = np.array([0.013247, 0.011991, 0.011540, 0.010223, 0.009850])
        slope2 = np.tile(slope_reach, (5, 1))
        width = np.full((5, 5), 30.0)
        
        # Assert result
        assert_allclose(dxa, input.data["d_x_area"])
        assert_allclose(slope2, input.data["slope2"])
        assert_allclose(width, input.data["width"])
        self.assertAlmostEqual(12.90476190, input.data["Qhat"][0])

if __name__ == "__main__":
    unittest.main()