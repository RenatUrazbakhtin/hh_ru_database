from configparser import ConfigParser

import psycopg2


def config(filename="src\database.ini", section="postgresql"):
    """
    Получает параметры подключения из файла filename
    :param filename: имя файла
    :param section: секция параметров
    :return:
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
