# fuck this

long_string = """

SURVEY

TRACK

LIGHT

PLAYGROUND

TIMER

WATCH

DESERT

SUEDE

BAKE

PULP

MONITOR

BLUR

HOURGLASS

BEACH

BROIL

OASIS"""

words = long_string.split()

print(words)

nothings = """
"""


trios = """
"""

groups = """79BF
"""

NOTHING_RULES = nothings.splitlines()
TRIO_RULES = trios.splitlines()
GROUP_RULES = groups.splitlines()


# lists must be sorted
def elements_in_common(l1, l2):
    if not l1 or not l2:
        return 0
    if l1[0] == l2[0]:
        return 1 + elements_in_common(l1[1:], l2[1:])
    if l1[0] < l2[0]:
        return elements_in_common(l1[1:], l2)
    return elements_in_common(l1, l2[1:])


def apply_nothing_rule(rule, guess):
    return elements_in_common(rule, guess) < 3


def apply_trio_rule(rule, guess):
    return elements_in_common(rule, guess) not in [2, 4]


def apply_group_rule(rule, guess):
    return elements_in_common(rule, guess) == 0


def apply_all_rules(nothing_rules, trio_rules, group_rules, guess):
    for rule in group_rules:
        if not apply_group_rule(rule, guess):
            print(f"{guess} fails on group rule {rule}")
            return False
    for rule in nothing_rules:
        if not apply_nothing_rule(rule, guess):
            print(f"{guess} fails on nothing rule {rule}")
            return False
    for rule in trio_rules:
        if not apply_trio_rule(rule, guess):
            print(f"{guess} fails on trio rule {rule}")
            return False
    return True


def try_guess(guess):
    return apply_all_rules(NOTHING_RULES, TRIO_RULES, GROUP_RULES, guess)


def all_possible_guesses():
    for first_value in range(16):
        for second_value in range(first_value + 1, 16):
            for third_value in range(second_value + 1, 16):
                for fourth_value in range(third_value + 1, 16):
                    yield (
                        "".join(
                            list(
                                map(
                                    lambda val: hex(val)[2],
                                    [
                                        first_value,
                                        second_value,
                                        third_value,
                                        fourth_value,
                                    ],
                                )
                            )
                        ).upper()
                    )


def words_for_guess(guess):
    output = []
    for hex_digit in guess:
        output.append(words[int(hex_digit, 16)])
    return output


def valid_guesses_left(nothing_rules, trio_rules, group_rules):
    output = []
    for guess in all_possible_guesses():
        if apply_all_rules(nothing_rules, trio_rules, group_rules, guess):
            # print(f"{guess} seems good: {words_for_guess(guess)}")
            output.append(guess)
    return output


def worst_case_from_guess(nothing_rules, trio_rules, group_rules, guess):
    if_its_nothing = len(
        valid_guesses_left(nothing_rules + [guess], trio_rules, group_rules)
    )
    if_its_a_trio = len(
        valid_guesses_left(nothing_rules, trio_rules + [guess], group_rules)
    )
    if_its_a_group = len(
        valid_guesses_left(nothing_rules, trio_rules, group_rules + [guess])
    )
    possibilities = [if_its_nothing, if_its_a_trio, if_its_a_group]
    print(f"Possibilities after guessing {guess}: {possibilities}")
    if not if_its_a_group:
        return 99999999
    return max(possibilities)


for i in range(16):
    print(f"word {i} is {words[i]}")
best_guess = None
best_number = 9999999999

candidates = valid_guesses_left(NOTHING_RULES, TRIO_RULES, GROUP_RULES)
print(f"There are {len(candidates)} valid guesses left.")
for guess in candidates:
    worst_case = worst_case_from_guess(NOTHING_RULES, TRIO_RULES, GROUP_RULES, guess)
    if worst_case < best_number:
        best_guess = guess
        best_number = worst_case
print(f"I recommend guessing {best_guess}: {words_for_guess(best_guess)}")
