import psycopg2

def connect():
    '''
    Establishes a connection to the database with the following credentials:
        user - username, which is also the name of the database
        password - the password for this database on perlman
    Returns: a database connection.
    Note: exits if a connection cannot be established.
    '''
    try:
        connection = psycopg2.connect(database="bellonie", user="bellonie", password="recycle368bird")
    except Exception as e:
        print("Connection error: ", e)
        exit()
    return connection

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self):
        '''
        Note: if you choose to implement the constructor, this does *not* count as one of your implemented methods.
        '''
        self.cursor = connection.cursor()

    def createTwoVariableTable(self, x, y):
        try:
            query = "SELECT " + x + ", " + y + " FROM lonelinesssurveyshort;"
            self.cursor.execute(query, (x, y,))
            return self.cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def createOneVariableTable(self, x):
        try:
            query = "SELECT " + x + " FROM lonelinesssurveyshort;"
            self.cursor.execute(query, (x,))
            return self.cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None
        
    '''Framework for create graph function that will be implemented later'''
    def createGraphBasedOn(self, table):
        pass
    
    '''Framework for converting long answer to short'''
    def convertLongToShort():
        pass

if __name__ == '__main__':
    # your code to test your function implementations goes here.
    connection = connect()
    data = DataSource()
    #Testing two variable table API
    print("Testing Two Variable Table")
    print(data.createTwoVariableTable("LonelinessFrequency", "LeftOut"))
    #Testing one variable table API
    print("Testing One Variable Table")
    print(data.createOneVariableTable("Lonely"))
    connection.close()
