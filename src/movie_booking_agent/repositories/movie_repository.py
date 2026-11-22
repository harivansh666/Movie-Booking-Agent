from __future__ import annotations

from collections.abc import Sequence
from movie_booking_agent.schemas.movie import Movie
class MovieRepository:
    def __init__(slef, movies: Sequence[Movie]) -> None:
        slef.movies: dict[str, Movie] = { movie.id: movie for movie in movies}

    def get(self, movie_id:str)-> Movie | None :
        return self.movies.get(movie_id)

    def list_all(self)-> list[Movie]:
        return sorted(self.movies.values(), key=lambda movie: movie.title)

    def search(self, *, genre: str | None, language:str | None, movie_ids: set[str] | None = None)-> list[Movie]:
        result = list(self.movies.values())
        if movie_ids is not None:
            return [ movie for movie in result if movie.id in movie_ids]

        if genre : 
            needle = genre.strip().casefold()
            result = [
                movie
                for movie in result
                if any(needle in item.casefold() for item in movie.gener)
            ]
        
        if language:
            needle = language.strip().casefold()
            results = [
                movie
                for movie in results
                if any(needle in item.casefold() for item in movie.languages)
            ]
        return sorted(results, key=lambda movie: movie.title)


