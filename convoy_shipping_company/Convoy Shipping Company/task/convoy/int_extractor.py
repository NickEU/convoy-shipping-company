import re

regex_look_for_integers = r"\d+"
pattern = re.compile(regex_look_for_integers)


def extract_int(to_sanitize, counter):
    matches = pattern.findall(str(to_sanitize))
    if str(matches[0]) != str(to_sanitize):
        counter.checked += 1
    return to_sanitize if not matches else matches[0]
