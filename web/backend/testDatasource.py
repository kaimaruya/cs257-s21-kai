import unittest
from datasource import *

class  DataSourceTester (unittest.TestCase):

    def test_two_variables(self):
        var1 = "Internet"
        var2 = "Drugs"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), data.getTwoVariables(var1, var2))
        
    def test_one_variable_x(self):
        var1 = "Internet"
        var2 = "None"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), data.getOneVariable(var1))
        
    def test_same_variable(self):
        var1 = "Internet"
        var2 = "Internet"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), data.getOneVariable(var1))
        
    def test_one_variable_y(self):
        var1 = "None"
        var2 = "Drugs"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), data.getOneVariable(var2))
        
    def test_both_none(self):
        var1 = "None"
        var2 = "None"
        data = DataSource()
        self.assertEqual(data.chooseMethod(var1, var2), "Error: Please select at least one variable")

if __name__ == "__main__":
    unittest.main()