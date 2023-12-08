import requests
from config import Config

tmdb_api_key = Config.TMDB_KEY

# Function to convert mins to hours & minutes
def minutes_to_hours_minutes(minutes):
  if minutes < 0:
    raise ValueError("Input must be a non-negative number of minutes.")

  hours = minutes // 60  # Integer division to get the number of hours
  remaining_minutes = minutes % 60  # The remaining minutes after calculating hours

  return f"{hours}h {remaining_minutes}m"

# Function to get the redirected URL of a given URL
def get_redirected_url(movie_id):
  url = f"https://letterboxd.com/tmdb/{movie_id}"
  try:
    response = requests.head(url, allow_redirects=True)
    return response.url
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    return None

# Function to fetch the movie details
def fetch_movie_details(film_name, year_of_release):
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
      release_year = movie_data['release_date'][:4]
      tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}"
      lb_url = get_redirected_url(movie_id)
      imdb_url = f"https://www.imdb.com/title/{movie_data['imdb_id']}/"
      overview = movie_data['overview']
      poster_paths = ''
      director = ''
      language = ''
      runtime = ''

      # Fetch poster gallery
      images_endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={tmdb_api_key}"
      images_response = requests.get(images_endpoint)

      if images_response.status_code == 200:
          images_data = images_response.json()
          poster_paths = [f"https://image.tmdb.org/t/p/original{poster['file_path']}" for poster in images_data['posters']]
      else:
          poster_paths = [f"https://image.tmdb.org/t/p/original/{movie_data['poster_path']}"]
          
      # Fetch video
      videos_endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={tmdb_api_key}"
      videos_response = requests.get(videos_endpoint)
      
      if videos_response.status_code == 200:
        videos_data = videos_response.json()
        trailer_key = None
        if 'results' in videos_data and len(videos_data['results']) > 0:
          # Find the first video with type "Trailer"
          for video in videos_data['results']:
            if (video.get('type') == 'Trailer') and (video.get('site') == 'YouTube'):
              print(f"{video.get('type')}, {video.get('site')}")
              trailer_key = video.get('key')
              break
      
      # Fetch genre details
      genres = movie_data['genres']
      genre_names = [genre['name'] for genre in genres]
      genre_list = ', '.join(genre_names)

      # Fetch production countries
      countries_list = []
      for country in movie_data['production_countries']:
        countries_list.append(country['name'])
      countries_list = ', '.join(countries_list)

      # Fetch additional details (director, language, runtime) if available
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

        # Fetch runtime
        # runtime = f"{movie_data['runtime']} minutes"
        runtime = minutes_to_hours_minutes(movie_data['runtime'])

      # Prepare the result dictionary
      result = {
        'title': title,
        'year_of_release': release_year,
        'director': director,
        'countries': countries_list,
        'language': language,
        'runtime': runtime,
        'genres': genre_list,
        'overview': overview,
        'tmdb_url': tmdb_url,
        'lb_url': lb_url,
        'imdb_url': imdb_url,
        'poster_paths': poster_paths,
        'trailer_key': trailer_key
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