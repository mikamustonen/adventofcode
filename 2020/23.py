# Part 1
def simulate_game(cups: list[int], number_of_moves: int, number_of_results: int) -> list[int]:

    # Construct a list pointing to the next cup from the index
    # Assume that cup numbers run from 1 to len(cups)
    # Item 0 is dummy
    links = [0 for _ in range(0, len(cups) + 1)]
    previous_cup = cups[-1]
    for cup in cups:
        links[previous_cup] = cup
        previous_cup = cup

    current_cup = cups[0]
    for turn in range(number_of_moves):

        cup1 = links[current_cup]
        cup2 = links[cup1]
        cup3 = links[cup2]
        pick_up = [cup1, cup2, cup3]

        destination = current_cup - 1
        if destination == 0:
            destination = len(cups)
        while destination in pick_up:
            destination -= 1
            if destination == 0:
                destination = len(cups)

        cup_after_pickup = links[cup3]
        links[cup3] = links[destination]
        links[destination] = cup1
        links[current_cup] = cup_after_pickup

        current_cup = links[current_cup]

    # Game over; return the requested number of items after cup 1
    result = []
    cup = 1
    for _ in range(number_of_results):
        cup = links[cup]
        result.append(cup)

    return result


cups = [int(x) for x in "137826495"]
print("".join(str(x) for x in simulate_game(cups, 100, len(cups) - 1)))


# Part 2
cups.extend(range(len(cups) + 1, 1000000 + 1))
x, y = simulate_game(cups, 10000000, 2)
print(f"{x} x {y} = {x * y}")
