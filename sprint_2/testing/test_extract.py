from src.extract import *
import unittest

raw_data = extract_func()

def test_extract():
    outcome=extract_func()
    expected=268
    assert len(outcome)==expected

# Function to validate keys in dictionaries inside a list
def validate_keys_in_list(raw_data, required_keys):
    raw_data=extract_func()
    return all(set(required_keys).issubset(data.keys()) for data in raw_data)
    
class testingTable(unittest.TestCase):
    
    # TESTS FOR KEYS THAT ARE IN THE raw_data LIST, SO IF THESE HEADERS DO NOT APPEAR, UNIT TEST WILL FAIL
    def test_correct_keys(self):
        required_keys = ["date", "time","branch_name","order","total","trans_type"]
        self.assertTrue(validate_keys_in_list(raw_data, required_keys))

# RUN UNIT TESTS
if __name__ == "__main__":
    unittest.main()
