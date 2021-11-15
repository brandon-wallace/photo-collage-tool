'''
application/remove_files.py

Remove files after a specified time to save space.
'''

import logging
import logging.handlers

from pathlib import Path
from os.path import getmtime
from datetime import datetime, timedelta

logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)

handler = logging.handlers.SysLogHandler(address='/dev/log')
logger.addHandler(handler)

base_dir = Path('.').cwd()

images_path = Path(base_dir / 'application' / 'static' / 'images' / 'uploads')


def remove_old_files(hours):
    '''Remove old files to save space'''

    total_size = []

    for image in images_path.iterdir():
        modified_date_file = datetime.fromtimestamp(getmtime(image))
        if datetime.now() - modified_date_file > timedelta(hours=hours):
            total_size.append(image.stat().st_size)
            print(f'DELETING: {image.name}')
            image.unlink()

    total = sum([size + size for size in total_size])
    return total


def convert_bytes(size):
    '''Convert bytes to human readable format'''

    if size >= 1024:
        return f'Total Deleted: {(round(size / (1024 * 1024), 2))} KB'
    if size >= 1048576:
        return f'Total Deleted: {(round(size / (1024 * 1024), 3))} MB'
    if size >= 1048576000:
        return f'Total Deleted: {(round(size / (1024 * 1024), 4))} GB'
    return None


def main():
    '''Main function'''

    total = remove_old_files(1)
    logger.info(convert_bytes(total))


if __name__ == '__main__':
    main()
