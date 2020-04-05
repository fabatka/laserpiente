import psycopg2 as pg

from typing import Optional, Union, Dict, List
from configparser import ConfigParser
from flask import Blueprint, Flask
from flask import current_app as app
from psycopg2.extras import DictCursor, DictRow
import psycopg2.sql as sql

app: Flask
bp = Blueprint('utils', __name__, template_folder='templates')


def execute_query(raw_query: str,
                  identifier_params: Optional[Dict[str, str]] = None,
                  query_params: Optional[Union[Dict[str, Union[str, int]], List]] = None) -> List[DictRow]:
    """
    :param raw_query: str The properly formatted raw query string. Value parameters should be escaped with %(param)s or
        one or more %s, identifier parameters should be escaped with {param}.
    :param identifier_params: dict This is mandatory if there are identifier parameters (like table or column names)
        used in the raw query.
    :param query_params: dict or list If the value parameters are escaped by name, dict must be used, otherwise list
    :return: list List of resulting rows in psycopg2's own type, DictRow
    """
    config: ConfigParser = app.config.get('file')
    db_config = config['postgresql']
    try:
        conn = pg.connect(host=db_config['host'], port=db_config['port'], database=db_config['database'],
                          user=db_config['user'], password=db_config['password'])
        cursor = conn.cursor(cursor_factory=DictCursor)
    except pg.OperationalError as err:
        app.logger.error(f"Couldn't connect to database: {err}")
        return []

    try:
        if identifier_params is not None:
            identifiers_map = {key: sql.Identifier(value) for key, value in identifier_params.items()}
            query = sql.SQL(raw_query).format(**identifiers_map)
        else:
            query = raw_query
        cursor.execute(query, query_params)
    except pg.Error as err:
        app.logger.error(f"Error executing query: {err}")
        app.logger.debug(f"\nquery:\n{raw_query}\n"
                         f"query_params:\n{query_params}\n"
                         f"identifier_params:\n{identifier_params}\n")
        conn.rollback()
        return []
    else:
        results = cursor.fetchall()
        conn.commit()
        return results
    finally:
        cursor.close()
        conn.close()
