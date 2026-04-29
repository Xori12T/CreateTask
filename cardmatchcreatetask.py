#imports modules
import turtle
import random

#initializes game interface
screen = turtle.Screen()

#changes screen size to match with device's screen size
displaywidth = screen.cv.winfo_screenwidth()
displayheight = screen.cv.winfo_screenheight()
screen.setup(displaywidth*0.45,displayheight*0.9)

#more screen configuration
screen.bgcolor("#B9CBD9")
#initializes extra turtles for game interface
writer = turtle.Turtle()
alert = turtle.Turtle()
writer.hideturtle()
alert.hideturtle()
alert.speed(0)
alert.pensize(20)
writer.up()
alert.up()
writer.speed(0)
#writer turtle writes game instructions
writer.goto(0,270)
writer.write("Match!", align="center", font=("Arial", 100, "normal"))
writer.goto(0,-390)
writer.write("Click on each card to reveal its color.\nMatch all cards in the least turns possible!", align="center", font=("Arial", 25, "normal"))

#makes and shuffles the color list for the cards
collist = ["cyan", "blue", "green", "red", "yellow", "purple", "orange", "chartreuse"]
random.shuffle(collist)
#positions that each card goes to
poslist = [(-225, 200), (-75, 200), (75, 200), (225,200),
           (-225, 50), (-75, 50), (75, 50), (225, 50),
           (-225, -100), (-75, -100), (75, -100), (225,-100),
           (-225, -250), (-75, -250), (75, -250), (225,-250)]

#initializes variables
first = None
second = None
firstcard = None
secondcard = None
locked = False
count = 1
turns = 0

#user defined function for pop up text
def notice(txt, align=35, t=1000):
    fs = 50
    alert.up()
    alert.goto(-275, 100)
    alert.seth(0)
    alert.down()
    alert.color("black","white")
    alert.begin_fill()
    for x in range(2):
        alert.forward(550)
        alert.right(90)
        alert.forward(200)
        alert.right(90)
    alert.up()
    alert.end_fill()
    alert.goto(0,-align)
    if len(txt) > 35:
        fs = 35
    alert.write(txt, align="center", font=("Arial", fs, "normal"))
    screen.ontimer(noterase, t)

#very small function to clear the pop up after a time with ontimer and doesn't stop the program's runtime
def noterase():
    alert.clear()
    
#small function to compare two clicked cards
def check(f, s):
    return f == s

#more actually ran code, asks for difficulty at start of the game
difficulty = screen.textinput("Difficulty", "1 for easy, 2 for normal, 3 for hard, default to easy.")
if difficulty == "3":
    difficulty = 16
elif difficulty == "2":
    difficulty = 12
else:
    difficulty = 8

#real mechanics of the game
#keeps track of what card was clicked, checks, basically runs the game
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
                print("Card clicked: " + color + ". ")
                card.color("black", color)
            else:
                #checks if the second card isn't the first card
                if card != firstcard:
                    locked = True
                    second = color
                    secondcard = card
                    count = 1
                    print("Card clicked: " + color + ". ")
                    card.color("black", color)
                    #compares the cards
                    if check(first, second):
                        print("Thats a match!")
                        firstcard.solved = True
                        secondcard.solved = True
                        notice("That's a match!")
                        #no program stall timed function call, replace time.sleep
                        screen.ontimer(reset, 1050)
                    else:
                        print("That's not a match...")
                        notice("That's not\na match...", 75)
                        screen.ontimer(reset, 1050)

#more setup function, creates the list of colors for the cards
def generate_cards(l, d):
    d = int(d)
    if d % 2 == 0:
        l2 = l[:]
        nl = []
        c = 0
        for x in range(int(d/2)):
            c = random.randint(0,len(l2)-1)
            nl.append(l2[c])
            nl.append(l2[c])
            l2.pop(c)
        for x in range(random.randint(1,5)):
            random.shuffle(nl)
        return nl
    else:
        print("d has to be an even number")
        return

#debug function
def showall():
    global cards, turns
    turns += 100
    for x in cards:
        x.fillcolor(x.revealcolor)
        x.solved = True

#function that runs after each round to make sure all non-solved cards are reset, and checks for win condition
def reset():
    global cards, firstcard, secondcard, turns, difficulty, locked
    firstcard = None
    secondcard = None
    diff = ""
    for x in cards:
        if not x.solved:
            x.fillcolor("white") 
    
    if difficulty == 8:
        diff = "easy"
    elif difficulty == 12:
        diff = "normal"
    else:
        diff = "hard"

    locked = False

    if donecheck():
        print("You win!")
        notice("You win!")
        screen.ontimer(lambda: notice(f"It took you {turns} turns\nto win in {diff} mode!", 50), 1500, 3000)
        print(f"It took you {turns} turns to win in {diff} mode!")
        screen.ontimer(turtle.bye, 4000)
    
#checks win condition, iterates through list
def donecheck():
    global cards
    isdone = True
    for x in cards:
        if not x.solved:
            isdone = False
    return isdone

#calls generate_cards function to setup game
cardcollist = generate_cards(collist, difficulty)

#set up cards, each card is an individual turtle
cards = []
for x in range(difficulty):
    cd = turtle.Turtle()
    cd.shape("square")
    cd.shapesize(5, 4)
    cd.color("black", "white")
    #revealcolor is a custom attribute that stores its color
    cd.revealcolor = cardcollist[x]
    cd.solved = False
    cd.speed(0)
    cd.up()
    cd.goto(poslist[x][0], poslist[x][1])
    #sets up what each turtle does when clicked, runs the game. x, y is unneeded, but onclick still needs to recieve them
    #c = cd returns what card is clicked, and col stores what color its supposed to be
    #then, it calls the on_card_click function.
    #lambda is a small unnamed function that onclick needs, it passes values to and from the onclick to the on_card_click function
    cd.onclick(lambda x, y, c=cd, col = cd.revealcolor: on_card_click(c, col))
    cards.append(cd)

#debug keyboard shortcuts
screen.onkeypress(showall, "s")
screen.onkeypress(reset, "r")
screen.listen()

#runs the tk mainloop
turtle.mainloop()
