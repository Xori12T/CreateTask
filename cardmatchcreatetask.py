import turtle
import random
from time import sleep as s

screen = turtle.Screen()
screen.setup(400,300)
screen.bgcolor("#B9CBD9")
writer = turtle.Turtle()
writer.hideturtle()
writer.up()
writer.speed(0)
writer.goto(0,270)
writer.write("Match!", align="center", font=("Arial", 100, "normal"))
writer.goto(0,-375)
writer.write("Click on each black card to reveal its color.\nTry to match all the cards!", align="center", font=("Arial", 25, "normal"))
collist = ["cyan", "blue", "green", "red", "yellow", "purple", "orange", "chartreuse"]
random.shuffle(collist)
poslist = [(-225, 200), (-75, 200), (75, 200), (225,200),
           (-225, 50), (-75, 50), (75, 50), (225, 50),
           (-225, -100), (-75, -100), (75, -100), (225,-100),
           (-225, -250), (-75, -250), (75, -250), (225,-250)]

first = None
second = None
firstcard = None
secondcard = None
locked = False
count = 1
turns = 0

def check(f, s):
    return f == s

difficulty = screen.textinput("Difficulty", "1 for easy, 2 for normal, 3 for hard, default to easy.")
if difficulty == "3":
    difficulty = 16
elif difficulty == "2":
    difficulty = 12
else:
    difficulty = 8

def on_card_click(card, color):
    global count, first, second, turns, firstcard, secondcard, locked
    if not locked:
        if not card.solved:
            if count == 1:
                first = color
                firstcard = card
                count = 2
                turns += 1
                print(f"------------- Turn {turns} -------------")
                print("Card clicked: " + color + ", " + str(card))
                card.color("black", color)
            else:
                if card != firstcard:
                    locked = True
                    second = color
                    secondcard = card
                    count = 1
                    print("Card clicked: " + color + ", " + str(card))
                    card.color("black", color)
                    # screen.ontimer(lambda: card.color("black", "black"), 2000)
                    if check(first, second):
                        print("Thats a match!")
                        firstcard.solved = True
                        secondcard.solved = True
                        screen.ontimer(reset, 2000)
                    else:
                        print("Oh noo...")
                        screen.ontimer(reset, 2000)




def generate_cards(l, d):
    l2 = l[:]
    nl = []
    c = 0
    for x in range(int(d/2)):
        c = random.randint(0,len(l2)-1)
        nl.append(l2[c])
        nl.append(l2[c])
        l2.pop(c)
    random.shuffle(nl)
    return nl

def showall():
    global cards
    for x in cards:
        x.fillcolor(x.revealcolor)

def reset():
    global cards, firstcard, secondcard, turns, difficulty, locked
    firstcard = None
    secondcard = None
    diff = ""
    for x in cards:
        if not x.solved:
            x.fillcolor("black") 
    
    if difficulty == 8:
        diff = "easy"
    elif difficulty == 12:
        diff = "medium"
    else:
        diff = "hard"

    locked = False

    if donecheck():
        print("You win!")
        print(f"It took you {turns} turns to win in {diff} mode!")
        turtle.bye()
    

def donecheck():
    global cards
    isdone = True
    for x in cards:
        if not x.solved:
            isdone = False
    return isdone

cardcollist = generate_cards(collist, difficulty)

cards = []
for x in range(difficulty):
    cd = turtle.Turtle()
    cd.shape("square")
    cd.shapesize(5, 4)
    cd.color("black", "black")
    cd.revealcolor = cardcollist[x]
    cd.solved = False
    cd.speed(0)
    cd.up()
    cd.goto(poslist[x][0], poslist[x][1])
    cd.onclick(lambda x, y, c=cd, col = cd.revealcolor: on_card_click(c, col))
    cards.append(cd)

screen.onkeypress(showall, "s")
screen.onkeypress(reset, "r")
screen.listen()
turtle.mainloop()