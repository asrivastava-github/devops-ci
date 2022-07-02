#! /usr/bin/env python3

from flask import Flask, render_template, request, flash, url_for, redirect, session, send_from_directory

blog = Flask(__name__)
blog.secret_key = 'super secret key'
blog.debug = False


@blog.route('/home')
def homepage():
    return render_template("home.html")


@blog.route('/blogs')
def blogs():
    return render_template("blogs.html")


@blog.route('/cloudsolutions')
def cloudsolutions():
    return render_template("cloudsolutions.html")


if __name__ == "__main__":
    blog.debug = True
    blog.run(host='0.0.0.0')         #Mandetory to provide host as 0.0.0.0
