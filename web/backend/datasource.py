import psycopg2

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self):
        '''
        Constructor for the DataSource class
        '''
        self.connection = self.connect()

    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman
        Returns: a database connection.
        Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database="bellonie", user="bellonie", password="recycle368bird",
                                          host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    def chooseMethod(self, x, y):
        '''
        Determine whether to query two variables or one variable and call the corresponding function.

        Args:
            x (str): Column name for the first variable (e.g. "LonelinessFrequency")
            y (str): Column name for the second variable (e.g. "LeftOut")
        Returns:
            list: The output of either getTwoVariables() or getOneVariable()
        '''
        if x == "None" and y == "None":
            return "Error: Please select at least one variable"
        elif y == "None" or y == x:
            return self.getOneVariable(x)
        elif x == "None":
            return self.getOneVariable(y)
        return self.getTwoVariables(x,y)

    def getTwoVariables(self, x, y):
        '''
        Query the database for two variables and return the resulting columns.

        Args:
            x (str): Column name for the first variable (e.g. "LonelinessFrequency")
            y (str): Column name for the second variable (e.g. "LeftOut")
        Returns:
            list: A list containing both of the columns specified by x and y
        '''
        cursor = self.connection.cursor()
        try:
            query = "SELECT " + x + ", " + y + " FROM lonelinesssurveyshort;"
            cursor.execute(query, (x, y,))
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getOneVariable(self, x):
        '''
        Query the database for one variable and return the resulting column.

        Args:
            x (str): Column name of the desired variable (e.g. "Lonely")
        Returns:
            list: A list containing the specified column
        '''
        cursor = self.connection.cursor()
        try:
            query = "SELECT " + x + " FROM lonelinesssurveyshort;"
            cursor.execute(query, (x,))
            return cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def createGraphBasedOn(self, x, y):
        '''
        Create a graph based on two variables.

        Args:
            x (str): x-axis variable
            y (str): y-axis variable
        Returns:
            An image of the graph. Filetype is still TBD.
        '''
        pass

if __name__ == '__main__':
    # Test getTwoVariables() with columns titled "LonelinessFrequency" and "LeftOut"
    print("Testing Query for Two Variables")
    data = DataSource()
    print(data.getTwoVariables("LonlinessFrequency", "LeftOut"))
    # Test getOneVariable() with the column titled "Lonely"
    print("Testing Query for One Variable")
    print(data.getOneVariable("Lonely"))
