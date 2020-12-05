from pathlib import Path


class Seat:
    def __init__(self, boarding_pass_id: str) -> None:
        # seats are encoded in binary in disguise
        self.code = boarding_pass_id
        self.id = int(self.code.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2)

    @property
    def row(self) -> int:
        return self.id // 8

    @property
    def column(self) -> int:
        return self.id % 8


# Part 1
input_path = Path("input") / "05.txt"
with input_path.open() as f:
    seats = [Seat(line.strip()) for line in f]
print(max(seat.id for seat in seats))

# Part 2
occupied_seat_ids = set(seat.id for seat in seats)
for i in range(1024):
    if i not in occupied_seat_ids and (i - 1) in occupied_seat_ids and (i + 1) in occupied_seat_ids:
        print(f"Found the seat: {i}")
        # There should be only one answer, but let's finish the loop to make sure
