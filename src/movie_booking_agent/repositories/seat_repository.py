
from threading import RLock
from movie_booking_agent.schemas.common import SeatStatus
from collections.abc import Mapping
class SeatUnavailableError(Exception):
    def __init__(self, labels: Sequence[str]) -> None:
        self.labels = list(labels)
        super().__init__(f"Seats no longer available: {', '.join(self.labels)}")


class SeatRepository:
    def __init__(self, seats: Mapping[str, Mapping[str, ShowSeat]]) -> None:
        self._seats: dict[str, dict[str, ShowSeat]] = {
            show_id: {label: seat for label, seat in show_seats.items()}
            for show_id, show_seats in seats.items()
        }
        self._lock = RLock()

    def get_seats(self, show_id: str) -> list[ShowSeat]:
        show_seats = self._seats.get(show_id, {})
        return sorted(show_seats.values(), key=lambda seat: (seat.row, seat.number))

    def get_seat(self, show_id: str, label: str) -> ShowSeat | None:
        return self._seats.get(show_id, {}).get(label)

    def available_count(self, show_id: str) -> int:
        return sum(
            seat.status is SeatStatus.AVAILABLE for seat in self._seats.get(show_id, {}).values()
        )

    def min_price(self, show_id: str) -> int:
        prices = [seat.price_inr for seat in self._seats.get(show_id, {}).values()]
        return min(prices) if prices else 0

    def check_available(
        self, show_id: str, labels: Sequence[str]
    ) -> tuple[list[ShowSeat], list[str]]:
        show_seats = self._seats.get(show_id, {})
        selected: list[ShowSeat] = []
        unavailable: list[str] = []

        for label in self._normalise_labels(labels):
            seat = show_seats.get(label)
            if seat is None or seat.status is not SeatStatus.AVAILABLE:
                unavailable.append(label)
            else:
                selected.append(seat)

        return selected, unavailable

    def mark_booked(self, show_id: str, labels: Sequence[str], booking_id: str) -> list[ShowSeat]:
        normalised = self._normalise_labels(labels)
        with self._lock:
            show_seats = self._seats.get(show_id, {})
            unavailable = [
                label
                for label in normalised
                if label not in show_seats
                or show_seats[label].status is not SeatStatus.AVAILABLE
            ]
            if unavailable:
                raise SeatUnavailableError(unavailable)

            booked: list[ShowSeat] = []
            for label in normalised:
                seat = show_seats[label].model_copy(
                    update={"status": SeatStatus.BOOKED, "booking_id": booking_id}
                )
                show_seats[label] = seat
                booked.append(seat)
            return booked

    def release_for_booking(
        self, show_id: str, labels: Sequence[str], booking_id: str
    ) -> list[ShowSeat]:
        released: list[ShowSeat] = []
        with self._lock:
            show_seats = self._seats.get(show_id, {})
            for label in self._normalise_labels(labels):
                seat = show_seats.get(label)
                if seat is None or seat.booking_id != booking_id:
                    continue
                updated = seat.model_copy(
                    update={"status": SeatStatus.AVAILABLE, "booking_id": None}
                )
                show_seats[label] = updated
                released.append(updated)
        return released

    @staticmethod
    def _normalise_labels(labels: Sequence[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for raw in labels:
            label = raw.strip().upper()
            if label and label not in seen:
                seen.add(label)
                result.append(label)
        return result


