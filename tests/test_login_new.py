from flask import Flask, g
import json
from website.auth import auth
from website.auth import db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys

sys.path.append("..")


## Test login page


def test_login_get_new(app):
    client = app.test_client()
    url = "/login"

    response = client.get(url)
    print(response.get_data())
    assert response.status_code == 200

def test_login_post_new(app):
    client = app.test_client()
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # This user is not present in the db
    data = {"email": "test@gmail.com",
            "password": "password123"}
    url = "/login"

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200


def test_login_check_positive_case(app):
    client = app.test_client()
    url = "/login"
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    data = {
        "email": "test@gmail.com",
        "password": "password123",
    }

    response = client.post(url, data=data, headers=headers)
    assert response.status_code, 200

def test_login_check_negative_case(app):
    client = app.test_client()
    url = "/login"
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # Incorrect password
    data = {"email": "test@gmail.com", "password": "wrongpassword"}
    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200  # Assuming incorrect login returns 401


def test_login_post_invalid_email(app):
    client = app.test_client()
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # Invalid email format
    data = {"email": "testgmail.com", "password": "password123"}
    url = "/login"

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200 













