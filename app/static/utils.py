import psycopg2 as pg

from typing import Optional, Union, Dict, List
from configparser import ConfigParser
from flask import Blueprint, Flask
from flask import current_app as app

app: Flask
bp = Blueprint('utils', __name__, template_folder='templates')


def execute_query(query: str, query_params: Optional[Union[Dict[str, Union[str, int]], List]] = None) -> List[Dict]:
    config: ConfigParser = app.config.get('file')
    db_config = config['postgresql']
    try:
        conn = pg.connect(host=db_config['host'], port=db_config['port'], database=db_config['database'],
                          user=db_config['user'], password=db_config['password'])
        cursor = conn.cursor()
    except pg.OperationalError as err:
        app.logger.error(f"Couldn't connect to database: {err}")
        return []

    try:
        cursor.execute(query, query_params)
    except pg.Error as err:
        app.logger.error(f"Error executing query: {err}")
        app.logger.debug(f"query:\n{query}\nquery_params:\n{query_params}")
        conn.rollback()
        return []
    else:
        results = cursor.fetchall()
        conn.commit()
        return results
    finally:
        cursor.close()
        conn.close()
