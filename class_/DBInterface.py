""" vim: set et sw=4 ts=4 sts=4: """
# Imports
try:
    import json
except:
    raise Exception('Failed to import json module')
try:
    import mysql.connector
except:
    raise Exception('Failed to import mysql module')


class DBInterface:
    """
    A class used to represent the Database Interface

    Attributes:
        __is_valid : bool
            is the database valid
        __dbi : database
            mysql database
        __dbi_cursor : cursor
            database cursor
        __last_result : none
            the last resuls
        __config : dict
            dict include host, user, passwd, database, port (optional)
    """

    __is_valid = False
    __dbi = None
    __dbi_cursor = None
    __last_result = None
    __config = None

    def __init__(self, config):
        if config is None or not isinstance(config, dict):
            raise Exception('Invalid db config')

        required = ['host', 'user', 'passwd', 'database']

        for x in required:
            if x not in config:
                raise Exception('Incomplete db config')

        if 'port' in config and config['port'] is None:
            del config['port']

        self.__config = config

        try:
            self.__dbi = mysql.connector.connect(**config)
        except:
            raise Exception('Failed to establish db connection')

        self.__dbi_cursor = self.__dbi.cursor(buffered=True, dictionary=True)
        self.__is_valid = True

    def run(self, sql, vals=None):
        """
        A fuction created to run a query

        Args:
            sql: string, sql query
            vals: optional, type can be list, tuple, or non-collection value

        Returns:
            False if query failed
            dict if successful/applicable
        """

        if not self.__is_valid:
            return False

        self.__last_result = None

        if vals is None:
            self.__dbi_cursor.execute(sql)

        else:
            # Make sure vals is a tuple
            if isinstance(vals, list):
                vals = tuple(vals)
            elif not isinstance(vals, tuple):
                vals = (vals,)

            try:
                self.__dbi_cursor.execute(sql, vals)
            except:
                return False

        try:
            self.__dbi.commit()
            return True
        except:
            return False

    def run_many(self, sql, vals):
        """
        A fuction created to run a query multiple times using supplied vals

        Args:
            sql: string, sql query
            vals: list of tuples or list of non-collection values

        Returns:
            True on success
            False on failure
        """

        if not self.__is_valid:
            return False

        self.__last_result = None

        try:
            self.__dbi_cursor.executemany(sql, vals)
            self.__dbi.commit()
            return True
        except:
            return False

    def view(self, sql, vals=None):
        """
        A fuction created to view queries

        Args:
            sql: string, sql query
            vals: optional, type can be list, tuple, or non-collection value

        Returns:
            False if query failed
            dict if successful/applicable
        """

        if not self.__is_valid:
            return False

        self.__last_result = None

        if vals is None:
            self.__dbi_cursor.execute(sql)

        else:
            # Make sure vals is a tuple
            if isinstance(vals, list):
                vals = tuple(vals)
            elif not isinstance(vals, tuple):
                vals = (vals,)

            try:
                self.__dbi_cursor.execute(sql, vals)
            except:
                return False

        try:
            res = self.__dbi_cursor.fetchall()
        except:
            return False

        if not isinstance(res, list):
            return False

        return res if len(res) > 0 else False

    def view_single(self, sql, vals=None):
        """
        A fuction created to view a query

        Args:
            sql: string, sql query
            vals: optional, type can be list, tuple, or non-collection value

        Returns:
            False if query failed or number of rows returned != 1
            dict if successful/applicable
        """

        res = self.view(sql, vals)

        if not res or len(res) != 1:
            return False

        return res[0]
