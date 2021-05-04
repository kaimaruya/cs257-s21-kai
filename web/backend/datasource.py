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
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
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
        cursor = connection.cursor()

    def createTwoVariableTable(self, x, y):
        try:
            query = "CREATE TABLE results AS SELECT " + x + ", " + y + " FROM lonelinesssurveyshort;"
            self.cursor.execute(query, (x, y,))
            return self.cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def createOneVariableTable(self, x):
        try:
            query = "CREATE TABLE results AS SELECT " + x + " FROM lonelinesssurveyshort;"
            self.cursor.execute(query, (x,))
            return self.cursor.fetchall()
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def createGraphBasedOn(self, x, y):
        pass

if __name__ == '__main__':
    # your code to test your function implementations goes here.
    print(createTwoVariableTable("LonelinessFrequency", "LeftOut"))
