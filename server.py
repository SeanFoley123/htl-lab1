"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""

import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

courses = pd.read_csv('./data/olin-courses-16-17.csv')
courses = courses.fillna("Not available")		#Information not in the csv

courses["course_contact"] = courses["course_contact"].apply(lambda contact: "; ".join([" ".join(name.split(", ")[::-1]) for name in str(contact).split("; ")]))

# 
text = ''
previous = ''

@app.route('/health')
def health():
    return 'ok'

@app.route('/<course_area>')
def home_page(course_area):
	global text
	global previous
	if previous == course_area:		#If you click a button twice, clears the search
		text = ''
		previous = ''
	else:
		previous = course_area		#Record current filter
	bool_vec = courses["course_area"].str.contains(text, False).fillna(False)
	for thing in courses.columns:
		bool_vec = courses[thing].str.contains(text, False).fillna(False) | bool_vec

	if course_area == 'ALL':
		courses_active = courses[bool_vec]
	else:
		courses_active = courses[(courses.course_area == course_area) & bool_vec]
	return render_template('index.html', areas=set(courses.course_area), courses=courses_active.iterrows(), current=course_area, search=text)

@app.route('/<course_area>', methods = ['POST'])
def search_term(course_area):
	global text
	global previous
	text = request.form['text']
	previous = ''				#Prevent a reset 
	return home_page(course_area)


@app.route('/')
def redir():
	return redirect("/ALL")

if __name__ == '__main__':
    app.run(debug=True)
debug
port = int(os.environ.get('PORT', 5000)))
app.run(host='0.0.0.0', debug=True, port=port)