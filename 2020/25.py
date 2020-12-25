def find_loop_size(public_key: int) -> int:
    value = 1
    loop_size = 0
    subject_number = 7
    while value != public_key:
        value = (value * subject_number) % 20201227
        loop_size += 1
    return loop_size


def transform_key(public_key: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value = (value * public_key) % 20201227
    return value


card_public_key = 335121
door_public_key = 363891
card_loop_size = find_loop_size(card_public_key)
door_loop_size = find_loop_size(door_public_key)

print(transform_key(card_public_key, door_loop_size))
print(transform_key(door_public_key, card_loop_size))  # for double-checking the result
