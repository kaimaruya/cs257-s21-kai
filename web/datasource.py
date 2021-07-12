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
        
    def get_data(self, question):
        '''
        Retrieves the number of times each response to a certain survey question is given.
        
        Parameters:
            question - the question name from which these data are to be retrieved.
            
        Returns:
            A list of single-element tuples each containing the count for one answer.
        '''
        answers = self.get_answers(question)
        try:
            cursor = self.connection.cursor()
            query = ""
            for answer in answers:
                if not len(query) == 0:
                    query += "\nUNION ALL\n"
                query += "SELECT COUNT(" + question + ") FROM lonelinesssurveyshort WHERE " + question + "='" + answer + "'"
            query += ";"
            cursor.execute(query, (question,))
            output = cursor.fetchall()
            for i in range(len(output)):
                output[i] = output[i][0]
            return output
        except Exception as e:
            print("Something went wrong when executing the data query: ", e)
            return None
    
    def get_answers(self, question):
        '''
        Retrieves every answer given to a question without duplicates. Does not include blank responses where the question was not asked.
        
        Parameters:
            question - the question name from which the answers are to be retrieved
            
        Returns:
            A list of the answers given
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT DISTINCT " + question + " FROM lonelinesssurveyshort WHERE NOT(" + question + "=' ') ;"
            cursor.execute(query, (question,))
            answers = cursor.fetchall()
            new_answers = []
            for answer in answers:
                new_answers.append(answer[0])
            return new_answers
        except Exception as e:
            print("Something went wrong when executing the answers query: ", e)
            return None
    
    def get_probability_of_two_answers(self, first_question, first_answer, second_question, second_answer):
        '''
        Returns the probability of one answer to one question occuring and a second answer to a second question also occuring. Essentially, the probability of both answers occuring.
        
        Parameters:
            first_question and second_question - the two questions/questions to be queried. There's no meaningful difference between the two.
            first_answer and second_answer - the two answers to their respective questions. Again, no meaningful difference except that they are specific to their corresponding     question
        
        Returns:
            A float containing the probability of both answers occuring together
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM lonelinesssurveyshort WHERE " + first_question + "='" + first_answer + "' AND " + second_question + "='" + second_answer + "'"
            query += "\nUNION ALL\n"
            query += "SELECT COUNT(*) FROM lonelinesssurveyshort WHERE NOT(" + first_question + "=' ') AND NOT(" + second_question + "=' ');"
            cursor.execute(query, (first_question, second_question))
            output = cursor.fetchall()
            # division and breaking the query results out of their list and their single-element tuples
            return (output[0][0]/float(output[1][0]))
        except Exception as e:
            print("Something went wrong when executing the probability query: ", e)
            return None
    
    def get_name(self, alias):
        '''
        Retreives the unshortened version of alias from the database
        
        Parameters:
            alias - the shortened name
            
        Returns:
            the full version of the name
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT fullname FROM aliases WHERE id = '" + alias + "';"
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong when executing the name query: '" + alias + "'", e)
            return alias
    

    def plot_data(self, first_question, second_question="NONE"):
        '''
        Plots the given question or questions in a bar chart if only one is provided or a heatmap if two questions are provided. Saves the resulting plot as plot.png
        
        Parameters:
            first_question: the first question to plot. The only one used if only one argument is given.
            second_question: the second question, defaults to "NONE" in which case only first_question will be used.
        '''
        self.fig = plt.figure()
        self.fig, self.ax = plt.subplots()
        
        if second_question == "NONE":
            self.__plot_bar(first_question)
        else:
            self.__plot_heatmap(first_question, second_question)
            
        
        self.fig.savefig("static/plot.png", bbox_inches="tight")
        

    def __plot_bar(self, question):
        '''
        Creates a bar chart of how often each answer to the provided question is given
            
        Parameters:
            question - The question whose answers are to be graphed.
        '''
        self.ax = self.fig.add_axes([0,0,1,1])
        self.ax.bar(self.get_answers(question), self.get_data(question))
        self.ax.set_xlabel(question)
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
        
    def __plot_heatmap(self, first_question, second_question):
        '''
        Creates a heatmap indicating the probability of each combination of responses. Does not account for situations where either question was not responded to.
        
        Parameters:
            first_question - the first question, which serves as the y-axis of the chart
            second_question - the second question, which serves as the x-axis of the chart
        '''
        
        first_answers = self.get_answers(first_question)
        second_answers = self.get_answers(second_question)
        
        probabilities = []
        i = -1
        for first_answer in first_answers:
            i += 1
            probabilities.append([])
            for second_answer in second_answers:
                probabilities[i].append(round(self.get_probability_of_two_answers(first_question, first_answer, second_question, second_answer) * 100,1))
                
        # probabilities must be converted to a numpy array to work with the heatmap function borrowed from the matplotlib documentation
        probabilities_array = np.array(probabilities)
        
        im, cbar = heatmap(probabilities_array, first_answers, second_answers, ax = self.ax, cbar_kw=dict(orientation='horizontal', cmap="bwr"), cbarlabel="Probability")
        texts = annotate_heatmap(im, valfmt="{x:.1f}%")
        self.ax.set_ylabel(first_question)
        self.ax.set_xlabel(second_question)
        self.fig.tight_layout()
        plt.show()
        self.fig.suptitle("Probability of a response to the second question given a response to the first question")
        
        
    
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.
    Code borrowed from https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_label(cbarlabel)

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    # ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap. 
    Code borrowed from https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

if __name__ == '__main__':
    data_source = DataSource()
    data_source.get_name("doctor")
    data_source.plot_data("doctor",)