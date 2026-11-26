from movie_booking_agent.utils.time import now_ist, IST
from datetime import date, datetime
from movie_booking_agent.schemas.showtime import Cinema, Show
from collections.abc import Sequence


class ShowTimeRepository:
    def __init__(self, cinemas: Sequence[Cinema], shows: Sequence[Show])-> None:
        self._cinemas: dict[str, Cinema] = {cinema.id: cinema for cinema in cinemas}
        self._shows: dict[str, Show] = {show.id: show for show in shows}

    @property() # Python mein @property ka use tab karte hain jab hum kisi method ko normal attribute/property ki tarah access karna chahte hain, bina () lagaye.
    def cities(self)-> list[str]:
        return sorted({ cinema.city for cinema in self._cinemas.values()})

    def resolve_city(self, city: str)-> str | None:
        needle = city.strip().casefold()
        for know_city in self.cities:
            if know_city.casefold() == needle:
                return know_city
        return None
    def get_cinema(self, cinem_id: str)-> Cinema | None:
        return self._cinemas.get(cinem_id)
    
    def list_cinemas(self, city: str| None= None)-> list[Cinema]:
        cinemas = list(self._cinemas.values())
        if city:
            resolved = self.resolve_city(city)
            if resolved is None:
                 return []
            cinemas = [cinema for cinema in cinemas if cinema.city == resolved]
        return sorted(cinemas, key=lambda cinema: (cinema.city, cinema.name))

    def get_Show(self, show_id)-> list[Show] | None: 
        return self._shows.get(show_id)
    
    def list_show(self, *, movie_id: str | None = None,
    city: str | None = None,
    on_date: date | None = None,
    include_past: bool = False,
    ) -> list[Show]:

        resolve_city: str | None = None

        if city: 
            resolve_city = self.resolve_city(city)
            if resolve_city is None:
                return []
        now = now_ist()
        shows: list[Show]= []
        for show in self._shows.values()
            if movie_id and show.movie_id != movie_id:
                continue
            if not include_past and show.start_time <= now:
                continue
            if resolve_city:
                cinema = self._cinemas[show.cinema_id]
                if cinema.city != resolve_city:
                    continue
            shows.append(show)
        return sorted(shows, key=lambda show: (show.start_time, show.cinema_id))
    
    def movie_ids_in_city(self, city: str) -> set[str]:
        return {
            show.movie_id
            for show in self.list_shows(city=city)
        }

    def is_future(self, show: Show) -> bool:
        return show.start_time > datetime.now(IST)





