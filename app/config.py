import configparser
import os
from typing import Dict


def parse_config() -> Dict:
    config_file_path = 'config.ini'
    conf_file = configparser.ConfigParser()
    conf_file.read(config_file_path)
    config = {
        'postgresql': dict(
            host=os.environ.get('db_host') or conf_file['postgresql']['host'],
            port=5432,
            user=os.environ.get('db_user') or conf_file['postgresql']['user'],
            password=os.environ.get('db_password') or conf_file['postgresql']['password'],
            database=os.environ.get('db_database') or conf_file['postgresql']['database']),
        'env': dict(
            env=os.environ.get('env_env') or conf_file['env']['env']),
        'azure': dict(
            key=os.environ.get('azure_key') or conf_file['azure']['key'],
            host=os.environ.get('azure_host') or conf_file['azure']['host']),
        'email': dict(
            host=os.environ.get('email_host') or conf_file['email']['host'],
            port=os.environ.get('email_port') or conf_file['email']['port'],
            domain=os.environ.get('email_domain') or conf_file['email']['domain'],
            user=os.environ.get('email_user') or conf_file['email']['user'],
            password=os.environ.get('email_password') or conf_file['email']['password'],
            recipient=os.environ.get('email_recipient') or conf_file['email']['recipient'],
            tls=os.environ.get('email_tls') or conf_file['email']['tls'],
            ssl=os.environ.get('email_ssl') or conf_file['email']['ssl'],)
    }

    return config
