import pymysql
import pymysql.cursors

from data.populate_db import read_db_config

sql_btc = "CREATE TABLE IF NOT EXISTS `btc_feargreed`.`BTC Data` ( `timestamp` BIGINT NOT NULL, `open` FLOAT NOT NULL, `high` FLOAT NOT NULL, `low` FLOAT NOT NULL,`close` FLOAT NOT NULL, `volume` FLOAT NULL, PRIMARY KEY (`timestamp`) ENGINE = InnoDB"

sql_fg = "CREATE TABLE IF NOT EXISTS `btc_feargreed`.`FearGreed` ( `timestamp` INT NOT NULL, `classification` VARCHAR(13) NULL, `value` INT NULL, PRIMARY KEY (`timestamp`), UNIQUE INDEX `timestamp_UNIQUE` (`timestamp` ASC) VISIBLE) ENGINE = InnoDB"


def create_table():
    """
    Pulls config file for DB to connect. Create table(s) if necessary.
    :param: None
    :return: Nothing
    """

    print('Connecting to MySQL database...')
    db_config = read_db_config()
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            print('Creating btc_data table')
            cursor.execute(sql_btc)
            print('Creating btc_data table')
            cursor.execute(sql_fg)
            print('Committing changes')
        connection.commit()
    finally:
        connection.close()
