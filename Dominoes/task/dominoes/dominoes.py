import random

# generate the full domino set
domino_set = []
for d1 in range(7):
    for d2 in range(d1, 7):
        domino_set.append([d1, d2])

# split the domino set to 3 parts by random
reshuffle = True
while reshuffle:
    random.shuffle(domino_set)
    stock = domino_set[0:14]
    computer = domino_set[14:21]
    player = domino_set[21:28]
#    print(domino_set)
#    print(stock)
#    print(computer)
#    print(player)

    # determine snake and first player
    for n in range(7, 0, -1):
        if [n, n] in computer:
            computer.remove([n, n])
            snake = [[n, n]]
            status = "player"
            reshuffle = False
            break
        elif [n, n] in player:
            player.remove([n, n])
            snake = [[n, n]]
            status = "computer"
            reshuffle = False
            break
        else:
            reshuffle = True
# print(f"Stock pieces: {stock}")
# print(f"Computer pieces: {computer}")
print("=" * 70)
print(f"Stock size: {len(stock)}")
print(f"Computer pieces: {len(computer)}")
print()
print(snake[0])
print()
print("Your pieces:")
n = 1
for piece in player:
    print(f"{n}:{piece}")
    n += 1
print()
if status == "player":
    print("Status: It's your turn to make a move. Enter your command.")
elif status == "computer":
    print("Status: Computer is about to make a move. Press Enter to continue...")
