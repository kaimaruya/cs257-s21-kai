import psycopg2
import psqlConfig as config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt




class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self):
        self.connection = self.connect()

    @staticmethod
    def connect():
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        try:
            print("database = " + config.database + " user = " + config.user + " password = " +config.password)
            connection = psycopg2.connect(database=config.database, user=config.user,
                                          password=config.password, host=config.host)
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    def get_data(self, first_column, second_column="NONE"):
        '''
        Retreives the data in the specified column or columns

        Parameters:
            first_column - the first (or only) column to be retrieved
            second_column (optional) - the second column to be retrieved if specified, otherwise unused

        Returns:
            All data from the specified column(s)
        '''
        try:
            cursor = self.connection.cursor()
            if second_column == "NONE":
                query = "SELECT " + first_column + " FROM lonelinesssurveyshort;"
                cursor.execute(query, (first_column,))
            else:
                query = "SELECT " + first_column + ", " + second_column + " FROM lonelinesssurveyshort;"
                cursor.execute(query, (first_column, second_column,))
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None


    def plot_data(self, first_column, second_column="NONE"):
        data = self.get_data(first_column, second_column)
        if second_column == "NONE":
            self.__plot_bar(data, first_column)
            plt.savefig("static/plot.png", bbox_inches="tight")

    def __plot_bar(self, data, name):
        answer_frequencies = self.get_answer_frequencies(data)
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.bar(answer_frequencies[0].keys(), answer_frequencies[0].values())
        plt.suptitle(name)

    def get_answer_frequencies(self, data):
        answer_frequencies = []
        for column in data:
            column_answer_frequencies = {}
            for data_point in column:
                if data_point in column_answer_frequencies:
                    column_answer_frequencies[data_point] += 1
                else:
                    column_answer_frequencies[data_point] = 1
            answer_frequencies.append(column_answer_frequencies)
        return answer_frequencies


if __name__ == '__main__':
    data_source = DataSource()
    data_source.plot_data("doctor")
