import re
from pathlib import Path


input_file = Path("input") / "21.txt"

pattern = re.compile(r"([^(]+)(\(contains (.+)\))?")
foods = []
with input_file.open() as f:
    for line in f:
        match = pattern.match(line)
        ingredients = set(match.group(1).strip().split())
        allergens = set(match.group(3).strip().split(", ")) if match.group(3) else set()
        foods.append((ingredients, allergens))

all_allergens = set().union(*[allergens for _, allergens in foods])
all_ingredients = set().union(*[ingredients for ingredients, _ in foods])

# Part 1
# Because each ingredient contains up to one allergens, we can map every allergen
# to one ingredient (but not vice versa). No allergen is found in two different
# ingredients, so when a food is listed to contain an allergen, we know that none
# of the ingredients not listed contain that allergen
mapping = {allergen: all_ingredients.copy() for allergen in all_allergens}
for ingredients, allergens in foods:
    ingredients_not_present = all_ingredients - ingredients
    for allergen in allergens:
        mapping[allergen] = mapping[allergen] - ingredients_not_present

unsafe_ingredients = set().union(*mapping.values())
safe_ingredients = all_ingredients - unsafe_ingredients

count = sum(len(ingredients & safe_ingredients) for ingredients, _ in foods)
print(count)

# Part 2
# Figure out which allergen goes to which ingredient by process of elimination
while any(len(x) > 1 for x in mapping.values()):
    for allergen, possible_ingredients in mapping.items():
        if len(possible_ingredients) == 1:
            [only_ingredient] = possible_ingredients
            for a in mapping:
                if a != allergen:
                    mapping[a] = mapping[a] - {only_ingredient}

print(",".join(str(*mapping[allergen]) for allergen in sorted(all_allergens)))
