#!/usr/bin/env python

import os
import json
from getpass import getpass
from pathlib import Path
from datetime import date, timedelta
from itertools import product

from book import BookClient, Time, Category, Campus, Place, BookResult


CONFIG_PATH = os.getenv('TJU_CLI_CONFIG_PATH', 'config.json')

def main():
    config = json.loads(Path(CONFIG_PATH).read_text())
    client = BookClient()

    print('Logging in...')
    default_username = config.get('default_username', '')
    default_password = config.get('default_password', '')
    username = input('Username: ') or default_username
    password = getpass('Password: ') or default_password
    success = client.authenticate(username, password)
    if not (success and client.authenticated):
        print('Failed to log in')
        return

    input('Press any key to continue...')

    default_task = {
        'date': date.today() + timedelta(days=2),
        'category': Category.Badminton,
        'campus': Campus.PeiYangYuan,
    }

    times = [Time.NinteenToTwenty, Time.TwentyToTwentyOne]
    places = [
        Place.PeiYangYuanBadminton1, Place.PeiYangYuanBadminton2,
        Place.PeiYangYuanBadminton3, Place.PeiYangYuanBadminton4,
        Place.PeiYangYuanBadminton5, Place.PeiYangYuanBadminton6,
        Place.PeiYangYuanBadminton7, Place.PeiYangYuanBadminton8,
    ]
    tasks = [
        {'time': time, 'place': place}
        for time, place in product(times, places)
    ]
    tasks = [{**default_task, **task} for task in tasks]

    booked_times = set()
    booked_indices = set()

    for i in range(1000):
        print(f'\n[Try #{i}]')

        tried = False
        for j, task in enumerate(tasks):
            if task['time'] in booked_times:
                continue

            tried = True
            print(f'[Task #{j}]', end=' ')
            result = client.book(**task)

            if result is BookResult.Success:
                print('suceeded')
                booked_times.add(task['time'])
                booked_indices.add(j)
            elif result is BookResult.Invalid:
                print('invalid')
            elif result is BookResult.Failure:
                print('failed to book')
            else:
                print('unknown result')
        if not tried:
            break
    print(f'\nBooked indices: {", ".join(str(i) for i in booked_indices) or "none"}.')

if __name__ == "__main__":
    main()
