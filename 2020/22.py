from itertools import count
from pathlib import Path
from copy import deepcopy


input_file = Path("input") / "22.txt"

# Each deck is represented by a list, with the topmost card in the beginning
decks = []
with input_file.open() as f:
    for section in f.read().split("\n\n"):
        decks.append([int(line) for line in section.strip().split("\n")[1:]])
initial_decks = deepcopy(decks)


# Part 1
def print_decks(decks: list[list[int]]) -> None:
    for i, deck in enumerate(decks, start=1):
        print(f"Player {i}'s deck: " + ", ".join(str(card) for card in deck))


def score(deck: list[int]) -> int:
    return sum(i * card for i, card in enumerate(deck[::-1], start=1))


round_ = 1
while all(len(deck) > 0 for deck in decks):
    print(f"-- Round {round_} --")
    print_decks(decks)
    played_cards = [deck.pop(0) for deck in decks]
    for i, card in enumerate(played_cards, start=1):
        print(f"Player {i} plays {card}")
    winner = 1 if played_cards[0] > played_cards[1] else 2
    print(f"Player {winner} wins the round!\n")
    round_ += 1
    decks[winner - 1].extend(sorted(played_cards, reverse=True))

print("== Post-game results ==")
print_decks(decks)
print(f"Winning player's score: {score(decks[winner - 1])}")
print()


# Part 2
game_counter = count(start=1)


def recursive_combat(decks: list[list[int]]) -> tuple[int, list[list[int]]]:
    encountered_states = set()
    game = next(game_counter)
    round_ = 0
    while all(len(deck) > 0 for deck in decks):
        round_ += 1
        print(f"-- Round {round_} (Game {game}) --")
        print_decks(decks)
        this_game_state = tuple(tuple(deck) for deck in decks)
        if this_game_state in encountered_states:
            print("This game state has been seen before, Player 1 wins!")
            winner = 1
            break
        encountered_states.add(this_game_state)
        played_cards = [deck.pop(0) for deck in decks]
        for i, card in enumerate(played_cards, start=1):
            print(f"Player {i} plays: {card}")
        if all(len(deck) >= played_card for played_card, deck in zip(played_cards, decks)):
            print("Playing a sub-game to determine the winner...\n")
            winner, _ = recursive_combat([deck[:card] for card, deck in zip(played_cards, decks)])
            print(f"...anyway, back to game {game}.")
        else:
            winner = 1 if played_cards[0] > played_cards[1] else 2
        print(f"Player {winner} wins round {round_} of game {game}!\n")
        if winner == 1:
            decks[0].extend(played_cards)
        else:
            decks[1].extend(played_cards[::-1])
        if any(len(deck) == 0 for deck in decks):
            break
    print(f"The winner of game {game} is Player {winner}!\n")
    return winner, decks


winner, decks = recursive_combat(initial_decks)
print("== Post-game results ==")
print_decks(decks)
print(score(decks[winner - 1]))
