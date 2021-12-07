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
# play the game
game_result = ""
game_continue = True
stock_empty = False
domino_num = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}


# define a function for checking game end
def check_end():
    snake_n = [x for group in snake for x in group]
    global game_result
    global game_continue
    if len(player) == 0:
        game_result = "You won!"
        game_continue = False
    elif len(computer) == 0:
        game_result = "The computer won!"
        game_continue = False
    elif snake[0][0] == snake[-1][-1] and snake_n.count(snake[0][0]) == 8:
        game_result = "It's a draw!"
        game_continue = False
    elif stock_empty:
        game_result = "It's a draw!"
        game_continue = False
    else:
        game_continue = True


def make_move(part, part_move):
    global move_illegal
    global stock_empty
    if int(part_move) > 0:
        if snake[-1][-1] == part[int(part_move) - 1][0]:
            snake.append(part.pop(int(part_move) - 1))
            move_illegal = False
        elif snake[-1][-1] == part[int(part_move) - 1][1]:
            x = part[int(part_move) - 1][1]
            part[int(part_move) - 1][1] = part[int(part_move) - 1][0]
            part[int(part_move) - 1][0] = x
            snake.append(part.pop(int(part_move) - 1))
            move_illegal = False
        else:
            move_illegal = True
    elif int(part_move) < 0:
        if snake[0][0] == part[-int(part_move) - 1][1]:
            snake.insert(0, part.pop(-int(part_move) - 1))
            move_illegal = False
        elif snake[0][0] == part[-int(part_move) - 1][0]:
            x = part[-int(part_move) - 1][1]
            part[-int(part_move) - 1][1] = part[-int(part_move) - 1][0]
            part[-int(part_move) - 1][0] = x
            snake.insert(0, part.pop(-int(part_move) - 1))
            move_illegal = False
        else:
            move_illegal = True
    elif int(part_move) == 0:
        if len(stock) == 0:
            stock_empty = True
        else:
            part.append(stock.pop(random.randint(0, len(stock) - 1)))
        move_illegal = False


def check_match(part, dp):
    global match
    if snake[-1][-1] == dp[0]:
        snake.append(dp)
        part.remove(dp)
        match = True
    elif snake[-1][-1] == dp[1]:
        x = dp[1]
        dp[1] = dp[0]
        dp[0] = x
        snake.append(dp)
        part.remove(dp)
        match = True
    elif snake[0][0] == dp[1]:
        snake.insert(0, dp)
        part.remove(dp)
        match = True
    elif snake[0][0] == dp[0]:
        x = dp[1]
        dp[1] = dp[0]
        dp[0] = x
        snake.insert(0, dp)
        part.remove(dp)
        match = True
    else:
        match = False


def ai(parts):
    part = [x for group in parts for x in group]
    snake_n = [x for group in snake for x in group]
    domino_num[0] = part.count(0) + snake_n.count(0)
    domino_num[1] = part.count(1) + snake_n.count(1)
    domino_num[2] = part.count(2) + snake_n.count(2)
    domino_num[3] = part.count(3) + snake_n.count(3)
    domino_num[4] = part.count(4) + snake_n.count(4)
    domino_num[5] = part.count(5) + snake_n.count(5)
    domino_num[6] = part.count(6) + snake_n.count(6)
#    print(domino_num)
    scores = {}
    for dp in parts:
        scores[str(dp)] = domino_num[dp[0]] + domino_num[dp[1]]
#    print(scores)
    global match
    match = False
    for i in range(14, -1, -1):
        for dp in parts:
            if scores[str(dp)] == i:
                check_match(parts, dp)
            if match:
                break
        if match:
            break
    if not match:
        if len(stock) == 0:
            global stock_empty
            stock_empty = True
        else:
            parts.append(stock.pop(random.randint(0, len(stock) - 1)))


while game_continue:
    print("=" * 70)
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}")
    print()
    if len(snake) <= 6:
        print(*snake, sep="")
    else:
        print(f"{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}")
    print()
    print("Your pieces:")
    n = 1
    for piece in player:
        print(f"{n}:{piece}")
        n += 1
    print()
    check_end()
    if game_continue:
        if status == "player":
            print("Status: It's your turn to make a move. Enter your command.")
            input_invalid = True
            move_illegal = True
            while move_illegal:
                input_invalid = True
                while input_invalid:
                    player_move = input()
                    try:
                        int(player_move)
                    except:
                        print("Invalid input. Please try again.")
                    else:
                        if -len(player) <= int(player_move) <= len(player):
                            input_invalid = False
                            break
                        else:
                            print("Invalid input. Please try again.")

                make_move(player, player_move)
                if move_illegal:
                    print("Illegal move. Please try again.")
            status = "computer"
        elif status == "computer":
            input("Status: Computer is about to make a move. Press Enter to continue...")
            match = False
            ai(computer)
            status = "player"
    else:
        print(f"Status: The game is over. {game_result}")
