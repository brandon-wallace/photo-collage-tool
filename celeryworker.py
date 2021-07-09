import os
from application import creat_app

app = creat_app()
app.app_context().push()

from application import celery
