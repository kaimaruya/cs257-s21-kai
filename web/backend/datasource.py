import psycopg2

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
        pass

    def getMagnitudesInRange(self, start, end=10.0):
        '''
        Returns a list of all of the magnitudes from the specified starting magnitude until the specified ending magnitude.

        PARAMETERS:
            start - the low end of the magnitude range
            end - the high end of the magnitude range (default: 10.0)

        RETURN:
            a list of all of the earthquake events with magnitudes in the specified range
        '''
        return []

    def getQuakesOnContinent(self, continent):
        '''
        Returns a list of all of the earthquakes that occurred on the specified continent.

        PARAMETERS:
            continent 
        
        RETURN:
            a list of all of the earthquake events that occurred on this continent
        '''
        return []

    def getQuakesInDateRange(self, start, end):
        '''
        Returns a list of all of the earthquakes that occurred within the range of specified dates.

        PARAMETERS:
            start - the starting date of the range
            end - the ending date of the range

        RETURN:
            a list of all of the earthquake events that occurred within this date range.
        '''
        return []

if __name__ == '__main__':
    # your code to test your function implementations goes here.
    pass
