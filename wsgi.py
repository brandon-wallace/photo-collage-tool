from application import create_app

app = create_app()

if __name__ == '__main__':
    app.app_context().push()
    app.run()

from application import celery
