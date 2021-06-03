import psycopg2
import matplotlib
import matplotlib.pyplot as plt

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
        self.oneVariable = False

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
            self.oneVariable = True
            return self.queryOneVariable(x)
        elif x == "None":
            self.oneVariable = True
            return self.queryOneVariable(y)
        return self.queryTwoVariables(x,y)

    def queryTwoVariables(self, x, y):
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

    def queryOneVariable(self, x):
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

    def createGraph(self, x, y):
        '''
        Create a graph based on two variables.

        Args:
            x (str): x-axis variable
            y (str): y-axis variable
        Returns:
            An image of the graph. Filetype is still TBD.
        '''
        
        queryResult = self.chooseMethod(x,y)
        
        xaxis = []
        yaxis = []
        ylist = []
        
        if self.oneVariable == True:
            for row in queryResult:
                if row[0] not in xaxis:
                    xaxis.append(str(row[0]))
                    yaxis.append(1)
                i = 0
                while row[0] != xaxis[i]:
                    i = i + 1
                yaxis[i] = yaxis[i] + 1

            plt.rc('xtick', labelsize=5)
            plt.clf()
            plt.bar(xaxis, yaxis)

            if x != "None":
                plt.title(x)
            elif y != "None":
                plt.title(y)
        else:
            plt.clf()
            for row in queryResult:
                if row[0] not in xaxis:
                    xaxis.append(str(row[0]))
                    yaxis.append(1)
                if row[1] not in ylist:
                    ylist.append(str(row[1]))
                i = 0
                while row[0] != xaxis[i]:
                    i = i + 1
                yaxis[i] = yaxis[i] + 1
            plt.bar(xaxis,yaxis)
            
            j = 0
            while j < len(ylist):
                for row in queryResult:
                    if row[1] == ylist[j]:
                        i = 0
                        while row[0] != xaxis[i]:
                            i = i + 1
                        yaxis[i] = yaxis[i] - 1
                plt.bar(xaxis,yaxis)
                j = j + 1

            plt.legend(ylist, title = y)
            plt.title(x + " vs " + y)
            plt.xlabel(x)
            plt.xticks(rotation=90)
            plt.ylabel("Number of Responses")
        
        plt.savefig("static/graph.png", bbox_inches="tight")
        
        pass

if __name__ == '__main__':
    # Test getTwoVariables() with columns titled "LonelinessFrequency" and "LeftOut"
    print("Testing Query for Two Variables")
    data1 = DataSource()
    print(data1.queryTwoVariables("Happiness", "Finances"))
    
    # Test getOneVariable() with the column titled "Lonely"
    print("Testing Query for One Variable")
    data2 = DataSource()
    print(data2.queryOneVariable("Lonely"))
