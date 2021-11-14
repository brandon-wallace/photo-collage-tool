'''
tests/test_routes.py
'''

import pytest
from flask import session
from application import create_app
from application.main.routes import rename_image_file


app = create_app()


@pytest.fixture()
def client():
    '''Client for testing routes'''

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['uploads'] = ['pic1.png', 'pic2.png']
            session['collage'] = 'collage_20211111-152527.106555.png'
        yield client


def test_index(client):
    '''Test index route for 200 status and text'''

    response = client.get('/')
    assert b'Upload Images' in response.data
    assert response.status_code == 200


def test_workspace(client):
    '''Test workspace route for 200 status and text'''

    response = client.get('/workspace')
    assert session['uploads'] == ['pic1.png', 'pic2.png']
    assert b'GENERATE COLLAGE' in response.data
    assert response.status_code == 200


def test_result(client):
    '''Test result route for 200 status and session'''

    response = client.get('/result')
    assert session['collage'] == 'collage_20211111-152527.106555.png'
    assert response.status_code == 200


def test_page_not_found(client):
    '''Test non existent routes for 404 status'''

    response = client.get('/asdf')
    assert response.status_code == 404


def test_rename_image_file():
    '''Test renaming of files for length and extension'''

    assert len(rename_image_file('example.jpg')) == 20
    assert rename_image_file('example.jpg')[-3:] == 'jpg'
