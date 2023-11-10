from app import app
from flask import render_template, request
from app.movie_details import fetch_movie_details  # Import the function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def get_movie_details():
    
    film_name = request.form['film_name']
    year_of_release = request.form['year_of_release']
    
    result = fetch_movie_details(film_name, year_of_release)
    
    if 'error' in result:
        result = [result]
    else:
        result = [result]

    return render_template('results.html', results=result)
