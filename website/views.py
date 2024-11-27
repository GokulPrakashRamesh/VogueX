# VogueX
# Copyright (c) 2024 Group 84: Gokul Prakash Ramesh, Haricharan Bharathi, Raghunandan Ganesh Mante
# This project is licensed under the MIT License.
# #
# Governance Model:
# This project follows an open governance model, which includes a leadership team,
# contribution guidelines, a code of conduct, and a clear decision-making process.
# Contributions are welcome, and please see CONTRIBUTING.md for details.
from datetime import datetime, timedelta


from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)

from flask_login import login_required, current_user
from . import models
import json

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/cycle', methods=['GET', 'POST'])
def cycle_tracker():
    insights = None
    if request.method == 'POST':
        last_period = request.form.get('lastPeriod')
        cycle_length = int(request.form.get('cycleLength'))
        period_length = int(request.form.get('periodLength'))
        
        # Calculate Next Period and Fertile Window
        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')
        next_period = last_period_date + timedelta(days=cycle_length)
        fertile_start = next_period - timedelta(days=14)
        fertile_end = fertile_start + timedelta(days=5)
        
        # Generate recommendations
        recommendation = "Stay hydrated and maintain a healthy diet for better cycle management."
        
        insights = {
            'next_period': next_period.strftime('%Y-%m-%d'),
            'fertile_window': f"{fertile_start.strftime('%Y-%m-%d')} to {fertile_end.strftime('%Y-%m-%d')}",
            'recommendation': recommendation
        }

    return render_template('cycle.html', insights=insights)



@views.route("/procResult", methods=["POST"])
@login_required
def procResult():
    if request.method == "POST":
        linksData = request.json["resultLinks"]["links"]
        strLinks = ""
        for links in linksData:
            strLinks += links + " || "
        linksData = strLinks
        return redirect(url_for("views.results", user=current_user, data=linksData))


@views.route("/results")
@login_required
def results():
    image_paths = request.args.get("images", "").split(",")
    return render_template(
        "results.html", ldata=image_paths, user=current_user, enumerate=enumerate
    )


@views.route("/datasets/fashion-dataset/images/<path:filename>")
def serve_images(filename):
    return send_from_directory("datasets/fashion-dataset/images", filename)


# @views.route("/results", methods=["POST", "GET"])
# @login_required
# def results():
#     linksData = str(request.args.to_dict())[2:-2].split(" || ")
#     return render_template(
#         "results.html", user=current_user, ldata=linksData, enumerate=enumerate
#     )


@views.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    preferenceObject = models.Preference.query.filter_by(
        userid=int(current_user.id)
    ).first()
    if preferenceObject:
        prefData = json.loads(preferenceObject.preferences)
    else:
        preferenceObject = models.Preference(
            userid=int(current_user.id), preferences=""
        )
        prefData = {}

    return render_template("profile.html", user=current_user, prefData=prefData)
