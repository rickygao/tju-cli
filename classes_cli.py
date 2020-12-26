#!/usr/bin/env python

import os
import json
from getpass import getpass
from pathlib import Path

from classes import ClassesClient, show_and_input


CONFIG_PATH = os.getenv('TJU_CLI_CONFIG_PATH', 'config.json')

def format_table(table):
    if len(table) == 0:
        return 'empty'

    head = ' '.join(table[0].keys())
    body = '\n'.join(' '.join(map(str, row.values())) for row in table)
    return head + '\n' + body

def main():
    config = json.loads(Path(CONFIG_PATH).read_text())
    client = ClassesClient()

    print('Logging in...')
    default_username = config.get('default_username', '')
    default_password = config.get('default_password', '')
    username = input('Username: ') or default_username
    password = getpass('Password: ') or default_password
    client.authenticate(username, password, show_and_input('Captcha: '))
    if not client.authenticated:
        print('Failed to log in')
        return

    print('Retrieving grade...')
    grade = client.retrieve_grade()

    print('=============== Overall  ===============')
    print(format_table([grade['overall']]))
    print('============== Semesters  ==============')
    print(format_table(grade['semesters']))
    print('=============== Courses  ===============')
    print(format_table(grade['courses']))


if __name__ == "__main__":
    main()
