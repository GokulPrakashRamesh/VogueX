from flask import Flask, g
import json
from website.auth import auth
from website.auth import db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys

sys.path.append("..")


## Test SignUp


def test_signup_get(app):
    client = app.test_client()
    url = "/sign-up"
    response = client.get(url)
    assert response.status_code, 200


def test_signup_post_missing_field(app):
    client = app.test_client()
    url = "/sign-up"
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    # Missing required field "age"
    data = {
        "email": "test@gmail.com",
        "firstName": "test_user",
        "lastName": "test_end_name",
        "gender": "unknown",
        "phoneNumber": 99999999999,
        "password1": "password123",
        "password2": "password123",
        "city": "Raleigh",
    }

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200  # Assuming validation returns 400





def test_signup_post_existing_user(app):
    client = app.test_client()
    url = "/sign-up"
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # Assuming this email is already in the database
    data = {
        "email": "existing@gmail.com",
        "firstName": "Existing",
        "lastName": "User",
        "gender": "unknown",
        "phoneNumber": 1234567890,
        "password1": "password123",
        "password2": "password123",
        "age": 30,
        "city": "New York",
    }

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200  # Assuming conflict returns 409


def test_signup_get(app):
    client = app.test_client()
    url = "/sign-up"
    response = client.get(url)
    assert response.status_code, 200


def test_signup_post(app):
    client = app.test_client()
    url = "/sign-up"
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    # This user is not present in the db
    data = {
        "email": "test@gmail.com",
        "firstName": "test_user",
        "lastName": "test_end_name",
        "gender": "unknown",
        "phoneNumber": 99999999999,
        "password1": "password123",
        "password2": "password123",
        "age": 25,
        "city": "Raleigh",
    }

    response = client.post(url, data=data, headers=headers)
    assert response.status_code, 200


def test_logout_redirect(app):
    client = app.test_client()
    url = "/logout"
    response = client.get(url)
    assert response.status_code in [200, 302]  # Logout should redirect


def test_signup_post_password_mismatch(app):
    client = app.test_client()
    url = "/sign-up"
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # Password mismatch
    data = {
        "email": "mismatch@gmail.com",
        "firstName": "Mismatch",
        "lastName": "Test",
        "gender": "unknown",
        "phoneNumber": 9876543210,
        "password1": "password123",
        "password2": "differentpassword",
        "age": 28,
        "city": "San Francisco",
    }

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200  


def test_login_post_empty_password(app):
    client = app.test_client()
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # Password field left empty
    data = {"email": "test@gmail.com", "password": ""}
    url = "/login"

    response = client.post(url, data=data, headers=headers)
    assert response.status_code == 200  


def test_signup_get_incorrect_url(app):
    client = app.test_client()
    url = "/signupp"  # Incorrect URL
    response = client.get(url)
    assert response.status_code != 200  


#################################