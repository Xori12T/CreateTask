import turtle
import random
from time import sleep as s

screen = turtle.Screen()
canvas = screen.getcanvas()
screen.bgcolor("#B9CBD9")
writer = turtle.Turtle()
writer.hideturtle()
writer.up()
writer.speed(0)
writer.goto(0,250)
writer.write("Match!", ("Arial", 255, "bold"))
collist = ["cyan", "blue", "green", "red", "yellow", "purple", "orange", "chartreuse"]
random.shuffle(collist)
poslist = [(-300, 150), (-100, 150), (100, 150), (300,150),
           (-300, 0), (-100, 0), (100, 0), (300, 0),
           (-300, -150), (-100, -150), (100, -150), (300,-150),
           (-300, -300), (-100, -300), (100, -300), (300,-300)]

difficulty = screen.textinput("Difficulty", "1 for easy, 2 for medium, 3 for hard, default to easy.")
if difficulty == "3":
    difficulty = 16
elif difficulty == "2":
    difficulty = 12
else:
    difficulty = 8

def on_card_click(card, color):
    print("Card clicked: " + color + ", " + str(card))

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

cardcollist = generate_cards(collist, difficulty)

cards = []
for x in range(difficulty):
    cd = turtle.Turtle()
    cd.shape("square")
    cd.shapesize(5, 4)
    cd.color("black", cardcollist[x])
    cd.speed(0)
    cd.up()
    cd.goto(poslist[x][0], poslist[x][1])
    #cd.onclick(on_card_click)
    cd.onclick(lambda x, y, c=cd, col=cd.fillcolor(): on_card_click(c, col))
    cards.append(cd)

turtle.mainloop()