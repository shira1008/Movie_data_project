from storage_json import StorageJson
from movie_app import MovieApp

from storage_csv import StorageCsv


def main():
    ##json storage:
    storage = StorageJson('storage/data.json')
    movies = storage.list_movies()
    movie_app = MovieApp(storage)
    movie_app.run()

    ###csv storage:
    # storage = StorageCsv('storage/movies.csv')
    # movie_app = MovieApp(storage)
    # movie_app.run()


if __name__ == "__main__":
  main()

