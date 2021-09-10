from pathlib import Path
from os.path import getmtime
from datetime import datetime, timedelta


base_dir = Path('.').cwd()

directory = Path(base_dir / 'application' / 'static' / 'images' / 'uploads')

for img in directory.iterdir():
    modified_date_file = datetime.fromtimestamp(getmtime(img))
    if datetime.now() - modified_date_file > timedelta(hours=1):
        print(f'DELETING: {img.name}')
        # img.unlink()
