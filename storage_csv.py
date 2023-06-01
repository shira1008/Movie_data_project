from istorage import IStorage
import csv


class StorageCsv(IStorage):
    def __init__(self, file_path):
        """
        Initialize the StorageCsv object.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Retrieve the list of movies from the CSV file.

        Returns:
            dict: A dictionary representing the movies, where the keys are movie titles
                  and the values are dictionaries containing movie information.
                  Each movie dictionary contains the following keys: 'rating', 'year',
                  'img', 'imdbID', 'note', and 'country'.
        """

        # creating a dictionary
        movies = {}
        with open(self.file_path, "r") as handle:
            file_reader = csv.DictReader(handle)
            for row in file_reader:
                movie_title = row['title']
                # dictionary of dictionaries
                movie_data = {
                    'rating': float(row['rating']),
                    'year': row['year'],
                    'img': row['img'],
                    'imdbID': row['imdbID'],
                    'country': row['country']
                }
                # check if note is exists, if not, dont add the note
                note = row.get('note')
                if note:
                    movie_data['note'] = note

                # add to the empty dict
                movies[movie_title] = movie_data
        return movies

    def _write_movies_to_csv(self, movies):
        """
        Write the movies data to the CSV file.

        Args:
            movies (dict): A dictionary representing the movies to be written to the CSV file.
                           The keys are movie titles and the values are dictionaries containing
                           movie information.
        """

        with open(self.file_path, "w", newline='') as csv_file:
            fieldnames = ['title', 'rating', 'year', 'img', 'imdbID', 'note', 'country']

            # DictWriter - allows writing dictionaries as rows in a CSV file, fieldnames is the headers
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            # each movie is represented as a row in the CSV file,
            # with the movie's attributes corresponding to the field names in the header row.

            for movie_title, movie_data in movies.items():
                movie_data['title'] = movie_title
                writer.writerow(movie_data)

    def add_movie(self, title, year, rating, img, imdb, country):
        """
        Add a new movie to the CSV file.
        """

        # Load the movies data from the file
        movies = self.list_movies()

        # Add the new movie to the dictionary
        movies[title] = {
            "title": title,
            "rating": rating,
            "year": year,
            "img": img,
            "imdbID": imdb,
            "country": country
        }

        # Write the updated movie data to the csv file
        self._write_movies_to_csv(movies)

    def delete_movie(self, title):
        """
        Delete a movie from the CSV file.
        """

        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._write_movies_to_csv(movies)

    def update_movie(self, title, note):
        """
        Update the note of a movie in the CSV file.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['note'] = note
            # Write the updated dictionary to the file
            self._write_movies_to_csv(movies)
