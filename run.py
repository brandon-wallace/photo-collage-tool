from application import create_app

app = create_app()
app.app_context().push()

# if __name__ == '__main__':
#     app.run(debug=True)

from application import celery
