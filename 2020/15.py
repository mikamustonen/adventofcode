# Part 1
def play_game(number_of_turns: int, starting_numbers: list[int]) -> int:
    last_turn_spoken = {}

    for turn in range(1, number_of_turns + 1):
        number = starting_numbers[turn - 1] if turn <= len(starting_numbers) else next_number
        next_number = 0 if number not in last_turn_spoken else turn - last_turn_spoken[number]
        last_turn_spoken[number] = turn

    return number


starting_numbers = [1, 2, 16, 19, 18, 0]
print(play_game(2020, starting_numbers))

# Part 2
print(play_game(30000000, starting_numbers))
