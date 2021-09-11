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

img_path = Path(base_dir / 'application' / 'static' / 'images' / 'uploads')

total_size = []

for img in img_path.iterdir():
    modified_date_file = datetime.fromtimestamp(getmtime(img))
    if datetime.now() - modified_date_file > timedelta(hours=1):
        total_size.append(img.stat().st_size)
        print(f'DELETING: {img.name}')
        # img.unlink()

total = sum([size + size for size in total_size])


def convert_bytes(size):
    '''Convert bytes to megabytes'''

    return f'Total Deleted: {(round(size / (1024 * 1024), 3))} MB'


logger.info(convert_bytes(total))
