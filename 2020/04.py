from pathlib import Path
from typing import Dict, List


required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


def parse_input(input_path: Path) -> List[Dict[str, str]]:
    results = []
    current_passport = {}
    with input_path.open() as f:
        for line in f:
            entries = line.strip().split()
            if entries:
                for entry in entries:
                    key, _, value = entry.partition(":")
                    current_passport[key] = value
            else:
                # i.e. a blank line
                results.append(current_passport)
                current_passport = {}
    # The final passport may be terminated by EOL instead of a blank line
    if current_passport:
        results.append(current_passport)
    return results


def is_passport_valid(passport: Dict[str, str]) -> bool:
    return all(field in passport for field in required_fields)


def is_passport_strictly_valid(passport: Dict[str, str]) -> bool:

    if not is_passport_valid(passport):
        return False  # early return if we don't have all required fields present

    byr_valid = 1920 <= int(passport['byr']) <= 2002
    iyr_valid = 2010 <= int(passport['iyr']) <= 2020
    eyr_valid = 2020 <= int(passport['eyr']) <= 2030
    hgt = passport['hgt']
    hgt_valid = ((hgt.endswith('in') and 59 <= int(hgt.removesuffix('in')) <= 76)
                 or (hgt.endswith('cm') and 150 <= int(hgt.removesuffix('cm')) <= 193))
    hcl_valid = (passport['hcl'].startswith('#') and
                 all(character in '0123456789abcdef' for character in passport['hcl'][1:]))
    ecl_valid = passport['ecl'] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    pid_valid = len(passport['pid']) == 9 and passport['pid'].isdigit()

    return byr_valid and iyr_valid and eyr_valid and hgt_valid and hcl_valid and ecl_valid and pid_valid


# Part 1
passports = parse_input(Path("input") / "04.txt")
print(sum(is_passport_valid(passport) for passport in passports))

# Part 2
print(sum(is_passport_strictly_valid(passport) for passport in passports))
