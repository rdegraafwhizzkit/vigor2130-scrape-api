from helper.global_helpers import sha224
from json import dumps
import mysql.connector
from mysql.connector import Error


def index_objects(database, objects, table, id_function=lambda x: sha224(x)):
    if type(objects) == dict:
        index_objects(database, [objects], table, id_function)
    elif type(objects) == list:
        connection = None
        try:
            connection = mysql.connector.connect(
                host='raspberrypi.whizzkit.nl',
                database='home',
                user='home',
                password='Home123!'
            )
            for o in objects:
                o['id'] = id_function(o)
                try:
                    columns = ','.join([c for c, v in o.items()])
                    values = ''
                    for value in [v for c, v in o.items()]:
                        values = values + '{}{}'.format(
                            '' if '' == values else ',',
                            f"'{value}'" if str == type(value) else value
                        )
                    cursor = connection.cursor()
                    cursor.execute(f"REPLACE INTO {table} ({columns}) VALUES ({values})")
                    cursor.close()
                except Exception as ex:
                    print('Could not insert object {} into {}: {}'.format(dumps(o), table, ex))
        except Error as error:
            print(f'An error occurred: {error}')

        finally:
            if connection is not None and connection.is_connected():
                connection.commit()
                connection.close()
    else:
        raise Exception('Unable to load objects with type ' + str(type(objects)))


if __name__ == '__main__':
    index_objects(
        'home',
        [{'mac_address': '4c:32:75:95:c8:bb', 'velop': 'livingroom', 'timestamp': 1583359863}],
        'velop'
    )
