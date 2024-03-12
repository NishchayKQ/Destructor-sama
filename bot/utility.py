from math import sqrt, floor, ceil
from time import time
from typing import Callable, Union

from data import levels


def performance(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        if t2 - t1 > 0.001:
            print(f"{func.__name__} took {(t2 - t1)}s")
        return result

    return wrapper


@performance
def convert_sec_to_day(n: int) -> str:
    n = floor(n)
    day = n // (24 * 3600)
    n = n % (24 * 3600)
    hour = n // 3600
    n %= 3600
    minutes = n // 60
    n %= 60
    seconds = n
    formatted_str = (
        f"{f'{day} days ' if day else ''}{f'{hour} hours ' if hour else ''}"
        f"{f'{minutes} minutes ' if minutes else ''}"
        f"{'' if (not day and not hour and not minutes) or (not seconds) else 'and '}"
        f"{f'{seconds} seconds' if seconds else ''}"
    )
    return formatted_str


@performance
def getLevel(xp: int) -> tuple[int, int]:
    if xp <= 34:  # for level 0 no formula
        return 0, 35
    else:
        calcu = 1 + (sqrt(5 * (xp - 35))) / 10
        x = ceil(calcu)
        try:
            y = levels[x]
        except KeyError:
            y = (20 * (x * x)) - (40 * x) + 55
            levels[x] = y

        return floor(calcu), y


@performance
def amPamConverter(received: Union[str, list], mode: int = 1) -> Union[str, list]:
    if mode == 1:  # Received is string here
        H, m = received.split()
        H = int(H)
        if H > 12:
            H = H - 12
            amPam = "pm"
        else:
            amPam = "am"
        return f"{H}:{m} {amPam}"
    if mode == 2:  # Received is like ["19 00 - 19 40\n" , "20 00 - 21 00\n" ]
        culturedList = []
        for amoeba in received:
            am1 = "am"
            am2 = "am"
            nLessAmoeba = amoeba[:-1]
            init_timestamp, final_timeStamp = nLessAmoeba.split(" - ")
            # h1,m1,am1          h2 m2,am2
            h1, m1 = init_timestamp.split()
            h2, m2 = final_timeStamp.split()
            h1 = int(h1)
            h2 = int(h2)
            if h1 > 12:
                h1 = h1 - 12
                am1 = "pm"
            if h2 > 12:
                h2 = h2 - 12
                am2 = "pm"
            culturedList.append(f"{h1}:{m1} {am1} - {h2}:{m2} {am2}\n")
        return culturedList
