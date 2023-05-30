from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
      self.file_path = file_path


    def list_movies(self):
      with open(self.file_path, "r") as handle:
          movies = json.load(handle)
      return movies
          

    def add_movie(self, title, year, rating, img, imdb, country):
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
      # Load the movies data from the file
      movies = self.list_movies()

      del movies[title]

      # Write the updated dictionary to the file
      with open(self.file_path, "w") as handle:
          json.dump(movies, handle)
        

    def update_movie(self, title, note):
      # Load the movies data from the file
      movies = self.list_movies()

      movies[title]["note"] = note

      # Write the updated dictionary to the file
      with open(self.file_path, "w") as handle:
          json.dump(movies, handle)
        