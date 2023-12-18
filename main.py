import random
import tkinter as tk
import ttkbootstrap as tkb
from PIL import Image, ImageTk


class DeckOfCards:
    cards = []
    cardImages = []
    cardValues = {}  
    
    def __init__(self):
        pass

    def generateDeck(self):
        suits = ["clubs", "diamonds", "hearts", "spades"]
        cardValues = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
        for card in cardValues:
            for suit in suits:
                card_name = f"{card}_of_{suit}"
                self.cards.append(card_name)
                self.cardValues[card_name] = self.getCardValue(card)

    def getCardValue(self, card):
        if card.isdigit():
            return int(card)
        elif card in ['j', 'q', 'k']:
            return 10
        else:
            return 11
    
    def calculateHandTotalFromFrame(self, frame):
        total = 0
        aceCount = 0 
        
        for label in frame.winfo_children():
            cardName = label.card_name 
            cardValue = self.cardValues.get(cardName, 0)
            
            if cardValue == 11:
                aceCount += 1
            total += cardValue
        
        while total > 21 and aceCount > 0:
            total -= 10 
            aceCount -= 1
        
        return total


    def generateCardImage(self, HandFrame, card):
        image = Image.open(f"cards/{card}.png")
        image = image.resize((250, 363))
        cardImage = ImageTk.PhotoImage(image)
        self.cardImages.append(cardImage)
        label = tkb.Label(HandFrame, image=cardImage)
        label.card_name = card  
        label.pack(side="left")


    def dealCard(self):
        return self.cards.pop()

    def shuffleDeck(self):
        random.shuffle(self.cards)

    def checkDeck(self):
        if len(self.cards) >= 10:
            self.generateDeck()
            self.shuffleDeck()

      


def main():
    game = tkb.Window(title="Blackjack", themename="solar")
    
    game.iconbitmap("icon/icon.ico")
    game.geometry("1920x1080")
    tkb.Style().configure('TButton', font= '-size 20')
    tkb.Style().configure('TLabel',font= "-size 20")

    #TITLE
    title = tkb.Label(game, bootstyle="primary",text=" Blackjack")
    title.pack(side="top")
    tkb.Style().configure("title.TLabel", font="-size 30")

    #TOP FRAME 
    TopFrame = tkb.Frame(game)  
    TopFrame.pack(side="top")

    #Dealer Frames
    dealerLabelFrame = tkb.LabelFrame(TopFrame, bootstyle="primary",text="Dealers Cards")
    dealerLabelFrame.pack(side="top", pady=20)
    dealerLabelFrame.configure('style',font='20')

    dealerHandFrame = tkb.Frame(dealerLabelFrame)
    dealerHandFrame.pack(side="top")
    #Dealer Frame End
    #TOP FRAME END

    #MIDDLE FRAME 
    MiddleFrame = tkb.Frame(game)
    MiddleFrame.pack(side="top",anchor="w", fill="x")

    #Hand Value Frames
    dealerHandTotalLabelFrame = tkb.LabelFrame(MiddleFrame,bootstyle="primary",text="Dealer Total:")
    dealerHandTotalLabelFrame.pack(side="top", anchor="n")

    PlayerHandTotalLabelFrame = tkb.LabelFrame(MiddleFrame,bootstyle="primary",text="player Total:")
    PlayerHandTotalLabelFrame.pack(side="top", anchor="s")

    dealerTotalLabel = tkb.Label(dealerHandTotalLabelFrame,bootstyle="primary",text="  ")
    dealerTotalLabel.pack(side="top")

    playerTotalLabel= tkb.Label(PlayerHandTotalLabelFrame, bootstyle="primary",text="  ")
    playerTotalLabel.pack(side="top")
    #Hand Value End

    #Button Frames
    buttonFrame = tkb.Frame(MiddleFrame)
    buttonFrame.pack(side="right", padx=10,pady=10)


   

    


    #Button Frame End
    #MIDDLE FRAME END

    #BOTTOM FRAME
    BottomFrame = tkb.Frame(game)
    BottomFrame.pack(side="bottom")
    #Player Frames
    playerLabelFrame= tkb.LabelFrame(BottomFrame,bootstyle="primary",text="Your Hand")
    playerLabelFrame.pack(side="bottom")

    playerHandFrame = tkb.Frame(playerLabelFrame,bootstyle="primary")
    playerHandFrame.pack(side="bottom")
    #Player Frame End
    #BOTTOM FRAME END
    #Quit Button
    
    def quitGame():
        game.quit()

    quitButton = tkb.Button(game, bootstyle="danger", text="QUIT GAME", command=quitGame)
    quitButton.pack(side="bottom", anchor="e",padx=15)

    def winCondition(dealerPoints,playerPoints):
        msg = "\n\nClick OK to play another hand."
        if playerPoints > 21:
            return "Dealer wins! Player busts." + msg
        elif dealerPoints > 21:
            return "Player wins! Dealer busts."+ msg
        elif playerPoints == dealerPoints:
            return "It's a tie!"+ msg
        elif playerPoints > dealerPoints:
            return "Player wins!"+ msg
        else:
            return "Dealer wins!"+ msg

    deck = DeckOfCards()
    deck.generateDeck()
    deck.shuffleDeck()

    def updateTotalLabel(frame, label):
        total = deck.calculateHandTotalFromFrame(frame)
        label.config(text=f"Total: {total}")

    def dealToPlayer():
        deck.generateCardImage(playerHandFrame,deck.dealCard())
        updateTotalLabel(playerHandFrame,playerTotalLabel)
        if deck.calculateHandTotalFromFrame(playerHandFrame) > 21:
            dealersTurn()

    hitButton = tkb.Button(buttonFrame,bootstyle="primary",text="HIT", command=dealToPlayer)
    hitButton.pack(side="left")
    
    def dealToDealer():
        deck.generateCardImage(dealerHandFrame,deck.dealCard())
        updateTotalLabel(dealerHandFrame,dealerTotalLabel)
   
    def dealersTurn():
        
        dealerPoints = deck.calculateHandTotalFromFrame(dealerHandFrame)
        playerPoints = deck.calculateHandTotalFromFrame(playerHandFrame)
        
        while deck.calculateHandTotalFromFrame(dealerHandFrame) < 17:
            dealToDealer()
        modal = tkb.dialogs.MessageDialog(winCondition(dealerPoints, playerPoints), buttons=['OK'], command=(resetGame), icon="icon\icon.ico") 
       
        modal.show(position=[1000,200])


    stayButton = tkb.Button(buttonFrame, bootstyle="primary", text="STAY", command=dealersTurn)
    stayButton.pack(side="left", padx=10)
    
    def resetGame():

        for widget in playerHandFrame.winfo_children():
            widget.destroy()
        for widget in dealerHandFrame.winfo_children():
            widget.destroy()

        playerTotalLabel.config(text="  ")
        dealerTotalLabel.config(text="  ")

        deck.checkDeck()

        for i in range(2):
            dealToDealer()
            dealToPlayer()

    for i in range(2):
        dealToDealer()
        dealToPlayer()
    playAgainButton = tkb.Button(MiddleFrame, bootstyle="info", text="Reset Game", command=resetGame)
    playAgainButton.pack(side="bottom", anchor="w", padx=15)

    game.mainloop()
if __name__ == "__main__":
    main()


