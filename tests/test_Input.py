# Standard library imports
import unittest

# Third party imports
import numpy as np

# Local imports
from app.Input import check_observations

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
        print(obs_dict)
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


if __name__ == "__main__":
    unittest.main()