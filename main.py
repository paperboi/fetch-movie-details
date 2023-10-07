import requests
import os

from dotenv import load_dotenv

load_dotenv()

tmdb_api_key = os.environ['TMDB_KEY']

# Function to get the redirected URL of a given URL
def get_redirected_url(movie_id):
  url = f"https://letterboxd.com/tmdb/{movie_id}"
  try:
    response = requests.head(url, allow_redirects=True)
    return response.url
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    return None

# 
def fetch_movie_details(tmdb_api_key, film_name, year_of_release):
  # Search for the movie on TMDB using film name and year of release
  search_endpoint = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&language=en-US&query={film_name}&year={year_of_release}"
  search_response = requests.get(search_endpoint)

  if search_response.status_code == 200:
    search_data = search_response.json()
    if search_data['total_results'] == 0:
      return {
        'error': f"No results found for film: {film_name} ({year_of_release})"
      }

    # Get the movie ID of the first result
    movie_id = search_data['results'][0]['id']

    # Make API request to fetch movie details
    movie_endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
    movie_response = requests.get(movie_endpoint)

    if movie_response.status_code == 200:
      movie_data = movie_response.json()
      

      # Extract relevant details
      title = movie_data['title']
      tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}"
      lb_url = get_redirected_url(movie_id)
      imdb_url = f"https://www.imdb.com/title/{movie_data['imdb_id']}/"
      overview = movie_data['overview']
      poster_url = f"https://image.tmdb.org/t/p/original/{movie_data['poster_path']}"
      director = ''
      language = ''
      duration = ''

      # Fetch genre details
      genres = movie_data['genres']
      genre_names = [genre['name'] for genre in genres]
      genre_list = ', '.join(genre_names)

      # Fetch production countries
      countries_list = []
      for country in movie_data['production_countries']:
        countries_list.append(country['name'])
      countries_list = ', '.join(countries_list)

      # Fetch additional details (director, language, duration) if available
      credits_endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={tmdb_api_key}&language=en-US"
      credits_response = requests.get(credits_endpoint)

      if credits_response.status_code == 200:
        credits_data = credits_response.json()

        # Fetch director
        directors = credits_data['crew']
        for crew_member in directors:
          if crew_member['job'] == 'Director':
            director = crew_member['name']
            break

        # Fetch language
        languages = movie_data['spoken_languages']
        if languages:
          language = ', '.join([lang['english_name'] for lang in languages])

        # Fetch duration
        duration = f"{movie_data['runtime']} minutes"

      # Prepare the result dictionary
      result = {
        'title': title,
        'year_of_release': year_of_release,
        'director': director,
        'countries': countries_list,
        'language': language,
        'duration': duration,
        'genres': genre_list,
        'overview': overview,
        'poster_url': poster_url,
        'tmdb_url': tmdb_url,
        'lb_url': lb_url,
        'imdb_url': imdb_url,
      }

      return result
    else:
      return {
        'error':
        f"Error occurred while fetching movie details for film: {film_name} ({year_of_release})"
      }
  else:
    return {
      'error':
      f"Error occurred while searching for film: {film_name} ({year_of_release})"
    }


# Read film names and years of release from a text file
films_file = open('films.txt', 'r')
films = [line.strip().split(',') for line in films_file]
films_file.close()

# Perform movie details fetch for each film
results = []
for film in films:
  film_name = film[0]
  year_of_release = film[1].replace(" ", "")
  result = fetch_movie_details(tmdb_api_key, film_name, year_of_release)
  results.append(result)
# Write results to the output file
with open('results.txt', 'w') as output_file:
  for result in results:
    if 'error' in result:
      output_file.write(f"Error: {result['error']}\n\n")
    else:
      output_file.write(f"Title: {result['title']}\n")
      output_file.write(f"Year of Release: {result['year_of_release']}\n")
      output_file.write(f"Director: {result['director']}\n")
      output_file.write(f"Countries: {result['countries']}\n")
      output_file.write(f"Language: {result['language']}\n")
      output_file.write(f"Duration: {result['duration']}\n")
      output_file.write(f"Genres: {result['genres']}\n")
      output_file.write(f"Overview: {result['overview']}\n")
      output_file.write(f"TMDB URL: {result['tmdb_url']}\n")
      output_file.write(f"LB URL: {result['lb_url']}\n")
      output_file.write(f"IMDB URL: {result['imdb_url']}\n")
      output_file.write(f"Poster URL: {result['poster_url']}\n")
      output_file.write("\n")

# Print the results to the console
for result in results:
  if 'error' in result:
    print(f"✕ Error: {result['error']}")
  else:
    print(f"✓ {result['title']} ({result['year_of_release']})")
