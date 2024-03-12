import sqlite3


def db_routine(func):
    """
    Decorator function to handle database connection and disconnection for the wrapped function.
    """

    def wrapper(*args, **kwargs):
        """
        A wrapper function that handles the database connection for the given function.

        Parameters:
            *args: Variable length argument list.

        Returns:
            The result of the given function.
        """
        db_object = args[0]
        db_object.connection = db_object.get_db_connection()
        db_object.cursor = db_object.connection.cursor()
        result = func(*args, **kwargs)
        db_object.connection.commit()
        db_object.connection.close()
        return result

    return wrapper


class DBManager:
    def __init__(self, db_path="./data/AQ.db"):
        """
        Initializes a new instance of the DBManager class.
        :param db_path: The path to the database file.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row
        self.conn.close()

    def get_db_connection(self):
        """
        Function to establish a connection to the database.
        :return: sqlite3 connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @db_routine
    def create_table(self, schema_path="./data/schema.sql"):
        """
        A database routine to create a table from the specified schema file.
        :param schema_path: The path to the schema file
        :return: None
        """
        with open(schema_path, 'r') as schema_file:
            schema_sql = schema_file.read()
        self.cursor.executescript(schema_sql)

    @db_routine
    def insert_values(self, table_name, **kwargs):
        """
        A database routine to insert values into the specified table.
        :param table_name: The name of the table to insert values into
        :param kwargs: The key-value pairs to be inserted into the table
        :return: None
        """
        question_marks_str = "(" + ','.join(['?'] * len(kwargs)) + ")"
        columns_str = "(" + ','.join(list(kwargs.keys())) + ")"
        query_str = '''INSERT INTO {} {} VALUES {}'''.format(table_name, columns_str, question_marks_str)
        self.cursor.execute(query_str, tuple(kwargs.values()))

    @db_routine
    def get_values(self, table_name, *args):
        """
        A database routine to get values from the specified table.
        :param table_name: The name of the table to get values from
        :param args: The columns to get values from
        :return: A list of dictionaries where each dictionary represents a row in the table
        """
        if not args:
            self.cursor.execute('''SELECT * FROM {}'''.format(table_name))
        else:
            self.cursor.execute('''SELECT {} FROM {}'''.format(','.join(list(args)), table_name))
        records = self.cursor.fetchall()
        return records

    @db_routine
    def update_values(self, table_name, condition_str, **kwargs):
        """
        A function to update values in the specified columns of a table based on the provided condition.

        Parameters:
            table_name (str): The name of the table to be updated.
            condition_str (str): The condition for the update operation.
            **kwargs: Additional keyword arguments representing the columns and their new values.
        """
        columns_str = ','.join(["{} = {}".format(key, value) for key, value in kwargs.items()])
        if not condition_str:
            self.cursor.execute('''UPDATE {} SET {}'''.format(table_name, columns_str))
        else:
            self.cursor.execute('''UPDATE {} SET {} WHERE {}'''.format(table_name, columns_str, condition_str))

    @db_routine
    def delete_values(self, table_name, condition_str):
        """
        Deletes values from the specified table based on the given condition.
        Parameters:
            table_name (str): The name of the table from which to delete values.
            condition_str (str): The condition for deleting values from the table.
        Returns:
            None
        """
        if not condition_str:
            self.cursor.execute('''DELETE FROM {}'''.format(table_name))
        else:
            self.cursor.execute('''DELETE FROM {} WHERE {}'''.format(table_name, condition_str))
