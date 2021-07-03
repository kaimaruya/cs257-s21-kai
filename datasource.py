import psycopg2
import psqlConfig as config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np




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
            connection = psycopg2.connect(database=config.database, user=config.user,
                                          password=config.password, host=config.host)
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection
        
    def get_data(self, column):
        answers = self.get_answers(column)
        try:
            cursor = self.connection.cursor()
            query = ""
            for answer in answers:
                if answer == ('No Response',):
                    answer = (' ',)
                if not len(query) == 0:
                    query += "\nUNION ALL\n"
                query += "SELECT COUNT(" + column + ") FROM lonelinesssurveyshort WHERE " + column + "='" + answer[0] + "'"
            query += ";"
            cursor.execute(query, (column,))
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None
    
    def get_answers(self, column):
        try:
            cursor = self.connection.cursor()
            query = "SELECT DISTINCT " + column + " FROM lonelinesssurveyshort;"
            cursor.execute(query, (column,))
            answers = cursor.fetchall()
            for answer in answers:
              if answer == (' ',):
                  answer = ('No Response',)
            return answers
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None
    
    def get_comparative_data(self, first_column, second_column):
        first_answers = get_answers(first_column)
        second_answers = get_answers(seond_column)
        try:
            cursor = self.connection.cursor()
            query = ""
            for first_answer in first_answers:
                if first_answer == ('No Response',):
                    first_answer = (' ',)
                for second_answer in second_answers:
                    if second_answer == ('No Response',):
                        second_answer = (' ',)
                    if not len(query) == 0:
                        query += "\nUNION ALL\n"
                    query += "SELECT COUNT(" + first_column + ", " + second_column + ") FROM lonelinesssurveyshort WHERE " 
                    query += first_column + "='" + first_answer[0] + " AND(" + second_column + "='" + second_answer[0] + "')"
            query += ";"
            print(query)
            cursor.execute(query, (column,))
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None
        
    
    def get_name(self, alias):
        '''
        retreives the unshortened version of alias from the database
        
        Parameters:
            alias - the shortened name
            
        Returns:
            the full version of the name
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT fullname FROM aliases WHERE id = " + alias + ";"
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None
    

    def plot_data(self, first_column, second_column="NONE"):
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0,0,1,1])
        
        if second_column == "NONE":
            self.__plot_bar(first_column)
        else:
            self.__plot_two_variables(first_column, second_column)
            
        
        self.fig.savefig("plot.png", bbox_inches="tight")
        

    def __plot_one_variable(self, column):
        answers = get_answers(column)
        ax.bar(get_answers(column), get_data(column))
        self.fig.suptitle(get_name(first_column))
    
    def __plot_two_variables(self, first_column, second_column):
        first_answers = get_answers(first_column)
        second_answers = get_answers(seond_column)
        num_bars = len(first_answers) * len(second_answers)
        bar_x_positions = np.arrange(num_bars)
        ax.bar(bar_x_positions, 
        
if __name__ == '__main__':
    data_source = DataSource()
    print(data_source.get_comparative_data('doctor', 'socialgroup'))
