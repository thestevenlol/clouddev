import random

suits = ["clubs", "diamonds", "hearts", "spades"]
cards = [
    "Ace",
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        "Jack",
        "Queen",
        "King"
]

matches = 0
last = None
current = None
for _ in range(500):
    suit = random.randint(0, 3)
    card = random.randint(0, 12)

    last = current
    current = f"{cards[card]} of {suits[suit]}"

    if last == current:
        matches = matches + 1

print(f"Matches: {matches}")