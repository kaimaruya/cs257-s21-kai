import unittest
from datasource import *

class TestDataSource (unittest.TestCase):

    def test_two_variables(self):
        var1 = "Internet"
        var2 = "Drugs"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), data.getTwoVariables(var1, var2))
        
    def test_one_variable(self):
        var1 = "Internet"
        var2 = "None"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), data.getOneVariable(var1))
        
    def test_same_variable(self):
        var1 = "Internet"
        var2 = "Internet"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), data.getOneVariable(var1))

if __name__ == "__main__":
    unittest.main()