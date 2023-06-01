import json

from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        """ Initialize the StorageJson with a file path."""

        self.file_path = file_path

    def list_movies(self):
        """
        Retrieve the list of movies from the JSON file.

        Returns:
        - movies: The dictionary of movies loaded from the file.
        """
        with open(self.file_path, "r") as handle:
            movies = json.load(handle)
        return movies

    def add_movie(self, title, year, rating, img, imdb, country):
        """
        Add a new movie to the JSON file.

        Args:
        - title: The title of the movie.
        - year: The year of the movie.
        - rating: The rating of the movie.
        - img: The URL of the movie poster image.
        - imdb: The IMDb ID of the movie.
        - country: The country of the movie.

        """
        # Load the movies data from the file
        movies = self.list_movies()

        # Add the new movie to the dictionary
        movies[title] = {
            "rating": rating,
            "year": year,
            "img": img,
            "imdbID": imdb,
            "country": country
        }

        # Write the updated dictionary to the file
        with open(self.file_path, "w") as handle:
            json.dump(movies, handle)

    def delete_movie(self, title):
        """
        Delete a movie from the JSON file."""
        # Load the movies data from the file
        movies = self.list_movies()

        del movies[title]

        # Write the updated dictionary to the file
        with open(self.file_path, "w") as handle:
            json.dump(movies, handle)

    def update_movie(self, title, note):
        """
        Update the note of a movie in the JSON file.

        Args:
        - title: The title of the movie to update.
        - note: The new note for the movie.

        """
        # Load the movies data from the file
        movies = self.list_movies()

        movies[title]["note"] = note

        # Write the updated dictionary to the file
        with open(self.file_path, "w") as handle:
            json.dump(movies, handle)
