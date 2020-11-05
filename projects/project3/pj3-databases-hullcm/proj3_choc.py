import sqlite3
import plotly.graph_objs as go

###############################
# Name: Chloe Hull            #
# Uniqname: hullcm@umich.edu  #
###############################

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from a database called choc.db
DBNAME = 'choc.sqlite'

## Create connection to database and execute query
def execute_query(query):
    '''Executes the specified query to return
    the query results and close the database connection

    Parameters
    -----------
    query: str
        the string representation of the SQL query to be run

    Returns
    --------
    list
        a list of tuples that represents the query result
    '''
    connection = sqlite3.connect(DBNAME)
    cur = connection.cursor()
    result = cur.execute(query).fetchall()
    connection.close()
    return result


# Part 1: Implement logic to process user commands
def process_command(command):
    '''Processes raw command given by user. Reformats raw
    command into appropriate SQL query conditions. Based on
    the specified command, calls the appropriate function,
    then returns the results of that function as a list
    of tuples containing the user's requested information.

    ------------
    Parameters
    command: str
        search terms to be reformatted into SQL query

    ------------
    Returns
    list
        list of requested information, formatted as list of tuples
    '''
    ### split words from command, then do if statements for each of the 4 commands
    search_list = command.split()
    join_clause = '''INNER JOIN COUNTRIES BC ON Bars.BroadBeanOriginId=BC.ID
    INNER JOIN COUNTRIES CC ON Bars.CompanyLocationId=CC.ID
    '''
    where_clause = ' '
    limit_clause = ' '
    valid_words = ['bars', 'companies', 'countries', 'regions', 'country', 'region', 'sell', 'source', 'ratings', 'cocoa', 'number_of_bars', 'top', 'bottom', 'barplot'] 
    command_words = ['bars', 'companies', 'countries','regions']
    
    #count command words to test for invalid search based on command
    count = 0
    for word in search_list:
        if word in command_words:
            count += 1
    if count > 1:
        results = f"Command not recognized: {command}"
        return results

    #test for invalid searches based on parameters
    for word in search_list:
        if word.isnumeric() == False and word.split('=')[0] not in valid_words:
            results = f"Command not recognized: {command}"
            return results
        if 'companies' in search_list and 'source' in search_list:
            results = f"Command not recognized: {command}"
            return results
        if 'countries' in search_list:
            if 'country=' in word:
                results = f"Command not recognized: {command}"
                return results
        if 'regions' in search_list:
            if 'country=' in word or 'region=' in word:
                results = f"Command not recognized: {command}"
                return results
        if 'bars' in search_list and 'number_of_bars' in search_list:
            results = f"Command not recognized: {command}"
            return results
        
        if where_clause == ' ':
        # obtain Where By clause
            if 'country=' in word and 'source' in search_list:
                location_code = word.rsplit('=')
                where_clause = f"WHERE BC.Alpha2='{location_code[1].upper()}'"
            elif 'country=' in word and 'sell' in search_list:
                location_code = word.rsplit('=')
                where_clause = f"WHERE CC.Alpha2='{location_code[1].upper()}'"
            elif 'country=' in word and 'source' not in search_list and 'sell' not in search_list:
                location_code = word.rsplit('=')
                where_clause = f"WHERE CC.Alpha2='{location_code[1].upper()}'"
            elif 'region=' in word and 'source' in search_list:
                location_code = word.rsplit('=')
                where_clause =  f"WHERE BC.Region='{location_code[1].capitalize()}'"
            elif 'region=' in word and 'sell' in search_list:
                location_code = word.rsplit('=')
                where_clause =  f"WHERE CC.Region='{location_code[1].capitalize()}'"
            elif 'region=' in word:
                location_code = word.rsplit('=')
                where_clause =  f"WHERE CC.Region='{location_code[1].capitalize()}'"
            elif 'region=' not in search_list and 'country=' not in search_list and 'source' not in search_list and 'sell' not in search_list:
                where_clause = ' '
        
         ## obtain Order by clause
        if 'cocoa' in search_list and 'bars' in search_list:
            if 'bottom' in search_list:
                order_clause = 'ORDER BY Bars.CocoaPercent'
            else:
                order_clause = 'ORDER BY Bars.CocoaPercent DESC'
        elif 'number_of_bars' in word and 'bars' in search_list:
            agg_statement = 'count(*)'
            if 'bottom' in search_list:
                order_clause = 'ORDER BY Count(*)'
            else:
                order_clause = 'ORDER BY Count(*) DESC'
        elif 'cocoa' not in search_list and 'number_of_bars' not in search_list and 'bars' in search_list:
            if 'bottom' in search_list:
                order_clause = 'ORDER BY Bars.Rating'
            else:
                order_clause = 'ORDER BY Bars.Rating DESC'
    
        # obtain LIMIT clause
        if word.isnumeric():
            limit_clause = 'LIMIT ' + word
        elif limit_clause == ' ':
            limit_clause = 'LIMIT 10'
        
        #obtain group and having clause
        if 'companies' in search_list or 'countries' in search_list or 'regions' in search_list:
            if 'number_of_bars' in search_list:
                agg_statement = 'count(*)'
                if 'bottom' in search_list:
                    order_clause = 'ORDER BY Count(*)'
                else:
                    order_clause = 'ORDER BY Count(*) DESC'
            elif 'ratings' in search_list:
                agg_statement = 'AVG(Rating)'
                if 'bottom' in search_list:
                    order_clause = 'ORDER BY AVG(Rating)'
                else:
                    order_clause = 'ORDER BY AVG(Rating) DESC'
            elif 'cocoa' in search_list:
                agg_statement = 'AVG(CocoaPercent)'
                if 'bottom' in search_list:
                    order_clause = 'ORDER BY AVG(CocoaPercent)'
                else:
                    order_clause = 'ORDER BY AVG(CocoaPercent) DESC'
            elif 'ratings' not in search_list and 'cocoa' not in search_list and 'number_of_bars' not in search_list and 'regions' in search_list or 'countries' in search_list:
                agg_statement = 'AVG(Rating)'
                if 'bottom' in search_list:
                    order_clause = 'ORDER BY AVG(Rating)'
                else:
                    order_clause = 'ORDER BY AVG(Rating) DESC'
            elif 'number_of_bars' not in search_list and 'rating' not in search_list and 'cocoa' not in search_list and 'countries' not in search_list and 'regions' not in search_list:
                agg_statement = 'AVG(Rating)'
                if 'bottom' in search_list:
                    order_clause = 'ORDER BY Bars.Rating'
                else:
                    order_clause = 'ORDER BY Bars.Rating DESC'

            #obtain group and having clauses
            if 'companies' in search_list:
                group_clause = 'GROUP BY company'
                having_clause = 'HAVING count(*) > 4'
            if 'countries' in search_list:
                if 'source' in search_list:
                    group_clause = 'GROUP BY BC.EnglishName'
                    having_clause = 'HAVING count(*) > 4'
                    country_statement = 'BC.EnglishName'
                    region_statement = 'BC.Region'
                if 'sell' in search_list:
                    group_clause = 'GROUP BY CC.EnglishName'
                    having_clause = 'HAVING count(*) > 4'
                    country_statement = 'CC.EnglishName'
                    region_statement = 'CC.Region'
                elif 'source' not in search_list and 'sell' not in search_list:
                    group_clause = 'GROUP BY CC.EnglishName'
                    having_clause = 'HAVING count(*) > 4'
                    country_statement = 'CC.EnglishName'
                    region_statement = 'CC.Region'
            if 'regions' in search_list:
                if 'source' in search_list:
                    group_clause = 'GROUP BY BC.Region'
                    region_statement = 'BC.Region'
                elif 'sell' in search_list:
                    group_clause = 'GROUP BY CC.Region'
                    region_statement = 'CC.Region'
                elif 'source' not in search_list and 'sell' not in search_list:
                    group_clause = 'GROUP BY CC.Region'
                    region_statement = 'CC.Region'
    
    # call correct function depending on command
    results = ' '
    if 'bars' in search_list:
        results = bar_command(join_clause, where_clause, order_clause, limit_clause)
    if 'companies' in search_list:
        results = company_command(join_clause, where_clause, group_clause, having_clause, order_clause, limit_clause, agg_statement)
    if 'countries' in search_list:
        results = country_command(join_clause, where_clause, group_clause, having_clause, order_clause, limit_clause, agg_statement,country_statement,region_statement)
    if 'regions' in search_list:
        results = region_command(join_clause, where_clause, group_clause, order_clause, limit_clause, agg_statement, region_statement)
    if results == ' ':
        results = f"Command not recognized: {command}"
    return results


def load_help_text():
    with open('help.txt') as f:
        return f.read()


def bar_command(join_clause, where_clause, order_clause, limit_clause):
    '''Reformats provided conditions into appropriate
    SQL query. Returns the results of the query as a list.

    Parameters
    -----------
    join_clause: str
        the join clause to be included in SQL query
    where_clause: str
        the where clause to be included in SQL query
    order_clause: str
        the order clause to be included in SQL query
    limit_clause: str
        the limit clause to be included in SQL query

    Returns
    --------
    list
        list of requested information, formatted as list of tuples
    '''
    #query to be used
    QUERY = 'SELECT SpecificBeanBarName, Company, CC.EnglishName, Rating, CocoaPercent, BC.EnglishName FROM Bars' + ' ' + join_clause + ' ' + where_clause + ' ' + order_clause + ' ' + limit_clause

    #obtain query results
    results = execute_query(QUERY)
    return results


def company_command(join_clause, where_clause, group_clause, having_clause, order_clause, limit_clause, count_statement):
    '''Reformats provided conditions into appropriate
    SQL query. Returns the results of the query as a list.

    Parameters
    -----------
    join_clause: str
        the join clause to be included in SQL query
    where_clause: str
        the where clause to be included in SQL query
    group_clause: str
        the group clause to be included in SQL query
    having_clause: str
        the having clause to be included in SQL query
    order_clause: str
        the order clause to be included in SQL query
    limit_clause: str
        the limit clause to be included in SQL query
    count_statement: str
        the count statement to be included in the SQL query

    Returns
    --------
    list
        list of requested information, formatted as list of tuples
    '''
    
    #query to be used
    QUERY = f"SELECT Company, CC.EnglishName, {count_statement} FROM Bars {join_clause} {where_clause} {group_clause} {having_clause} {order_clause} {limit_clause}"
    
    #obtain query results
    results = execute_query(QUERY)
    return results

def country_command(join_clause, where_clause, group_clause, having_clause, order_clause, limit_clause, agg_statement, country_statement, region_statement):
    '''Reformats provided conditions into appropriate
    SQL query. Returns the results of the query as a list.

    Parameters
    -----------
    join_clause: str
        the join clause to be included in SQL query
    where_clause: str
        the where clause to be included in SQL query
    group_clause: str
        the group clause to be included in SQL query
    having_clause: str
        the having clause to be included in SQL query
    order_clause: str
        the order clause to be included in SQL query
    limit_clause: str
        the limit clause to be included in SQL query
    agg_statement: str
        the aggregation statement to be included in the SQL query
    country_statement: str
        the country statement to be included in the SQL query
    region_statement: str
        the region statement to be included in the SQL query

    Returns
    --------
    list
        list of requested information, formatted as list of tuples
    '''
    
    #query to be used
    QUERY = f"SELECT {country_statement}, {region_statement}, {agg_statement} FROM Bars {join_clause} {where_clause} {group_clause} {having_clause} {order_clause} {limit_clause}"

    #obtain query results
    results = execute_query(QUERY)
    return results


def region_command(join_clause, where_clause, group_clause, order_clause, limit_clause, agg_statement, region_statement):
    '''Reformats provided conditions into appropriate
    SQL query. Returns the results of the query as a list.

    Parameters
    -----------
    join_clause: str
        the join clause to be included in SQL query
    where_clause: str
        the where clause to be included in SQL query
    group_clause: str
        the group clause to be included in SQL query
    order_clause: str
        the order clause to be included in SQL query
    limit_clause: str
        the limit clause to be included in SQL query
    agg_statement: str
        the aggregation statement to be included in the SQL query
    region_statement: str
        the region statement to be included in the SQL query

    Returns
    --------
    list
        list of requested information, formatted as list of tuples
    '''
    
    #query to be used
    QUERY = f"SELECT {region_statement}, {agg_statement} FROM Bars {join_clause} {where_clause} {group_clause} {order_clause} {limit_clause}"

    #obtain query results
    results = execute_query(QUERY)
    return results

def reduce_words(word):
    '''Checks word length to ensure words longer than 12 
    characters are appropriately truncated. 

    Parameters
    ------------
    word: str
        word to be checked for length and reformatted if appropriate
    
    Returns
    ---------
    str
        word in appropriate formatting
    '''
    new_word = word[:12] + '...'
    return new_word


def format_table(results):
    '''Reformats SQL Query results into a table and
    prints the table for the user to see.

    Parameters
    ------------
    results: list
        list of tuples that contains the results from the SQL query

    Returns
    -------
    None
    '''
    #reformat words if greater than 12 chars
    results_to_use = []
    for item in results:
        words = []
        for word in item:
            if type(word) != float and len(str(word)) >= 15:
                word = reduce_words(word)
                words.append(word)
            if type(word) != float and len(str(word)) < 15:
                word = word
                words.append(word)
            if type(word) == float:
                word = word
                words.append(word)
        results_to_use.append(tuple(words))

    #determine number of rows to include in output & print for each column option
    for item in results_to_use:
        if len(item) == 2:
            if type(item[1]) == float:
                row = "{x1:<15s} {x2:<15.1f}".format
                print(row(x1=item[0], x2=item[1]))
            else:
                row = "{x1:<15s} {x2:<15n}".format
                print(row(x1=item[0], x2=item[1]))
        if len(item) == 3:
            if type(item[2]) == float:
                row = "{x1:<15s} {x2:<15s} {x3:<15.1f}".format
                print(row(x1=item[0], x2=item[1], x3=item[2]))
            else:
                row = "{x1:<15s} {x2:<15s} {x3:<15n}".format
                print(row(x1=item[0], x2=item[1], x3=item[2]))
        if len(item) == 4:
            row = "{x1:<15s} {x2:<15s} {x3:<15s} {x4:<15s}".format
            print(row(x1=item[0], x2=item[1], x3=item[2], x4=item[3]))
        if len(item) == 5:
            row = "{x1:<15s} {x2:<15s} {x3:<15s} {x4:<15s} {x5:<15s}".format
            print(row(x1=item[0], x2=item[1], x3=item[2], x4=item[3]))
        if len(item) == 6:
            row = "{x1!s:<15s} {x2!s:<15s} {x3!s:<15s} {x4:<6.1f} {x5:<6.0%} {x6!s:<15s}".format
            print(row(x1=item[0], x2=item[1], x3=item[2], x4=item[3],x5=item[4],x6=item[5]))


def create_plot(results, user_input):
    '''Takes SQL query results and creates
    a bar plot using plotly. Opens the barplot
    in an HTML page and saves to computer.

    Parameters
    ------------
    results: list
        list of tuples that contains the results from the SQL query
    user_input: str
        raw input provided by the user

    Returns
    -------
    None
    '''
    #generate info for plot
    x_axis = []
    y_axis = []
    if 'bars' in user_input and 'number_of_bars' not in user_input:
        for item in results:
            x_axis.append(item[0])
        if 'cocoa' in user_input:
            for item in results:
                y_axis.append(item[4])
        else:
            for item in results:
                y_axis.append(item[3])
    if 'companies' in user_input:
        for item in results:
            x_axis.append(item[0])
            y_axis.append(item[2])
    if 'countries' in user_input:
        for item in results:
            x_axis.append(item[0])
            y_axis.append(item[2])
    if 'regions' in user_input:
        for item in results:
            x_axis.append(item[0])
            y_axis.append(item[1])
    
    #generate plot
    graph_data = go.Bar(x=x_axis,y=y_axis)
    fig = go.Figure(data=graph_data)
    fig.write_html("barplot.html", auto_open=True)

# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = input('Enter a command: ')
    while response.lower() != 'exit':
        if response == 'help':
            print(help_text)
            response = input('Enter a command: ')
        else:
            results = process_command(response)
            while 'Command not recognized' in results and response != 'exit' and response != 'help':
                print(results)
                print(' ')
                response = input('Enter a command: ')
                if response == 'help':
                    print(help_text)
                    response = input('Enter a command: ')
                results = process_command(response)
            if 'barplot' in response:
                create_plot(results, response)
            else:
                format_table(results)
            if response.lower() != 'exit':
                print(' ')
                response = input('Enter a command: ')
    print('Bye!')
    exit()

    
        
# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()
