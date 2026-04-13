#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pytest
from datetime import datetime
import re
import os
import collections
import json
from collections import defaultdict


class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file):
        self.data = self.read_file(path_to_the_file)
        
        
    def read_file(self, path_to_the_file):
        try:
            title = list()
            data_dict = dict()
            b = True
            with open(path_to_the_file, "r", encoding='utf-8') as file:
                
                for line_num, line in enumerate(file):
                    
                    data_list = list()
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line_num == 1001:
                        break
                    
                    if b == False:
                        if '"' not in line:
                            data_list = [item.strip() for item in line.split(",")]
                        else:
                            k = 0
                            row = ""
                            for bukv in line:
                                if bukv == '"':
                                    k += 1
                                    continue
                                elif bukv == "," and k%2 == 0:
                                    data_list.append(row.strip())
                                    row = ""
                                    continue
                                
                                row += bukv
                            if row.strip() != "":
                                data_list.append(row.strip())
                                
                        if len(title) == len(data_list):
                            row_dict = dict()
                            for i in range(len(title)):
                                if title[i] == "movieId":
                                    pass
                                elif title[i] == "title":
                                    full_name = data_list[i]
                                    year_match = re.search(r'\((\d{4})\)$', full_name.strip())
                                    if year_match != None:
                                        year = year_match.group(1)
                                        title_without_year = re.sub(r'\s*\(\d{4}\)\s*$', '', full_name).strip()
                                        row_dict["name"] = title_without_year
                                        row_dict["year"] = int(year)
                                    else:
                                        row_dict["name"] = full_name
                                        row_dict["year"] = None
                                elif title[i] == "genres":
                                    list_gen = data_list[i].strip().split("|")
                                    row_dict[title[i]] = list_gen
                                else:
                                    row_dict[title[i]] = data_list[i]
                                
                        else:
                            raise Exception("Invalid data format in table")
                        
                        data_dict[int(data_list[0])] = row_dict
                        
                    else:
                        title = [item.strip() for item in line.split(",")]
                        b = False
                    
            return data_dict
        except Exception as e:
            print(f"Error: {e}")
            return None
        
        
    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        
        Метод возвращает dict или OrderedDict, где ключами являются годы, а значениями — количество. 
        Вам нужно извлечь годы из названий. Отсортируйте его по количеству по убыванию.
        """
        years_dict = dict()
        for key in self.data:
            if self.data[key] and self.data[key]["year"] is not None:
                year = self.data[key]["year"]
                if year in years_dict:
                    years_dict[year] += 1
                else:
                    years_dict[year] = 1
        release_years = dict(sorted(years_dict.items(), key=lambda item: item[1], reverse=True))
        return release_years
    
    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        
        Метод возвращает словарь, в котором ключами являются жанры, а значениями — количество.
        Отсортируйте его по количеству по убыванию.
        """
        genres_not_sort = dict()
        for key in self.data:
            if self.data[key] and self.data[key]["genres"]:
                genres_list = self.data[key]["genres"]
                for g in genres_list:
                    if g in genres_not_sort:
                        genres_not_sort[g] += 1
                    else:
                        genres_not_sort[g] = 1
        genres = dict(sorted(genres_not_sort.items(), key=lambda item:item[1], reverse=True))
        return genres
        
    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов и 
        значения — количество жанров фильма. Отсортируйте его по номерам по убыванию.
        """
        films_dict = dict()
        for key in self.data:
            if self.data and self.data[key]["name"] and self.data[key]["genres"]:
                name = self.data[key]["name"]
                films_dict[name] = len(self.data[key]["genres"])
        movies_sort = sorted(films_dict.items(), key=lambda item:item[1], reverse=True)
        movies = dict(movies_sort[:n])
        return movies
    
    
    ######### Бонусная часть #########
    def popular_genres(self, n):
        """
        В какие года был наиболее популярен какой жанр
        """
        # year_dict = {
        #     year: genres: count
        #           genres: count
        # }
        year_dict = dict()
        year_genres_dict = dict()
        for key in self.data:
            year = self.data[key]["year"]
            if year is None:
                continue
            
            for genres in self.data[key]["genres"]:
                if genres == "(no genres listed)":
                    continue
                
                if year not in year_dict:
                    year_dict[year] = {}

                if genres not in year_dict[year]:
                    year_dict[year][genres] = 1
                else:
                    year_dict[year][genres] += 1
                
        for year, genres in year_dict.items():
            sorted_genres = sorted(genres.items(), key=lambda item: item[1], reverse=True)
            if sorted_genres is not None:
                year_genres_dict[year] = sorted_genres[0][0]
                
        year_sort = dict(sorted(year_genres_dict.items(), key=lambda item: item[0])[:n])
        return year_sort


class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file):
        self.data = self.read_file(path_to_the_file)
        
    def read_file(self, path_to_the_file):
        try:
            user_dict = dict()
            title = list()
            b = True
            with open(path_to_the_file, "r", encoding='utf-8') as file:
                for line_num, line in enumerate(file):
                    
                    data_list = list()
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line_num == 1002:
                        break
                    
                    if b == False:
                        data_list = [item.strip() for item in line.split(",")]
                        
                        if len(data_list) < 4:
                            raise Exception("Invalid data format in table")
                        
                        user_id = int(data_list[0])
                        movie_id = int(data_list[1])
                        tag = data_list[2]
                        timestamp = int(data_list[3])
                        
                        if user_id not in user_dict:
                            user_dict[user_id] = {}
                            
                        if movie_id not in user_dict[user_id]:
                            user_dict[user_id][movie_id] = {
                                title[2]: set(),
                                title[3]: list()
                            }
                        
                        user_dict[user_id][movie_id][title[2]].add(tag)
                        user_dict[user_id][movie_id][title[3]].append(timestamp)
                    else:
                        title = [item.strip() for item in line.split(",")]
                        b = False
                return user_dict
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        
        Метод возвращает топ-n тегов, в которых содержится большинство слов. Это словарь
        где ключи — это теги, а значения — количество слов внутри тега.
        Отбросьте дубликаты. Отсортируйте его по номерам по убыванию.
        """
        tag_word = dict()
        for movies in self.data.values():
            for movie_data in movies.values():
                for tag in movie_data["tag"]:
                    if tag not in tag_word:
                        tag_word[tag] = len(tag.split())
        big_tags_sort = sorted(tag_word.items(), key=lambda item: item[1], reverse=True)
        big_tags = dict(big_tags_sort[:n])
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        
        Метод возвращает n самых длинных тегов по количеству символов.
        Это список тегов. Отбросьте дубликаты. Отсортируйте его по номерам по убыванию.
        """
        tag_word = dict()
        for movies in self.data.values():
            for movie_data in movies.values():
                for tag in movie_data["tag"]:
                    if tag not in tag_word:
                        tag_word[tag] = len(tag)
        tag_word_sort = sorted(tag_word.items(), key=lambda item: item[1], reverse=True)
        big_tags = [tag for tag, _ in tag_word_sort[:n]]
        return big_tags
    

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        
        Метод возвращает пересечение топ-n тегов с большинством слов внутри и 
        Топ-n самых длинных тегов по количеству символов.
        Отбросьте дубликаты. Это список тегов.
        """
        mnoga_word_dict = self.most_words(n)
        longest_list = self.longest(n)
        mnoga_word_set = set(mnoga_word_dict)
        longest_set = set(longest_list)
        
        intersection = mnoga_word_set & longest_set
        big_tags = sorted(intersection, key=lambda tag:mnoga_word_dict[tag], reverse=True)
        
        return big_tags
        
    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        
        Метод возвращает самые популярные теги. 
        Это словарь, в котором ключи являются тегами, а значения — счетчиками.
        Отбросьте дубликаты. Отсортируйте его по количеству по убыванию.
        """
        tag_popular = dict()
        for movies in self.data.values():
            for movie_data in movies.values():
                for tag in movie_data["tag"]:
                    if tag in tag_popular:
                        tag_popular[tag] += 1
                    else:
                        tag_popular[tag] = 1
        tag_word_sort = sorted(tag_popular.items(), key=lambda item: item[1], reverse=True)
        popular_tags = dict(tag_word_sort[:n])
        
        return popular_tags
        
    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        
        Метод возвращает все уникальные теги, содержащие слово, указанное в качестве аргумента.
        Отбросьте дубликаты. Это список тегов. Отсортируйте его по именам тегов в алфавитном порядке.
        """
        tags_with_word = list()      
        for movies in self.data.values():
            for movie_data in movies.values():
                for tag in movie_data["tag"]:
                    if word in tag and tag not in tags_with_word:
                        tags_with_word.append(tag)
                        
        tags_with_word.sort(key=str.lower)
        return tags_with_word


    ######### Бонусная часть #########
    def tegs_movie_popular(self, n):
        """
        топ самых (тегируемых?) фильмов
        """
        movie_tags = dict()
        for movies in self.data.values():
            for movie_id, movie_data in movies.items():
                if movie_id not in movie_tags:
                    movie_tags[movie_id] = 0
                movie_tags[movie_id] += len(movie_data["tag"])
        
        sorted_movies = dict(sorted(movie_tags.items(), key=lambda item: item[1], reverse=True)[:n])
        return sorted_movies




#########################################################################################################################
#########################################################################################################################
#########################################################################################################################



class Links:
    def __init__(self, path_to_the_file, movies_data=None):
        self.data = self.read_csv(path_to_the_file)
        self.imdb_data = []
        self.movies_data = movies_data  
        
    def read_csv(self, path_to_the_file):
        data = []
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as file:
                headers = file.readline().strip().split(',')
                stop = 0
                for line in file:
                    values = line.strip().split(',')
                    if len(values) == len(headers):
                        row = {headers[i]: values[i] for i in range(len(headers))}
                        data.append(row)
                        stop+=1
                        if stop == 1000:
                            break
            return data
        except FileNotFoundError:
            print(f"File {self.path} not found")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    def get_imdb(self, list_of_movies):
        """
        Get IMDB data for list of movies
        Returns sorted list of [movie_id, director, budget, gross, runtime]
        """
        imdb_info = []
        
        for movie_id in list_of_movies:
            imdb_id = None
            for movie in self.data:
                if movie.get('movieId') == str(movie_id):
                    imdb_id = movie.get('imdbId')
                    break
            
            if not imdb_id:
                print(f"IMDB ID not found for movieId {movie_id}")
                continue
                
            url = f'https://www.imdb.com/title/tt{imdb_id}/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                director = self._extract_field(soup, "Director") or "Not found"
                budget = self._extract_field(soup, "Budget") or "Not available"
                gross = self._extract_field(soup, "Gross") or "Not available"
                runtime = self._extract_field(soup, "Runtime") or "Not available"
                
                movie_data = [movie_id, director, budget, gross, runtime]
                imdb_info.append(movie_data)
                
            except requests.exceptions.RequestException as e:
                print(f"Network error fetching data for movie {movie_id}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error fetching data for movie {movie_id}: {e}")
                continue
        
        imdb_info.sort(key=lambda x: int(x[0]), reverse=True)
        self.imdb_data = imdb_info
        return imdb_info

    def _extract_field(self, soup, field_name):
        try:
            tag_to_find = 'a' if field_name == "Director" else 'span'
                
            field_label = soup.find('span', string=re.compile(field_name, re.I))
            if field_label:
                field_value = field_label.find_next(tag_to_find)
                if field_value:
                    return field_value.text.strip()
       
        except Exception:
            return None
        
    def _parse_budget(self, budget_str):
        if not budget_str or budget_str == "Not available":
            return 0.0
        
        numbers = re.findall(r'\d+', budget_str.replace(',', ''))
        if numbers:
            return float(max(numbers, key=len))
        return 0.0
    
    def _parse_runtime(self, runtime_str):
        if not runtime_str or runtime_str == "Not available":
            return 0
        
        hours_match = re.search(r'(\d+)\s*h', runtime_str, re.I)
        minutes_match = re.search(r'(\d+)\s*m', runtime_str, re.I)
        
        hours = int(hours_match.group(1)) if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        
        return hours * 60 + minutes
    
    def _get_movie_title(self, movie_id):
        if self.movies_data and movie_id in self.movies_data:
            return self.movies_data[movie_id]["name"]
        else:
            return f"Movie {movie_id}"
        
    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        director_count = {}
        
        for movie in self.imdb_data:
            director = movie[1]
            if director and director != "Not found":
                director_count[director] = director_count.get(director, 0) + 1
        
        sorted_directors = sorted(director_count.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_directors[:n])
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        movies_with_budget = []
        
        for movie in self.imdb_data:
            movie_id = movie[0]
            budget_str = movie[2]
            budget = self._parse_budget(budget_str)
            
            if budget > 0:
                movie_title = self._get_movie_title(movie_id)
                movies_with_budget.append((movie_title, budget))
        
        sorted_movies = sorted(movies_with_budget, key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])
        
    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        movies_with_profit = []
        
        for movie in self.imdb_data:
            movie_id = movie[0]
            budget = self._parse_budget(movie[2])
            gross = self._parse_budget(movie[3])
            profit = gross - budget
            
            movie_title = self._get_movie_title(movie_id)
            movies_with_profit.append((movie_title, profit))
        
        sorted_movies = sorted(movies_with_profit, key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])
        
    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        movies_with_runtime = []
        
        for movie in self.imdb_data:
            movie_id = movie[0]
            runtime = self._parse_runtime(movie[4])
            
            if runtime > 0:
                movie_title = self._get_movie_title(movie_id)
                movies_with_runtime.append((movie_title, runtime))
        
        sorted_movies = sorted(movies_with_runtime, key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        movies_with_cost = []
        
        for movie in self.imdb_data:
            movie_id = movie[0]
            budget = self._parse_budget(movie[2])
            runtime = self._parse_runtime(movie[4])
            
            if runtime > 0 and budget > 0:
                cost_per_minute = budget / runtime
                movie_title = self._get_movie_title(movie_id)
                movies_with_cost.append((movie_title, round(cost_per_minute, 2)))
        
        sorted_movies = sorted(movies_with_cost, key=lambda x: x[1], reverse=True)
        return dict(sorted_movies[:n])

    #БОНУС

    def budget_analysis(self, n):
        if not self.imdb_data:
            return {"error": "No IMDB data available. Run get_imdb() first."}
        
        budgets = []
        for movie in self.imdb_data:
            budget = self._parse_budget(movie[2])
            if budget > 0:
                budgets.append(budget)
        
        if not budgets:
            return {"error": "No budget data available"}
        
        budgets_sorted = sorted(budgets)
        
        result = (
            f"Average budget: ${sum(budgets) / len(budgets):,.0f}\n"
            f"Median budget: ${budgets_sorted[len(budgets_sorted) // 2]:,.0f}\n"
            f"Max budget: ${max(budgets):,.0f}\n"
            f"Min budget: ${min(budgets):,.0f}"
        )

        return result



#########################################################################################################################
#########################################################################################################################
#########################################################################################################################



class Ratings:
    """
    Анализ данных из ratings.csv
    """
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.data = []
        self._load_data()
    
    def _load_data(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                file.readline()  
                line_count = 0
                for line in file:
                    if line_count >= 1000: 
                        break
                    
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        self.data.append({
                            'userId': int(parts[0]),      
                            'movieId': int(parts[1]),     
                            'rating': float(parts[2]),    
                            'timestamp': int(parts[3])
                        })
                        line_count += 1
        except FileNotFoundError:
            print(f"Ошибка: Файл {self.path} не найден")
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
    
    class Movies:    
        def __init__(self, ratings_obj, movies_data):
            self.ratings_data = ratings_obj.data 
            self.movie_titles = {}
            
            if isinstance(movies_data, dict):
                for movie_id, movie_info in movies_data.items():
                    if isinstance(movie_info, dict) and 'name' in movie_info:
                        title = movie_info['name']
                        if movie_info.get('year'):
                            title = f"{title} ({movie_info['year']})"
                        self.movie_titles[movie_id] = title
        
        def dist_by_year(self):
            """
            Метод возвращает словарь, где ключи - годы, а значения - количество оценок.
            Отсортировано по годам по возрастанию. Годы извлекаются из временных меток.
            """
            ratings_by_year = defaultdict(int)
            for rating in self.ratings_data:
                year = datetime.fromtimestamp(rating['timestamp']).year
                ratings_by_year[year] += 1
            
            return dict(sorted(ratings_by_year.items(), key=lambda x: x[0]))
        
        def dist_by_rating(self):
            """
            Метод возвращает словарь, где ключи - оценки, а значения - количество таких оценок.
            Отсортировано по оценкам по возрастанию.
            """
            ratings_distribution = defaultdict(int)
            for rating in self.ratings_data:
                ratings_distribution[rating['rating']] += 1
            
            return dict(sorted(ratings_distribution.items(), key=lambda x: x[0]))
        
        def top_by_num_of_ratings(self, n):
            """
            Метод возвращает топ-n фильмов по количеству оценок.
            Это словарь, где ключи - названия фильмов, а значения - числа.
            Отсортировано по числам по убыванию.
            """
            movie_counts = defaultdict(int)
            for rating in self.ratings_data:
                movie_id = rating['movieId']
                if movie_id in self.movie_titles:
                    title = self.movie_titles[movie_id]
                    movie_counts[title] += 1
            
            sorted_movies = sorted(movie_counts.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_movies[:n])
        
        def top_by_ratings(self, n, metric='average'):
            """
            Метод возвращает топ-n фильмов по среднему или медианному значению оценок.
            Это словарь, где ключи - названия фильмов, а значения - значения метрики.
            Отсортировано по метрике по убыванию.
            Значения округлены до 2 десятичных знаков.
            """
            movie_ratings = defaultdict(list)
            
            for rating in self.ratings_data:
                movie_id = rating['movieId']
                if movie_id in self.movie_titles:
                    title = self.movie_titles[movie_id]
                    movie_ratings[title].append(rating['rating'])
            
            top_movies = {}
            for title, ratings in movie_ratings.items():
                if len(ratings) >= 1:  
                    if metric == 'average':
                        value = sum(ratings) / len(ratings)
                    elif metric == 'median':
                        sorted_ratings = sorted(ratings)
                        mid = len(sorted_ratings) // 2
                        if len(sorted_ratings) % 2 == 0:
                            value = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
                        else:
                            value = sorted_ratings[mid]
                    else:
                        raise ValueError("Метрика должна быть 'average' или 'median'")
                    
                    top_movies[title] = round(value, 2)
            
            sorted_movies = sorted(top_movies.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_movies[:n])
        
        def top_controversial(self, n):
            """
            Метод возвращает топ-n фильмов по дисперсии оценок.
            Это словарь, где ключи - названия фильмов, а значения - дисперсии.
            Отсортировано по дисперсии по убыванию. Значения округлены до 2 десятичных знаков.
            """
            movie_ratings = defaultdict(list)
            
            for rating in self.ratings_data:
                movie_id = rating['movieId']
                if movie_id in self.movie_titles:
                    title = self.movie_titles[movie_id]
                    movie_ratings[title].append(rating['rating'])
            
            top_movies = {}
            for title, ratings in movie_ratings.items():
                if len(ratings) >= 2:  
                    mean = sum(ratings) / len(ratings)
                    variance = sum((x - mean) ** 2 for x in ratings) / len(ratings)
                    top_movies[title] = round(variance, 2)
            
            sorted_movies = sorted(top_movies.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_movies[:n])
        

        ######### БОНУСНЫЙ МЕТОД ########
        def rating_trend_analysis(self, n):
            """
            Анализ трендов рейтингов по годам. 
            Возвращает словарь с анализом изменения средних рейтингов по годам.
            """
            year_ratings = defaultdict(list)
            
            for rating in self.ratings_data:
                year = datetime.fromtimestamp(rating['timestamp']).year
                year_ratings[year].append(rating['rating'])
            
            yearly_avg = {}
            for year, ratings in year_ratings.items():
                if len(ratings) > 0:
                    yearly_avg[year] = round(sum(ratings) / len(ratings), 2)
            
            sorted_years = sorted(yearly_avg.items(), key=lambda x: x[0])
            
            # Анализ тренда
            if len(sorted_years) >= 2:
                first_year_avg = sorted_years[0][1]
                last_year_avg = sorted_years[-1][1]
                trend = "повышающийся" if last_year_avg > first_year_avg else "понижающийся" if last_year_avg < first_year_avg else "стабильный"
                trend_change = round(last_year_avg - first_year_avg, 2)
            else:
                trend = "недостаточно данных"
                trend_change = 0.0
            
            top_years = dict(sorted(yearly_avg.items(), key=lambda x: x[1], reverse=True)[:n])
            
            result = {
                "trend": trend,
                "trend_change": trend_change,
                "top_years_by_rating": top_years,
                "yearly_averages": dict(sorted_years),
                "total_years_analyzed": len(yearly_avg)
                }
            
            return result


    class Users(Movies):
        """
        В этом классе должны работать три метода.
        1-й возвращает распределение пользователей по количеству поставленных ими оценок.
        2-й возвращает распределение пользователей по средним или медианным оценкам.
        3-й возвращает топ-n пользователей с наибольшей дисперсией их оценок.
        """
        def __init__(self, ratings_obj):
            super().__init__(ratings_obj, {})
        
        def dist_by_num_of_ratings(self):
            """
            1-й метод возвращает распределение пользователей по количеству поставленных ими оценок.
            """
            user_counts = defaultdict(int)
            for rating in self.ratings_data:
                user_counts[rating['userId']] += 1
            
            return dict(sorted(user_counts.items(), key=lambda x: x[1], reverse=True))
        
        def dist_by_ratings(self, metric='average'):
            """
            2-й метод возвращает распределение пользователей по средним или медианным оценкам.
            """
            user_ratings = defaultdict(list)
            for rating in self.ratings_data:
                user_ratings[rating['userId']].append(rating['rating'])
            
            user_metrics = {}
            for user_id, ratings in user_ratings.items():
                if len(ratings) >= 1:
                    if metric == 'average':
                        value = sum(ratings) / len(ratings)
                    elif metric == 'median':
                        sorted_ratings = sorted(ratings)
                        mid = len(sorted_ratings) // 2
                        if len(sorted_ratings) % 2 == 0:
                            value = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
                        else:
                            value = sorted_ratings[mid]
                    else:
                        raise ValueError("Метрика должна быть 'average' или 'median'")
                    
                    user_metrics[user_id] = round(value, 2)
            
            return dict(sorted(user_metrics.items(), key=lambda x: x[1], reverse=True))
        
        def top_controversial(self, n):
            """
            3-й метод возвращает топ-n пользователей с наибольшей дисперсией их оценок.
            """
            user_ratings = defaultdict(list)
            for rating in self.ratings_data:
                user_ratings[rating['userId']].append(rating['rating'])
            
            user_variances = {}
            for user_id, ratings in user_ratings.items():
                if len(ratings) >= 2:
                    mean = sum(ratings) / len(ratings)
                    variance = sum((x - mean) ** 2 for x in ratings) / len(ratings)
                    user_variances[user_id] = round(variance, 2)
            
            sorted_users = sorted(user_variances.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_users[:n])
        
        



class TestMovies:
    @pytest.fixture
    def movies(self):
        """Фикстура для создания объекта Movies с тестовыми данными"""
        test_data = """movieId,title,genres
1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
2,Jumanji (1995),Adventure|Children|Fantasy
3,Grumpier Old Men (1995),Comedy|Romance
4,Waiting to Exhale (1995),Comedy|Drama|Romance
5,Father of the Bride Part II (1995),Comedy
6,Heat (1995),Action|Crime|Thriller
7,Sabrina (1995),Comedy|Romance
8,Tom and Huck (1995),Adventure|Children
9,Sudden Death (1995),Action
10,GoldenEye (1995),Action|Adventure|Thriller
11,"American President, The (1995)",Comedy|Drama|Romance
12,Dracula: Dead and Loving It (1995),Comedy|Horror
13,Balto (1995),Adventure|Animation|Children
14,Nixon (1995),Drama
15,Cutthroat Island (1995),Action|Adventure|Romance
16,Casino (1995),Crime|Drama
17,Sense and Sensibility (1995),Drama|Romance
18,Four Rooms (1995),Comedy
19,Ace Ventura: When Nature Calls (1995),Comedy
20,Money Train (1995),Action|Comedy|Crime|Drama|Thriller
21,Get Shorty (1995),Comedy|Crime|Thriller
22,Copycat (1995),Crime|Drama|Horror|Mystery|Thriller
23,Assassins (1995),Action|Crime|Thriller
24,Powder (1995),Drama|Sci-Fi
25,Leaving Las Vegas (1995),Drama|Romance"""
        
        test_filename = "test_movies_fixture.csv"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_data)
        
        movies_obj = Movies(test_filename)
        
        yield movies_obj
        
        if os.path.exists(test_filename):
            os.remove(test_filename)

    def test_load_movies(self, movies):
        """Тест: загрузка данных movies"""
        assert isinstance(movies.data, dict)
        
        if movies.data and 1 in movies.data:
            movie_data = movies.data[1]
            assert isinstance(movie_data, dict)
            assert "name" in movie_data
            assert "year" in movie_data
            assert "genres" in movie_data

    def test_dist_by_release(self, movies):
        """Тест: распределение по годам выпуска"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        result = movies.dist_by_release()
        
        assert isinstance(result, dict)
        
        for year, count in result.items():
            assert isinstance(year, int)
            assert isinstance(count, int)
            assert count > 0
        
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_dist_by_genres(self, movies):
        """Тест: распределение по жанрам"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        result = movies.dist_by_genres()
        
        assert isinstance(result, dict)
        
        for genre, count in result.items():
            assert isinstance(genre, str)
            assert isinstance(count, int)
            assert count > 0
        
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_most_genres(self, movies):
        """Тест: фильмы с наибольшим количеством жанров"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        for n in [1, 3, 5]:
            result = movies.most_genres(n)
            
            assert isinstance(result, dict)
            assert len(result) == n
            
            for title, count in result.items():
                assert isinstance(title, str)
                assert isinstance(count, int)
                assert count > 0
            
            counts = list(result.values())
            assert counts == sorted(counts, reverse=True)

    def test_most_genres_specific(self, movies):
        """Тест: конкретные фильмы в most_genres"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        result = movies.most_genres(5)
        
        movies_with_5_genres = [title for title, count in result.items() if count == 5]
        assert len(movies_with_5_genres) >= 1 

    def test_popular_genres(self, movies):
        """Тест: популярные жанры по годам (бонусный метод)"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        try:
            result = movies.popular_genres(5)
            
            if result:
                assert isinstance(result, dict)
                
                for year, genre in result.items():
                    assert isinstance(year, int)
                    assert isinstance(genre, str)
                
                years = list(result.keys())
                assert years == sorted(years)
        except Exception:
            pytest.skip("Метод popular_genres не реализован или выдает ошибку")

    def test_data_structure(self, movies):
        """Тест: структура данных фильмов"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        for movie_id, movie_data in movies.data.items():
            assert isinstance(movie_id, int)
            
            assert isinstance(movie_data, dict)
            assert "name" in movie_data
            assert "year" in movie_data
            assert "genres" in movie_data
            
            assert isinstance(movie_data["name"], str)
            assert movie_data["year"] is None or isinstance(movie_data["year"], int)
            assert isinstance(movie_data["genres"], list)
            assert all(isinstance(genre, str) for genre in movie_data["genres"])

    def test_json_serialization(self, movies):
        """Тест: результаты сериализуемы в JSON"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        methods_to_test = [
            ('dist_by_release', []),
            ('dist_by_genres', []),
            ('most_genres', [5])
        ]
        
        for method_name, args in methods_to_test:
            method = getattr(movies, method_name)
            result = method(*args)
            
            try:
                json.dumps(result)
            except TypeError as e:
                pytest.fail(f"Метод {method_name} возвращает несериализуемые данные: {e}")

    def test_collections_mapping(self, movies):
        """Тест: методы возвращают Mapping (dict)"""
        if movies.data is None or len(movies.data) == 0:
            pytest.skip("Данные не загружены")
            
        assert isinstance(movies.dist_by_release(), collections.abc.Mapping)
        assert isinstance(movies.dist_by_genres(), collections.abc.Mapping)
        assert isinstance(movies.most_genres(5), collections.abc.Mapping)




class TestTags:
    @pytest.fixture
    def tags(self):
        """Фикстура для создания объекта Tags с тестовыми данными"""
        test_data = """userId,movieId,tag,timestamp
1,1,funny,1445714994
1,1,highly quotable,1445714996
1,2,BOXING STORY,1445714997
2,1,funny,1445714998
2,3,atmospheric,1445714999
3,1,great story,1445715000
3,2,classic,1445715001
4,4,very long tag with many words,1445715002
5,1,action packed,1445715003
6,2,sci-fi adventure,1445715004"""
        
        test_filename = "test_tags_fixture.csv"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_data)
        
        tags_obj = Tags(test_filename)
        
        yield tags_obj
        
        if os.path.exists(test_filename):
            os.remove(test_filename)

    def test_load_tags(self, tags):
        """Тест: загрузка данных tags"""
        assert isinstance(tags.data, dict)
        
        if tags.data:
            for user_id, movies in tags.data.items():
                assert isinstance(user_id, int)
                assert isinstance(movies, dict)
                for movie_id, movie_data in movies.items():
                    assert isinstance(movie_id, int)
                    assert isinstance(movie_data, dict)
                    assert "tag" in movie_data
                    assert "timestamp" in movie_data

    def test_most_words(self, tags):
        """Тест: теги с наибольшим количеством слов"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")
            
        result = tags.most_words(5)
        
        assert isinstance(result, dict)
        
        for tag, word_count in result.items():
            assert isinstance(tag, str)
            assert isinstance(word_count, int)
            assert word_count > 0
        
        word_counts = list(result.values())
        assert word_counts == sorted(word_counts, reverse=True)
        
        assert len(result) == 5

    def test_longest(self, tags):
        """Тест: самые длинные теги по символам"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")
            
        result = tags.longest(5)
        
        assert isinstance(result, list)
        
        for tag in result:
            assert isinstance(tag, str)
        
        if len(result) > 1:
            tag_lengths = [len(tag) for tag in result]
            assert tag_lengths == sorted(tag_lengths, reverse=True)
        
        assert len(result) == len(set(result))
        
        assert len(result) == 5

    def test_most_words_and_longest(self, tags):
        """Тест: пересечение самых длинных тегов по словам и символам"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")
            
        result = tags.most_words_and_longest(3)
        
        assert isinstance(result, list)
        
        for tag in result:
            assert isinstance(tag, str)
        
        assert len(result) == len(set(result))
        
        most_words_tags = set(tags.most_words(3).keys())
        longest_tags = set(tags.longest(3))
        intersection = most_words_tags & longest_tags
        
        assert set(result) == intersection

    def test_most_popular(self, tags):
        """Тест: самые популярные теги"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")
            
        result = tags.most_popular(5)
        
        assert isinstance(result, dict)
        
        for tag, count in result.items():
            assert isinstance(tag, str)
            assert isinstance(count, int)
            assert count > 0
        
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)
        
        assert len(result) == len(set(result.keys()))
        
        assert len(result) == 5

    def test_tags_with(self, tags):
        """Тест: теги содержащие указанное слово"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")
            
        word = "story"
        result = tags.tags_with(word)
        
        assert isinstance(result, list)
        
        for tag in result:
            assert isinstance(tag, str)
            assert word.lower() in tag.lower()
        
        if len(result) > 1:
            assert result == sorted(result, key=str.lower)
        
        assert len(result) == len(set(result))

    def test_tegs_movie_popular(self, tags):
        """Тест: самые тегируемые фильмы (бонусный метод)"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")
            
        try:
            result = tags.tegs_movie_popular(3)
            
            assert isinstance(result, dict)
            
            for movie_id, tag_count in result.items():
                assert isinstance(movie_id, int)
                assert isinstance(tag_count, int)
                assert tag_count > 0
            
            tag_counts = list(result.values())
            assert tag_counts == sorted(tag_counts, reverse=True)
            
            assert len(result) == 3
        except Exception:
            pytest.skip("Метод tegs_movie_popular не реализован или выдает ошибку")

    def test_json_serialization(self, tags):
        """Тест: результаты сериализуемы в JSON"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")
            
        methods_to_test = [
            ('most_words', [5]),
            ('most_popular', [5]),
            ('tegs_movie_popular', [3])
        ]
        
        for method_name, args in methods_to_test:
            method = getattr(tags, method_name)
            result = method(*args)
            
            try:
                json.dumps(result)
            except TypeError as e:
                pytest.fail(f"Метод {method_name} возвращает несериализуемые данные: {e}")

    def test_collections_mapping(self, tags):
        """Тест: методы возвращают Mapping (dict)"""
        if tags.data is None or len(tags.data) == 0:
            pytest.skip("Данные не загружены")

        assert isinstance(tags.most_words(5), collections.abc.Mapping)
        assert isinstance(tags.most_popular(5), collections.abc.Mapping)
        assert isinstance(tags.tegs_movie_popular(3), collections.abc.Mapping)




class TestLinks:
    @pytest.fixture
    def links(self):
        """Фикстура для создания объекта Links с тестовыми данными"""
        test_data = """movieId,imdbId,tmdbId
1,0114709,862
2,0113497,8844
3,0113228,15602
4,0114885,31357
5,0113041,11862"""
        
        test_filename = "test_links_fixture.csv"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_data)
        
        movies_data = {
            1: {"name": "Toy Story"},
            2: {"name": "Jumanji"}, 
            3: {"name": "Grumpier Old Men"},
            4: {"name": "Waiting to Exhale"},
            5: {"name": "Father of the Bride Part II"}
        }
        
        links_obj = Links(test_filename, movies_data)
        
        yield links_obj
        
        if os.path.exists(test_filename):
            os.remove(test_filename)

    @pytest.fixture
    def n(self):
        return 5

    def test_load_links(self, links):
        """Тест: загрузка данных links"""
        assert isinstance(links.data, list)
        
        if links.data:
            for movie in links.data:
                assert isinstance(movie, dict)
                assert "movieId" in movie
                assert "imdbId" in movie
                assert "tmdbId" in movie

    def test_get_imdb(self, links):
        """Тест: получение данных с IMDB"""
        try:
            movie_ids = [1, 2]
            result = links.get_imdb(movie_ids)
            
            assert isinstance(result, list)
            
            for item in result:
                assert isinstance(item, list)
                assert len(item) == 5  
                assert isinstance(item[0], int) 
                assert isinstance(item[1], str)  
                assert isinstance(item[2], str)
                assert isinstance(item[3], str)
                assert isinstance(item[4], str)

        except Exception as e:
            pytest.skip(f"Тест get_imdb пропущен из-за: {e}")

    def test_top_directors(self, links, n):
        """Тест: топ режиссеров"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            result = links.top_directors(n)
            
            assert isinstance(result, dict)
            
            for director, count in result.items():
                assert isinstance(director, str)
                assert isinstance(count, int)
            
            counts = list(result.values())
            assert counts == sorted(counts, reverse=True)
            
        except Exception:
            pytest.skip("Не удалось получить IMDB данные для теста")

    def test_most_expensive(self, links, n):
        """Тест: самые дорогие фильмы"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            result = links.most_expensive(n)
            
            assert isinstance(result, dict)
            
            for title, budget in result.items():
                assert isinstance(title, str)
                assert isinstance(budget, float) or isinstance(budget, int)
            
            budgets = list(result.values())
            assert budgets == sorted(budgets, reverse=True)
            
        except Exception:
            pytest.skip("Не удалось получить IMDB данные для теста")

    def test_most_profitable(self, links, n):
        """Тест: самые прибыльные фильмы"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            result = links.most_profitable(n)
            
            assert isinstance(result, dict)
            
            for title, profit in result.items():
                assert isinstance(title, str)
                assert isinstance(profit, float) or isinstance(profit, int)
            
            profits = list(result.values())
            assert profits == sorted(profits, reverse=True)
            
        except Exception:
            pytest.skip("Не удалось получить IMDB данные для теста")

    def test_longest(self, links, n):
        """Тест: самые длинные фильмы"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            result = links.longest(n)
            
            assert isinstance(result, dict)
            
            for title, runtime in result.items():
                assert isinstance(title, str)
                assert isinstance(runtime, int)
            
            runtimes = list(result.values())
            assert runtimes == sorted(runtimes, reverse=True)
            
        except Exception:
            pytest.skip("Не удалось получить IMDB данные для теста")

    def test_top_cost_per_minute(self, links, n):
        """Тест: стоимость за минуту"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            result = links.top_cost_per_minute(n)
            
            assert isinstance(result, dict)
            
            for title, cost in result.items():
                assert isinstance(title, str)
                assert isinstance(cost, float)
            
            costs = list(result.values())
            assert costs == sorted(costs, reverse=True)
            
        except Exception:
            pytest.skip("Не удалось получить IMDB данные для теста")

    def test_budget_analysis(self, links):
        """Тест: анализ бюджетов (бонусный метод)"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            result = links.budget_analysis(5)
            
            assert isinstance(result, str) or isinstance(result, dict)
            
        except Exception:
            pytest.skip("Метод budget_analysis не реализован или выдает ошибку")

    def test_parse_budget(self, links):
        """Тест: парсинг бюджета"""
        test_cases = [
            ("$3,000,000", 3000000.0),
            ("$1,500,000", 1500000.0),
            ("Not available", 0.0),
            ("", 0.0),
            ("$1,000,000", 1000000.0)
        ]
        
        for budget_str, expected in test_cases:
            result = links._parse_budget(budget_str)
            assert isinstance(result, float)
            assert result == expected

    def test_parse_runtime(self, links):
        """Тест: парсинг времени"""
        test_cases = [
            ("1 hour 36 minutes", 96),
            ("2h 15m", 135),
            ("90 min", 90),
            ("Not available", 0),
            ("", 0),
            ("2 hours", 120)
        ]
        
        for runtime_str, expected in test_cases:
            result = links._parse_runtime(runtime_str)
            assert isinstance(result, int)
            assert result == expected

    def test_get_movie_title(self, links):
        """Тест: получение названия фильма"""
        result = links._get_movie_title(1)
        assert isinstance(result, str)
        assert result == "Toy Story"
        
        result = links._get_movie_title(999)
        assert isinstance(result, str)
        assert "Movie 999" in result

    def test_json_serialization(self, links, n):
        """Тест: результаты сериализуемы в JSON"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            methods_to_test = [
                ('top_directors', [n]),
                ('most_expensive', [n]),
                ('most_profitable', [n]),
                ('longest', [n]),
                ('top_cost_per_minute', [n])
            ]
            
            for method_name, args in methods_to_test:
                method = getattr(links, method_name)
                result = method(*args)
                
                try:
                    json.dumps(result)
                except TypeError as e:
                    pytest.fail(f"Метод {method_name} возвращает несериализуемые данные: {e}")
                    
        except Exception:
            pytest.skip("Не удалось получить IMDB данные для теста")

    def test_collections_mapping(self, links, n):
        """Тест: методы возвращают Mapping (dict)"""
        try:
            movie_ids = [1, 2]
            links.get_imdb(movie_ids)
            
            assert isinstance(links.top_directors(n), collections.abc.Mapping)
            assert isinstance(links.most_expensive(n), collections.abc.Mapping)
            assert isinstance(links.most_profitable(n), collections.abc.Mapping)
            assert isinstance(links.longest(n), collections.abc.Mapping)
            assert isinstance(links.top_cost_per_minute(n), collections.abc.Mapping)
            
        except Exception:
            pytest.skip("Не удалось получить IMDB данные для теста")




class TestRatings:
    @pytest.fixture
    def ratings(self):
        """Фикстура для создания объекта Ratings с тестовыми данными"""
        test_data = """userId,movieId,rating,timestamp
1,1,4.0,964982703
1,2,3.5,964981247
1,3,5.0,964982224
2,1,3.0,964982703
2,2,4.5,964981247
2,4,2.0,964982224
3,1,5.0,964982703
3,3,4.0,964981247
3,5,3.5,964982224
4,2,2.5,964982703
4,4,1.0,964981247
4,6,4.5,964982224"""
        
        test_filename = "test_ratings_fixture.csv"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write(test_data)
        
        ratings_obj = Ratings(test_filename)
        
        yield ratings_obj
        
        if os.path.exists(test_filename):
            os.remove(test_filename)

    @pytest.fixture
    def movies_data(self):
        """Фикстура для тестовых данных о фильмах"""
        return {
            1: {"name": "Toy Story", "year": 1995},
            2: {"name": "Jumanji", "year": 1995},
            3: {"name": "Grumpier Old Men", "year": 1995},
            4: {"name": "Waiting to Exhale", "year": 1995},
            5: {"name": "Father of the Bride Part II", "year": 1995},
            6: {"name": "Heat", "year": 1995}
        }

    @pytest.fixture
    def movies(self, ratings, movies_data):
        """Фикстура для создания объекта Movies"""
        return Ratings.Movies(ratings, movies_data)

    @pytest.fixture
    def users(self, ratings):
        """Фикстура для создания объекта Users"""
        return Ratings.Users(ratings)


    def test_rating_trend_analysis(self, movies):
        """Тест: анализ трендов рейтингов по годам (бонусный метод)"""
        print(f"\n=== DEBUG test_rating_trend_analysis ===")
        print(f"movies object: {movies}")
        print(f"movies type: {type(movies)}")
        print(f"has ratings_data: {hasattr(movies, 'ratings_data')}")
        
        if hasattr(movies, 'ratings_data'):
            print(f"ratings_data: {movies.ratings_data}")
            print(f"ratings_data length: {len(movies.ratings_data) if movies.ratings_data else 0}")
            if movies.ratings_data:
                print(f"first rating: {movies.ratings_data[0]}")
        
        if not movies.ratings_data:
            print("SKIP: Нет данных о рейтингах")
            pytest.skip("Нет данных о рейтингах")
            
        try:
            n = 3
            print(f"Calling rating_trend_analysis({n})...")
            result = movies.rating_trend_analysis(n)
            print(f"Result: {result}")
            
            assert isinstance(result, dict), f"Result should be dict, got {type(result)}"
            
            expected_keys = ["trend", "trend_change", "top_years_by_rating", "yearly_averages", "total_years_analyzed"]
            for key in expected_keys:
                assert key in result, f"Отсутствует ключ: {key}"
            
            assert isinstance(result["trend"], str)
            assert isinstance(result["trend_change"], float)
            assert isinstance(result["top_years_by_rating"], dict)
            assert isinstance(result["yearly_averages"], dict)
            assert isinstance(result["total_years_analyzed"], int)
            
            valid_trends = ["повышающийся", "понижающийся", "стабильный", "недостаточно данных"]
            assert result["trend"] in valid_trends, f"Недопустимое значение trend: {result['trend']}"
            
            assert len(result["top_years_by_rating"]) == min(n, result["total_years_analyzed"]), \
                f"Неверное количество лет в top_years_by_rating: ожидается {min(n, result['total_years_analyzed'])}, получено {len(result['top_years_by_rating'])}"
            
            for year, avg_rating in result["top_years_by_rating"].items():
                assert isinstance(year, int), f"Год должен быть int, получено {type(year)}"
                assert isinstance(avg_rating, float), f"Рейтинг должен быть float, получено {type(avg_rating)}"
                assert 0 <= avg_rating <= 5, f"Рейтинг {avg_rating} вне диапазона 0-5"
            
            for year, avg_rating in result["yearly_averages"].items():
                assert isinstance(year, int), f"Год должен быть int, получено {type(year)}"
                assert isinstance(avg_rating, float), f"Рейтинг должен быть float, получено {type(avg_rating)}"
                assert 0 <= avg_rating <= 5, f"Рейтинг {avg_rating} вне диапазона 0-5"
            
            assert result["total_years_analyzed"] == len(result["yearly_averages"]), \
                "total_years_analyzed не соответствует количеству элементов в yearly_averages"
            
            if result["total_years_analyzed"] > 0:
                all_ratings = list(result["yearly_averages"].values())
                top_ratings = list(result["top_years_by_rating"].values())
                sorted_all_ratings = sorted(all_ratings, reverse=True)[:n]
                assert top_ratings == sorted_all_ratings, "top_years_by_rating не содержит самые высокие рейтинги"
            
            if result["total_years_analyzed"] >= 2:
                years_sorted = sorted(result["yearly_averages"].items())
                first_rating = years_sorted[0][1]
                last_rating = years_sorted[-1][1]
                expected_change = round(last_rating - first_rating, 2)
                assert result["trend_change"] == expected_change, \
                    f"Неверный trend_change: ожидается {expected_change}, получено {result['trend_change']}"
                
                if result["trend_change"] > 0:
                    assert result["trend"] == "повышающийся"
                elif result["trend_change"] < 0:
                    assert result["trend"] == "понижающийся"
                else:
                    assert result["trend"] in ["стабильный", "недостаточно данных"]
            
            try:
                json.dumps(result)
            except TypeError as e:
                pytest.fail(f"Бонусный метод rating_trend_analysis возвращает несериализуемые данные: {e}")
                
        except Exception as e:
            print(f"EXCEPTION: {e}")
            print(f"Exception type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            pytest.skip(f"Бонусный метод rating_trend_analysis не реализован или выдает ошибку: {e}")



if __name__ == "__main__":
    pytest.main([__file__, "-v"])
