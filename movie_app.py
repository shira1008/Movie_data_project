import json
import random
import statistics

import matplotlib.pyplot as plt
import pycountry
import requests
from colored import fg, attr
from fuzzywuzzy import process
from config import API_KEY


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def fetch_data(self, title):
        url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # raise an exception for a bad status code
            data = response.json()
            return data
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error: {e}")

    def create_website(self, data_with_html_structure):
        TEMPLATE_FILE_NAME = "_static/index_template.html"
        NEW_FILE_NAME = "_static/index.html"

        with open(TEMPLATE_FILE_NAME, "r") as handle:
            template = handle.read()

        template = template.replace("__TEMPLATE_TITLE__", "My Movie App")
        template = template.replace("__TEMPLATE_MOVIE_GRID__", data_with_html_structure)

        with open(NEW_FILE_NAME, "w") as handle:
            handle.write(template)
            print(f"{fg(2)}Website was generated successfully.{attr(0)}")

    def html_structure(self):
        movies = self._storage.list_movies()
        my_html_structure = ""
        for title, data in movies.items():
            imdb_link = f'https://www.imdb.com/title/{data["imdbID"]}/'
            note_html = f"<p class='movie-note'>{data['note']}</p>" if 'note' in data else ""
            movie_html = f""" 
            <li class="movie-grid-item">
            <div class="movie">
            <a href={imdb_link} target="_blank" ><img class="movie-poster" src="{data['img']}" alt="{title}"/></a>
            <div class="movie-info">
                <h2 class="movie-title">{title} <div class="rate_flag"><span class="movie-rating"><i class="fa fa-star"></i> {data['rating']}</span> <img class="flag" src="https://flagsapi.com/{data['country']}/shiny/64.png" alt=f"{data['country']}"></div></h2>
                <p class="movie-year">Year: {data['year']} </p>
                {note_html}
            </div>
            </div>
            </li>

            """
            my_html_structure += movie_html
        return my_html_structure

    def list_movies(self):
        """print the movies"""
        movies = self._storage.list_movies()
        print(" ")
        print(f"{fg(85)}{len(movies)} movies in total: {attr(0)}")
        print("  ")
        for key, value in movies.items():
            print(f"{fg(87)}{key}({value['year']}), its rated: {value['rating']}{attr(0)}")

    def add_movie(self):
        """adding new movie+rating"""
        movies = self._storage.list_movies()
        user_input_movie_name = input("Enter new movie name: ").capitalize()
        if user_input_movie_name not in movies:
            try:
                movie_data = self.fetch_data(user_input_movie_name)
                fetch_movie_rating = float(movie_data["imdbRating"])
                fetch_movie_year = movie_data['Year']
                fetch_movie_img = movie_data['Poster']
                fetch_movie_imdb = movie_data['imdbID']
                fetch_movie_country = movie_data['Country'].split(",")[0]
                country_obj = pycountry.countries.get(name=fetch_movie_country)
                if country_obj:
                    fetch_movie_country = country_obj.alpha_2
                else:
                    fetch_movie_country = "unknown"
                movies[user_input_movie_name] = {"rating": fetch_movie_rating, "year": fetch_movie_year,
                                                 "img": fetch_movie_img, "imdbID": fetch_movie_imdb,
                                                 "country": fetch_movie_country}
                # Save the data to the storage
                self._storage.add_movie(user_input_movie_name, fetch_movie_year, fetch_movie_rating, fetch_movie_img,
                                        fetch_movie_imdb, fetch_movie_country)
                print(f"{fg(2)}The movie {user_input_movie_name} was successfully added!{attr(0)}")
            except Exception:
                print(f"{fg(1)}No movie name: {user_input_movie_name}{attr(0)}")
        else:
            print(f"{fg(1)}The movie {user_input_movie_name} already exists!{attr(0)}")

    def delete_movie(self):
        """delete movie"""
        movies = self._storage.list_movies()
        user_input_movie_name = input("Enter movie name to delete: ").capitalize()
        if user_input_movie_name not in movies:
            print(f"{fg(1)}Movie {user_input_movie_name} doesn't exist!{attr(0)}")
        else:
            del movies[user_input_movie_name]
            # Save the data to the storage
            self._storage.delete_movie(user_input_movie_name)
            print(f"{fg(2)}The movie {user_input_movie_name} was successfully deleted!{attr(0)}")

    def update_movie(self):
        """Add movie note"""
        user_input_movie_name = input("Enter movie name to update: ").capitalize()
        movies = self._storage.list_movies()

        if user_input_movie_name not in movies:
            print(f"{fg(1)}The movie {user_input_movie_name} doesn't exist!{attr(0)}")
        else:
            user_input_movie_update = input("Enter movie note: ")
            movies[user_input_movie_name]["note"] = user_input_movie_update
            # Save the data to the storage
            self._storage.update_movie(user_input_movie_name, user_input_movie_update)
            print(f"{fg(2)}The movie {user_input_movie_name} was successfully updated.{attr(0)}")

    def stats(self):
        """Show statistics"""
        movies = self._storage.list_movies()  # Retrieve movie data from storage

        ratings = [movie["rating"] for movie in movies.values()]
        average_rating = sum(ratings) / len(ratings)
        median_rating = statistics.median(ratings)
        best_rating = max(ratings)
        worst_rating = min(ratings)

        movie_name_best = None
        movie_name_worst = None

        for movie_name, movie_data in movies.items():
            if movie_data["rating"] == best_rating:
                movie_name_best = movie_name
            if movie_data["rating"] == worst_rating:
                movie_name_worst = movie_name

        print("")
        print(f"{fg(221)}Average rating: {average_rating}")
        print(f"Median rating: {median_rating}")
        print(f"The best movie: {movie_name_best}, {best_rating}")
        print(f"The worst movie: {movie_name_worst}, {worst_rating}{attr(0)}")

    def random_movie(self):
        """pick a random movie for the user"""
        movies = self._storage.list_movies()
        random_key = random.choice(list(movies.keys()))
        random_value_matched = movies[random_key]
        print("")
        print(
            f"{fg(117)}Your movie for tonight: {random_key}({random_value_matched['year']}), it's rated {random_value_matched['rating']}{attr(0)}")

    def search_movie(self):
        movies = self._storage.list_movies()
        """search a movie by typing part of the name, case insensitive"""
        user_input_movie_name = input("Enter part of movie name: ").lower()
        exact_match_found = False

        # Look for exact matches - when the string is in one of the keys
        for key, value in movies.items():
            if user_input_movie_name in key.lower():
                print(f"{fg(151)}{key}({value['year']}), its rated: {value['rating']}{attr(0)}")
                exact_match_found = True

        # If not, suggest similar movies
        if not exact_match_found:
            matches = process.extract(user_input_movie_name, movies.keys(), limit=3)
            for match, score in matches:
                if score >= 70:
                    print(f"{fg(151)}Did you mean '{match}'?{attr(0)}")
                    new_input = input("(Y/N): ")
                    if new_input.lower() == "y":
                        print(
                            f"{fg(151)}{match}({movies[match]['year']}), its rated: {movies[match]['rating']}{attr(0)}")
                        return ""

    def movies_sorted_by_rating(self):
        """print movies by rating in descending order"""
        movies = self._storage.list_movies()
        # sort the dictionary by the value - reverse
        sorted_movies_rating_dictionary = dict(sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True))
        print("")
        for key, value in sorted_movies_rating_dictionary.items():
            print(f"{fg(80)}{key}({value['year']}), its rated: {value['rating']}{attr(0)}")

    # BONUS
    def create_Rating_Histogram(self):
        movies = self._storage.list_movies()
        user_format = input("Enter a format and a file name (for example histo.png): ")
        data = [movie["rating"] for movie in movies.values()]
        # 10 bins cause movies rating is 1-10.
        plt.hist(data, bins=10, color='magenta', alpha=0.5)
        plt.xlabel('Movie Rating')
        plt.ylabel('Frequency')
        plt.title('Histogram of Movies Ratings')
        plt.savefig(user_format)
        plt.show()

    def run(self):
        print(f'{fg("medium_purple_2b")}{attr("bold")}********** My Movies Database **********{attr(0)}')
        enter_input = True
        while enter_input:
            menu_options = """
Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate website
10. Create Rating Histogram
    """

            print(f'{fg(225)}{menu_options}{attr(0)}')

            # to handle input that is not a number
            try:
                user_input = int(input("Enter choice(0-10): "))
            except ValueError:
                print(f"{fg(1)}Invalid input, try again{attr(0)}")
                continue

            # for numbers > 9 or numbers < 0
            while user_input not in range(11):
                print(f"{fg(1)}Invalid input, try again{attr(0)}")
                user_input = int(input("Enter choice(0-10): "))

            # for quit:
            if user_input == 0:
                print(f'{fg(3)}Bye! {attr(0)}')
                break
            else:
                if user_input == 1:
                    self.list_movies()
                if user_input == 2:
                    self.add_movie()
                if user_input == 3:
                    self.delete_movie()
                if user_input == 4:
                    self.update_movie()
                if user_input == 5:
                    self.stats()
                if user_input == 6:
                    self.random_movie()
                if user_input == 7:
                    self.search_movie()
                if user_input == 8:
                    self.movies_sorted_by_rating()
                if user_input == 9:
                    self.create_website(self.html_structure())
                if user_input == 10:
                    self.create_Rating_Histogram()

            print(" ")
            enter_input = input("Press enter to continue ")
            if enter_input == "":
                enter_input = True
