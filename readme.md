# DevProjects - Photo Collage Tool

This is an open source project from [DevProjects](http://www.codementor.io/projects). Feedback and questions are welcome!
Find the project requirements here: [Online photo collage tool](https://www.codementor.io/projects/web/online-photo-collage-tool-atx32mwend)

## Tech/framework used
Built with Python3 Flask RabbitMQ Celery Pillow Numpy

## Screenshot 
![screenshot](screenshot.png)

## Installation

Create a .env file.
```
$ vim .env

# Add the following lines.

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=asoethuasntehosentuhoethuothuonehu
CELERY_RESULT_BACKEND='rpc://'  # For RabbitMQ
CELERY_BROKER_URL='<your_rabbitmq_url>'
```

```
$ sudo apt install rabbitmq-server
```

## License
[GPL3](https://choosealicense.com/licenses/gpl-3.0/)
Most open source projects use the GPL3 license.
