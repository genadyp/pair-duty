import sys
import csv
import datetime
from collections import defaultdict


USAGE = 'usage: {} <dd-mm-yyyy>'.format(__file__)

NAMES = [
    'leonid', 'misha', 'ariel', 'genady', 'alex', 'stas', 
    'igal', 'moshe', 'boris', 'ron', 'haim', 'avi', 'semion', 'igor'
]


def generate_pairs():
    pairs = []
    for idx, name in enumerate(NAMES[:-1]):
        for second_name in NAMES[idx+1:]:
            pairs.append((name, second_name))
    return pairs

def group_pairs(pairs: list) -> dict:
    groups = defaultdict(set)
    for name1, name2 in pairs:
        groups[name1].add(name2)
        groups[name2].add(name1)
    return groups


def init_ordering(queue: list, groups: dict) -> list:
    initial_order = []
    for idx, name1 in enumerate(NAMES[:-1:2]):
        name2 = NAMES[2*idx+1]
        initial_order.append((name1, name2))
        queue.append(name1)
        queue.append(name2)
        groups[name1].remove(name2)
        groups[name2].remove(name1)
    return initial_order


def update_order(queue: list, groups: dict, order: list, pair: tuple):
    order.append(pair)

    name1, name2 = pair
    queue.remove(name1)
    queue.remove(name2)
    queue.append(name1)
    queue.append(name2)

    groups[name1].remove(name2)
    groups[name2].remove(name1)


def calculate_pair(queue: list, name1: str, group: set) -> tuple:
    if not group:
        return None

    idx = queue.index(name1)
    for name2 in queue[idx+1:]:
        if name2 in group:
            return name1, name2


def calculate_next_pair(queue: list, groups: dict) -> tuple:
    next_pair = None
    next_pair_indexes = None

    for idx, name in enumerate(queue):
        if next_pair_indexes and next_pair_indexes[1] <= idx:
            break

        pair = calculate_pair(queue, name, groups[name])
        if not pair:
            continue

        second_idx = queue.index(pair[1])
        if not next_pair or next_pair_indexes[1] > second_idx:
            next_pair = pair
            next_pair_indexes = (idx, second_idx)

    return next_pair


def order_pairs(pairs: list) -> list:
    groups = group_pairs(pairs)
    queue = []

    result = init_ordering(queue, groups)
    total = len(pairs)

    while len(result) < total:
        next_pair = calculate_next_pair(queue, groups)
        update_order(queue, groups, result, next_pair)

    return result


def generate_duties(from_date: datetime.date, delta: datetime.timedelta) -> list:
    pairs = generate_pairs()
    order = order_pairs(pairs)

    result = []
    current_date = from_date
    for duty_person1, duty_person2 in order:
        result.append({
            'date': current_date,
            'duty_person1': duty_person1,
            'duty_person2': duty_person2
        })
        current_date += delta
    return result


def write(duties: list, out_file: str):
    with open(out_file, 'w', newline='') as csvfile:
        fieldnames = ['date', 'duty_person1', 'duty_person2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(duties)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        exit(1)

    from_time_str = sys.argv[1]
    from_date = datetime.datetime.strptime(from_time_str, '%d-%m-%Y').date()

    one_week = datetime.timedelta(weeks=1)

    duties = generate_duties(from_date, one_week)
    out_file = 'output.{}.csv'.format(datetime.date.today())
    write(duties, out_file)
