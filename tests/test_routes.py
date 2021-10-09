from application.main.routes import rename_image_file


def test_rename_image_file():

    assert len(rename_image_file('example.jpg')) == 20

    assert rename_image_file('example.jpg')[-3:] == 'jpg'
