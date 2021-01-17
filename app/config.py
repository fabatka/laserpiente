import configparser
import os
from typing import Dict


def parse_config() -> Dict:
    config_file_path = 'config.ini'
    conf_file = configparser.ConfigParser()
    conf_file.read(config_file_path)
    config = {
        'postgresql': dict(
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            database=os.environ.get('DB_DB')),
        'env': dict(
            env=os.environ.get('ENV')),
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
