from urllib import response
from flask import Flask, g
import json
from website.auth import auth
from website.auth import db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys
from website.models import User

sys.path.append("..")

# Test 1
def test_recommendations_with_different_city(app):
    client = app.test_client()

    data = json.dumps({"occasion": "birthday", "city": "Charlotte"})
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype
    }

    url = "/recommendations"
    with client as c:
        var = c.post(url, data=data, headers=headers)
        assert var.status_code == 403

# Test 2
def test_recommendations_with_different_occasion(app):
    client = app.test_client()

    data = json.dumps({"occasion": "anniversary", "city": "Raleigh"})
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype
    }

    url = "/recommendations"
    with client as c:
        var = c.post(url, data=data, headers=headers)
        assert var.status_code == 403

# Test 3: Test with invalid data
def test_recommendations_with_invalid_data(app):
    client = app.test_client()

    data = json.dumps({"event": "birthday"})  # Missing required keys
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype
    }

    url = "/recommendations"
    with client as c:
        var = c.post(url, data=data, headers=headers)
        assert var.status_code == 403  # Server denies access without incomplete headers

# Test 4: Test with missing headers
def test_recommendations_with_missing_headers(app):
    client = app.test_client()

    data = json.dumps({"occasion": "birthday", "city": "Raleigh"})
    url = "/recommendations"
    with client as c:
        var = c.post(url, data=data)  # No headers included
        assert var.status_code == 400  # 400 for incomplete data

# Test 5: Test with incorrect session user
def test_recommendations_with_incorrect_session(app):
    client = app.test_client()

    data = json.dumps({"occasion": "birthday", "city": "Raleigh"})
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype
    }

    url = "/recommendations"
    with client as c:
        with c.session_transaction() as sess:
            sess["userid"] = 999  # Assuming this user does not exist in the DB

        var = c.post(url, data=data, headers=headers)
        assert var.status_code == 500 # internal server error for not existing user