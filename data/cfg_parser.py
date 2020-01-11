import os
from configparser import ConfigParser


def set_db_name():
    while True:
        db_name = input("Please enter a new DB name: ")

        if db_name.isalnum() and db_name[0].isalpha():
            return db_name
        else:
            print("Invalid Name")


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    print("\nReading DB config...")
    # create parser and read ini configuration file

    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db
