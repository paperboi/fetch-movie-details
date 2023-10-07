# Movie Details Fetcher

This project is a movie details fetcher that utilizes the [themoviedb.org](https://www.themoviedb.org/) API to retrieve information about movies based on the film title and year of release. It provides a simple and convenient way to gather comprehensive details about movies, including the title, release date, overview, poster URL, director, language, and duration.

By utilizing the themoviedb.org API, this project enables users to quickly and easily access comprehensive movie details based on the film title and year of release. Whether for personal use or as part of a larger movie-related application, this project provides a valuable resource for movie enthusiasts, researchers, and developers alike.

## How to Use

1. **API Keys Setup**

   To use this project, you need to obtain API keys for both themoviedb.org. You can sign up and obtain API keys from [themoviedb.org API](https://developer.themoviedb.org/docs). Once you have obtained the API keys, make sure to set them as environment variables:

   ```shell
   export TMDB_KEY=YOUR_TMDB_API_KEY
   ```

2. **Film List Setup**

   Create a text file named `films.txt` containing the list of films you want to fetch details for. Each line should contain the film title followed by a comma and the year of release, like this:

   ```
   The Shawshank Redemption,1994
   Inception,2010
   ```

3. **Run the Script**

   Execute the script using Python:

   ```shell
   python script.py
   ```

4. **Output**

   The script will fetch movie details for each film listed in `films.txt` and generate a `results.txt` file with the results. Each film's details will be written in the following format:

   ```
    Title: The Shawshank Redemption
    Year of Release: 1994
    Director: Frank Darabont
    Countries: United States of America
    Language: English
    Duration: 142 minutes
    Genres: Drama, Crime
    Overview: Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden. During his long stretch in prison, Dufresne comes to be admired by the other inmates -- including an older prisoner named Red -- for his integrity and unquenchable sense of hope.
    TMDB URL: https://www.themoviedb.org/movie/278
    LB URL: https://letterboxd.com/film/the-shawshank-redemption/
    IMDB URL: https://www.imdb.com/title/tt0111161/
    Poster URL: https://image.tmdb.org/t/p/original//lyQBXzOQSuE59IsHyhrp0qIiPAz.jpg
   ```

   If an error occurs during the fetch process, it will be logged as follows:

   ```
   Film: Some Film (Year) ✕
   Error: [Error message]
   ```

## Dependencies

This project relies on the following Python libraries, which you can install using `pip`:

- `requests`: To make API requests.

You can install these dependencies by running:

```shell
pip install requests
```

## Credits

- [themoviedb.org API](https://www.themoviedb.org/documentation/api)

Feel free to use and modify this project for your movie-related needs.
