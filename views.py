from flask import Blueprint, render_template, request, redirect
import scrape

views = Blueprint(__name__, "views")

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/search", methods=['GET', 'POST'])
def link():
    args = request.args
    title = args.get('title')
    location = args.get('location')
    url = f"http://127.0.0.1:5000/views/jobs?title={title}&location={location}" 

    return redirect(url)

@views.route("/jobs")
def jobs():
    args = request.args
    title = args.get('title')
    location = args.get('location')
    scrape.run(f"http://127.0.0.1:5000/views/jobs?title={title}&location={location}" )
#asynchronous vs. synchronous, should use cached
    return render_template("jobs.html", title=title, location=location)