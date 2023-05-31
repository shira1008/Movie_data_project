from movie_app import MovieApp
# storage:
from storage_json import StorageJson
from storage_csv import StorageCsv
# Command Line Arguments:
import sys
import json
import os


def main():
    # Command Line Arguments:
    file_name = "storage/" + sys.argv[1]

    if sys.argv[1].split(".")[1] == 'json':
        # JSON storage
        if not os.path.exists(file_name):
            # i dont want an empty file to beggin with
            data = {
                "Mulan": {
                    "rating": 7.6,
                    "year": "1998",
                    "img": "https://m.media-amazon.com/images/M/MV5BODkxNGQ1NWYtNzg0Ny00Yjg3LThmZTItMjE2YjhmZTQ0ODY5XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
                    "imdbID": "tt0120762",
                    "country": "US"
                }
            }
            with open(file_name, "w") as handle:
                json.dump(data, handle)

        storage = StorageJson(file_name)
        movies = storage.list_movies()
        movie_app = MovieApp(storage)
        movie_app.run()

    elif sys.argv[1].split(".")[1] == 'csv':
        # CSV storage
        if not os.path.exists(file_name):
            with open(file_name, "w") as handle:
                pass

        storage = StorageCsv(file_name)

        # Add the movie if the file was newly created
        if not storage.list_movies():
            storage.add_movie(
                "Mulan",
                "1998",
                7.6,
                "https://m.media-amazon.com/images/M/MV5BODkxNGQ1NWYtNzg0Ny00Yjg3LThmZTItMjE2YjhmZTQ0ODY5XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
                "tt0120762",
                "US"
            )

        movie_app = MovieApp(storage)
        movie_app.run()


if __name__ == "__main__":
    main()
