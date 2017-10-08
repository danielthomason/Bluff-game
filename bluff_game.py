import random
import sys
import num2words
from time import sleep

'''
Bluff game has players start with X dice
First player makes a bid of how many of a given number is on the table
Then second player must either increase bid (+ die face same number or just + number any die face)
or call 'bluff'
Call of bluff means all dice are revealed
If there are fewer dice on the table than bid, then bidding player loses one die
If there are equal to or greater than number of dice bid, calling player loses one die
Whichever player was correct starts next round
First player to reach zero dice loses


'''

# Put some pauses in to make it less jarring
# Make computer logic better
# Make GUI


computer_think_time = 4     # (number of quarter-seconds computer should think)

# To do: set up game initial state
def whoGoesFirst():
    if random.randint(0,1) == 0:
        return 'computer'
    else:
        return 'player'

def rollDice(diceCount):
    new_dice = []
    for i in range(diceCount):
        new_dice.append(random.randint(1,6))
    return new_dice

def isLegalBid(newBid,oldBid,totalDiceCount):
    # newBid and oldBid should be lists of the form (die face, number of dice, # dice left for player)
    if (newBid[1] < 1) or (newBid[1] > totalDiceCount) or (newBid[0] < 1) or (newBid[0] > 6):
        return False
    elif newBid[1] < oldBid[1]:
        return False
    elif newBid[1] == oldBid[1] and (newBid[0] <= oldBid[0]):
        return False
    else:
        return True

def checkBidWins(bid,biddingPlayerDice,callingPlayerDice):
    # bid should be a list of the form (die face, number of dice)
    count = 0
    count += biddingPlayerDice.count(bid[0])
    count += callingPlayerDice.count(bid[0])
    if count >= bid[1]:
        return True
    else:
        return False

def playAgain():
    print("Do you want to play again? (yes or no)")
    return raw_input().lower().startswith("y")

def computerThinking():
    print "Computer thinking",
    for wait in range(computer_think_time):
        sleep(0.35)
        print ".",
        sys.stdout.flush()

def currentState(visibleDice,hiddenDice):
    print "Your dice:       ",
    for die in range(len(visibleDice)):
        print("[{0}]".format(visibleDice[die])),
    print
    print "Opponent's dice: ",
    for die in range(len(hiddenDice)):
        print("[X]"),
    print("")

def revealDice(playersDice,computersDice):
    print
    print "Your dice:",
    for die in range(len(playersDice)):
        print(playersDice[die]),
    print
    print "Opponent's dice: ",
    for die in range(len(computersDice)):
        print(computersDice[die]),
    print("")

def makeBid(oldBid,player1DiceCount,player2DiceCount):
    legalBid = False
    totalDiceCount = player1DiceCount + player2DiceCount
    counter = 0
    while legalBid == False:
        if counter > 0:
            print
            print("That's not a legal bid, sorry - try again!")
            print
        bid = []
        while True:
            try:
                bid.append(int(raw_input("What die face would you like to bid? ")))
            except ValueError:
                print("That's not a number! Try again")
                print
            else:
                break
        while True:
            try:
                bid.append(int(raw_input("How many %ds would you like to bid? " % bid[0])))
            except ValueError:
                print("That's not a number! Try again")
                print
            else:
                break
        legalBid = isLegalBid(bid,oldBid,totalDiceCount)
        counter += 1
    print
    print("You bid that there are %d %ds in total" % (bid[1],bid[0]))
    print
    return bid

def bidOrCallLogic(computerDice,humanDiceCount,currentBid,humanBidHistory):
    if len(computerDice) + humanDiceCount == currentBid[1]:
        return "call"
    else:
        return "bid"

def computerBid(computerDice,humanDiceCount,currentBid,humanBidHistory):
    newBid = [0,0]
    if currentBid[0] == 6:
        newBid = (1,currentBid[1]+1)
    elif currentBid[1] == 0:
        newBid = (currentBid[0]+1,1)
    else:
        newBid = (currentBid[0]+1,currentBid[1])
    return newBid

#####

print
print "Welcome to Bluff!"

while True:
    humanDice = []
    computerDice = []
    print

    while True:
        try:
            gameDiceCount = int(raw_input("How many dice should we play with? "))
        except ValueError:
            print
            print "That's not a number of dice we can play with!"
            print "Try again"
            print
        else:
            print
            break

    humanDiceCount = gameDiceCount
    computerDiceCount = gameDiceCount

    turn = whoGoesFirst()
    print("The %s will go first." % turn)

    while True:
        if humanDiceCount == 0:
            print "That was your last die!"
            print "You lost the game :("
            print
            break
        elif computerDiceCount == 0:
            print "That was the computer's last die!"
            print "You won the game :)"
            print
            break

        print raw_input("Let's roll! ")
        humanDice = rollDice(humanDiceCount)
        computerDice = rollDice(computerDiceCount)

        currentState(humanDice,computerDice)
        print

        previousHumanBids = []
        bid = [0,0]

        while True:
            oldBid = bid
            if turn == "player":
                while True:
                    print
                    bid_or_call = raw_input("Would you like to bid or call? ").lower()
                    if bid_or_call == "quit":
                        print('Thanks for playing!')
                        sys.exit() # terminate the program
                    elif (bid_or_call == "call") and oldBid == [0,0]:
                        print
                        print("But you are the first to bid this turn!")
                        print("That means you'll have to bid.")
                        print
                        bid_or_call = "bid"
                        break
                    elif (bid_or_call == "bid") or (bid_or_call == "call"):
                        break
                    else:
                        print("You must choose either 'bid' or 'call'!")
                        print
                if bid_or_call == "bid":
                    print
                    bid = makeBid(oldBid,humanDiceCount,computerDiceCount)
                    turn = "computer"
                else:
                    revealDice(humanDice,computerDice)
                    if checkBidWins(bid,computerDice,humanDice):
                        print
                        print "The computer's bid was correct!"
                        print "You lose a die :("
                        print
                        humanDiceCount -= 1
                        turn = "computer"
                    else:
                        print
                        print "The computer's bid was too high!"
                        print "The computer loses a die :D"
                        print
                        computerDiceCount -= 1
                        turn = "player"
                    break
            else:
                computerThinking()
                print
                print
                bid_or_call = bidOrCallLogic(computerDice,humanDiceCount,bid,previousHumanBids)
                if bid_or_call == "bid":
                    bid = computerBid(computerDice,humanDiceCount,bid,previousHumanBids)
                    print("The computer bids that there are %d %ds in total" % (bid[1],bid[0]))
                    turn = "player"
                else:
                    print("The computer wants to call your bluff!")
                    print
                    revealDice(humanDice,computerDice)
                    if checkBidWins(bid,humanDice,computerDice):
                        print "Your bid was correct!"
                        print "The computer loses a die :D"
                        print
                        computerDiceCount -= 1
                        turn = "player"
                    else:
                        print "Your bid was too high!"
                        print "You lose a die :("
                        print
                        humanDiceCount -= 1
                        turn = "computer"
                    break



    if not playAgain():
        break
