'''
Name: Chloe Hull
Uniqname: hullcm@umich.edu
'''

import sqlite3

def connect_database():
    '''

    Parameters
    ------------
    None

    Returns
    [INSERT WHAT THIS RETURNS]
    '''
    connection = sqlite3.connect('Northwind_small.sqlite')
    cursor = connection.cursor()
    return connection


def execute_query(connection, query):
    '''Executes the specified query to return
    the query results and close the database connection

    Parameters
    -----------
    str
        the string representation of the SQL query to be run

    Returns
    --------
    list
        a list of tuples that represents the query result
    '''
    result = connection.execute(query).fetchall()
    connection.close()
    return result


def question0():
    ''' Constructs and executes SQL query to retrieve
    all fields from the Region table

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = "SELECT * FROM Region"
    result = execute_query(connection, query)
    return result


def question1():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = "SELECT * FROM Territory"
    result = execute_query(connection, query)
    return result


def question2():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = "SELECT count(LastName) FROM Employee"
    result = execute_query(connection, query)
    return result


def question3():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT *
    FROM Product
    ORDER BY ID DESC
    LIMIT 10
    '''
    result = execute_query(connection, query)
    return result


def question4():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT ProductName, UnitPrice
    FROM Product
    ORDER BY UnitPrice DESC
    LIMIT 3
    '''
    result = execute_query(connection, query)
    return result


def question5():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT ProductName, UnitPrice, UnitsInStock
    FROM Product
    WHERE UnitsInStock BETWEEN 60 and 100
    '''
    result = execute_query(connection, query)
    return result


def question6():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT ProductName
    FROM Product
    WHERE UnitsInStock < ReorderLevel
    '''
    result = execute_query(connection, query)
    return result


def question7():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT Id
    FROM [Order]
    WHERE ShipCountry='France' and ShipPostalCode LIKE '%04'
    '''
    result = execute_query(connection, query)
    return result


def question8():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT CompanyName, ContactName
    FROM Customer
    WHERE Country='UK' AND Fax <> 'Null'
    '''
    result = execute_query(connection, query)
    return result


def question9():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT product.ProductName, product.UnitPrice
        FROM Product
	        JOIN Category
		        ON product.CategoryId=Category.Id
			        WHERE Category.CategoryName='Beverages'
    '''
    result = execute_query(connection, query)
    return result


def question10():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT product.ProductName
        FROM Product
            JOIN Category
                ON product.CategoryId=Category.Id
                    WHERE Category.CategoryName='Meat/Poultry' AND Product.Discontinued='1'
    '''
    result = execute_query(connection, query)
    return result


def question11():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT [order].Id, Employee.FirstName, Employee.LastName
        FROM [Order]
            JOIN Employee
                ON [Order].EmployeeId=Employee.Id
                    WHERE [Order].ShipCountry='Germany'
    '''
    result = execute_query(connection, query)
    return result


def question12():
    ''' Constructs and executes SQL query to retrieve
    data based on requirements

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = connect_database().cursor()
    query = '''
    SELECT [Order].Id, [Order].OrderDate, Customer.CompanyName
        FROM [Order]
            JOIN Customer
                ON [Order].CustomerId=Customer.Id
                    WHERE [Order].OrderDate <= '2012-07-10'
    '''
    result = execute_query(connection, query)
    print(result)
    return result


#################################################################
########################  ECs start here  #######################
#################################################################

#########
## EC1 ##
#########

def print_query_result(raw_query_result):
    ''' Pretty prints raw query result

    Parameters
    ----------
    list
        a list of tuples that represent raw query result

    Returns
    -------
    None
    '''
    col_width = max(len(str(word)) for row in raw_query_result for word in row) + 2  # padding
    if len(raw_query_result) <= 2:
        for row in raw_query_result:
            print(" + ".join('-'*col_width for word in row))
            print(" | ".join(str(word).ljust(col_width) for word in row))
            print(" + ".join('-'*col_width for word in row))
    else:
        for row in raw_query_result:
            if row == raw_query_result[0] or row == raw_query_result[-1]:
                print(" + ".join('-'*col_width for word in row))
            else:
                print(" | ".join(str(word).ljust(col_width) for word in row))


if __name__ == "__main__":
    '''WHEN SUBMIT, UNCOMMENT THE TWO LINES OF CODE
    BELOW IF YOU COMPLETED EC1'''

    result = question9()
    print_query_result(result)

#########
## EC2 ##
#########
import re

info = input('''Please enter a Order Date and a Ship Country seperated by space
(e.g. 2012-07-04 France), or 'exit' to quit: ''')
r = re.compile('.*-.*-.*')
while info != 'exit':
    while r.match(info) is None and info != 'exit':
        info = input('''Invalid input. Please enter a Order Date and a Ship Country 
seperated by space(e.g. 2012-07-04 France), or 'exit' to quit: ''')
    while info == 'exit':
        exit()
    while r.match('xxxx-xx-xx') is not None:
        search_terms = info.split()
        connection = connect_database().cursor()
        query = str('''
            SELECT Employee.FirstName, Employee.LastName
            FROM [Order]
            JOIN Employee
            ON [Order].EmployeeId=Employee.Id
            WHERE [Order].OrderDate= '{0}' AND [Order].ShipCountry= '{1}' '''.format(search_terms[0], search_terms[1]))
        result = execute_query(connection, query)
        if result == []:
            print('Sorry! Your search returns no results.')
            exit()
        else:
            print_query_result(result)
            exit()
exit()

