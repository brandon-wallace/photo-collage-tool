# DevProjects - Photo Collage Tool

## Upload and combine images asynchronously using a task queue to create a photo collage. Select horizontally or vertically orientation with the option to set a border and background color. 

## Continuous Integration and continuous development deployment with Github Actions.

## Testing with Pytest.

## Python script set up with cron job scheduled to removes old files.

This is an open source project from [DevProjects](http://www.codementor.io/projects). Feedback and questions are welcome!

Find the project requirements here: [Online photo collage tool](https://www.codementor.io/projects/web/online-photo-collage-tool-atx32mwend)

## Technologies used

Built with:

* Python3 
* Flask 
* RabbitMQ 
* Celery 
* Pillow 
* Gunicorn
* Nginx

Development:

* Pytest

![tests](https://github.com/brandon-wallace/photo-collage-tool/actions/workflows/python-app.yml/badge.svg)

## Screenshot 

![screenshot 1](screenshot1.png)

![screenshot 2](screenshot2.png)

![screenshot 3](screenshot3.png)

## Example Images 

![example image 1](collage_20211008-032021.png)

![example image 2](collage_20211008-040629.png)

## Installation

Create a .env file.
```
$ vim .env

# Add the following lines.

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=<your_secret_key>
CELERY_RESULT_BACKEND='rpc://'  # For RabbitMQ
CELERY_BROKER_URL='<your_rabbitmq_url>'
UPLOADED_IMAGES_DEST='application/static/images/uploads'
DOWNLOAD_URL='</full/path/to/images>'
```

Install development dependancies.

```
$ pipenv install pytest --dev
```

Install dependancies.

```
$ pipenv install
```

Install RabbitMQ.

```
$ sudo apt install rabbitmq-server
```

Enable and start the rabbitmq server.

```
$ sudo systemctl enable rabbitmq-server
$ sudo systemctl start rabbitmq-server
```

Check status of the server.

```
$ sudo systemctl status rabbitmq-server

# Output

● rabbitmq-server.service - RabbitMQ broker
     Loaded: loaded (/lib/systemd/system/rabbitmq-server.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2021-11-14 22:20:58 EST; 4h 28min ago
   Main PID: 816 (beam.smp)
      Tasks: 27 (limit: 13977)
     Memory: 129.6M
        CPU: 1min 45.945s
     CGroup: /system.slice/rabbitmq-server.service
[...]
```

Start a celery worker.

```
$ celery -A application.tasks worker --loglevel=INFO

# Output

-------------- celery@server v5.1.2 (sun-harmonics)
-- ***** ----- 
- ******* ---- Linux-5.10.0-9-amd64-x86_64-with-glibc2.31 2021-11-15 02:51:48
 *** --- * --- 
 ** ---------- [config]
 ** ---------- .> app:         tasks:0x7ffb222e7550
 ** ---------- .> transport:   amqp://guest:**@127.0.0.1:5672//
 ** ---------- .> results:     rpc://
 *** --- * --- .> concurrency: 4 (prefork)
- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
-- ***** ----- 
-------------- [queues]
               .> celery           exchange=celery(direct) key=celery
[...]
```

In another terminal start the application.

```
$ flask run

# Output

 * Serving Flask app 'run.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-123-321
```

Browse to http://127.0.0.1:5000

Set up a crontab to delete old files on the server.

```
$ crontab -e

# Add this line to run script every 10 minutes.

10   *   *   *   *   python3 /var/www/photo-collage/application/remove_files.py
```


## License

[GPL3](https://choosealicense.com/licenses/gpl-3.0/)
Most open source projects use the GPL3 license.
