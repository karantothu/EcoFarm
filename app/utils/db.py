import mysql
import mysql.connector
from mysql.connector import Error, errorcode
from mysql.connector import pooling


class DB:

    def __init__(self, pool_size=None, pool_name=None, database=None, host=None,
                 port=None, user=None, password=None):
        self.pool_size = pool_size
        self.pool_name = pool_name
        self.database = database
        self.host = host
        if port is None:
            port = 3306
        self.port = int(port)
        self.user = user
        self.password = password
        self.connection_pool = None

    def create_conn_pool(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name=self.pool_name,
                                                                               pool_size=self.pool_size, user=self.user,
                                                                               password=self.password, port=self.port,
                                                                               host=self.host, database=self.database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Error("Something is wrong with your Username and Password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Error("Database does not exist")
            else:
                raise Error(err)
        return self.connection_pool


class DBInit:
    def __init__(self):
        self.db_config = {
            "pool_name": "DB_POOL",
            "pool_size": 5,
            "user": "user",
            "password": "password",
            "database": "eco_farm",
            "host": "127.0.0.1",
            "port": 3306
        }
        self.conn_pool = DB(**self.db_config).create_conn_pool()

    def fetch_all(self, query):
        results = None
        try:
            __conn = self.conn_pool.get_connection()
        except mysql.connector.errors.PoolError as err:
            print("Unable to pull the connection: {}".format(err))
        else:
            if __conn.is_connected():
                cursor = __conn.cursor()
                try:
                    cursor.execute(query)
                except mysql.connector.Error as err:
                    cursor.close()
                    __conn.close()
                    print("Something went wrong: {}".format(err))
                else:
                    columns = [col[0] for col in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    # results = cursor.fetchall()
                    cursor.close()
                    __conn.close()
        return results

    def close_conn(self):
        num_conn_closed = self.conn_pool._remove_connections()
        print('Connections_closed: {}'.format(num_conn_closed))

    def conn_queue(self):
        return self.conn_pool._cnx_queue

    def fetch_one(self, query):
        result = None
        try:
            __conn = self.conn_pool.get_connection()
        except mysql.connector.errors.PoolError as err:
            print("Unable to pull the connection: {}".format(err))
        else:
            if __conn.is_connected():
                cursor = __conn.cursor()
                try:
                    cursor.execute(query)
                except mysql.connector.Error as err:
                    cursor.close()
                    __conn.close()
                    print("Something went wrong: {}".format(err))
                else:
                    columns = [col[0] for col in cursor.description]
                    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    # result = cursor.fetchone()
                    cursor.close()
                    __conn.close()
        if result:
            return result[0]
        else:
            result = None
            return result

    def execute(self, query):
        result = None
        try:
            __conn = self.conn_pool.get_connection()
        except mysql.connector.errors.PoolError as err:
            print("Unable to pull the connection: {}".format(err))
        else:
            if __conn.is_connected():
                cursor = __conn.cursor()
                try:
                    cursor.execute(query)
                except mysql.connector.Error as err:
                    cursor.close()
                    __conn.close()
                    print("Something went wrong: {}".format(err))
                else:
                    # columns = [col[0] for col in cursor.description]
                    # rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    __conn.commit()
                    print("Query executed successfully.")
                    cursor.close()
                    __conn.close()
        return result






