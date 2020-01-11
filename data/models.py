import pymysql
import pymysql.cursors
from data.cfg_parser import read_db_config, set_db_name
import inspect

db_config = read_db_config()

db_name = db_config['database']


def create_tables():
    """
    Connects to DB. Create table(s) if necessary.
    :param: None
    :return: Nothing
    """
    global db_name
    if not db_name:
        db_name = set_db_name()
        print("Database set successfully to: " + db_name)
        print("To permanently set DB name edit " + inspect.getfullargspec(read_db_config).defaults[0])

    drop_db = "DROP DATABASE IF EXISTS " + db_name + ";"

    create_db = "CREATE DATABASE IF NOT EXISTS " + db_name + ";"

    btc_table = "CREATE TABLE IF NOT EXISTS `" + db_name + "`.`btc_data` (`index` INT NOT NULL, `timestamp` INT NOT NULL, `date` varchar(45) NOT NULL, `open` float NOT NULL, `high` float NOT NULL, `low` float NOT NULL, `close` float NOT NULL, `volume` float DEFAULT NULL, PRIMARY KEY (`timestamp`,`index`,`date`), UNIQUE KEY `index_UNIQUE` (`index`), UNIQUE KEY `timestamp_UNIQUE` (`timestamp`), UNIQUE KEY `date_UNIQUE` (`date`));"
    fg_table = "CREATE TABLE IF NOT EXISTS `" + db_name + "`.`feargreed` ( `index` INT NOT NULL, `timestamp` INT NOT NULL, `date` varchar(45) NOT NULL, `classification` varchar(15) DEFAULT NULL, `value` INT DEFAULT NULL, PRIMARY KEY (`timestamp`,`date`,`index`),UNIQUE KEY `index_UNIQUE` (`index`));"

    print(db_config)

    print('\nConnecting to MySQL database...\n')

    db_config['database'] = ""  # Connect first, try to create/use later
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            print('   Dropping {0}'.format(db_name))
            cursor._defer_warnings = True
            cursor.execute(drop_db)
            print('     -->Done')
            cursor._defer_warnings = False
            print('   Creating {0}'.format(db_name))
            cursor.execute(create_db)
            print('     -->Done')
            print('   Creating btc_data table')
            cursor.execute(btc_table)
            print('     -->Done')
            print('   Creating fg_data table')
            cursor.execute(fg_table)
            print('     -->Done')
        print('\nCommitting changes')
        connection.commit()
    finally:
        connection.close()
