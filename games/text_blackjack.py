import random

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        string = ""
        for card in self.deck:
            string= string + f"{str(card)}\n"
        return string

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        num=random.randint(0, len(self.deck) -1)
        card = self.deck[num]
        for nums in range (num, len(self.deck)-1):
            self.deck[num] = self.deck[num+1]
        self.deck.pop()
        return card
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + card.value
    
    def adjust_for_ace(self):
        for cards in self.cards:
            if cards.rank == 'Ace':
                while True:
                    value = int(input("enter value of this ace, 1 or 11"))
                    if value == 1 or value == 11:
                        break
                cards.value = value
                self.count_values()
                
    def count_values(self):
        self.value=0
        for cards in self.cards:
            self.value = self.value + cards.value
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total = self.total + self.bet
    
    def lose_bet(self):
        self.total = self.total - self.bet
def take_bet(Chips):
    bet = -1
    while bet<0 or bet>Chips.total:
        try:
            bet = int(input("enter a bet"))
        except:
            print("wrong input")
    return bet
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    if hand.value >21 :
        hand.adjust_for_ace()
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    action = ""
    while True:
        action = input("Do you want to hit or to stand? Type 'hit' to hit or type 'stand' to stand")
        if action == "stand":
            playing = False
            break
        elif action == "hit":
            hit(deck,hand)
            break
        else:
            print("Sorry, wrong action.")
def show_some(player,dealer):
    
    print("\n")
    print(f"dealer's card: \n{dealer.cards[1]}\n")
    print(f"player's cards: \n")
    for card in player.cards:
        print(f"{card}")
    print("\n")

    
def show_all(player,dealer):
    
    print("\n")
    print(f"dealer's cards:\n")
    for card in dealer.cards:
        print(f"{card}")
    print("\n")
    print(f"player's cards:\n")
    for card in player.cards:
        print(f"{card}")
    print("\n")
    print(f"dealer's value: {dealer.value}\n")
    print(f"player's value: {player.value}\n")
def player_busts(player, dealer, chips):
    print("player busts!")
    chips.lose_bet()

def player_wins(player,dealer, chips):
    print("player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("dealer busts!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("dealer wins!")
    chips.lose_bet()
    
def push():
    print("Tie! It's a push!")
if __name__ == '__main__':
	
	suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
	ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
	values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
	         'Queen':10, 'King':10, 'Ace':11}

	playing = True
	game=0

	while True:
	    # Print an opening statement
	    if game==0:
	        print("Welcome in the Blackjack game!\nYou have 100 starting chips.")
	    start = input("Are you ready for the game?(yes,no)")
	    if start == "yes":
	        # Create & shuffle the deck, deal two cards to each player
	        deck = Deck()
	        deck.shuffle()
	        player = Hand()
	        dealer = Hand()
	        dealer.add_card(deck.deal())
	        dealer.add_card(deck.deal())
	        player.add_card(deck.deal())
	        player.add_card(deck.deal())

	        # Set up the Player's chips
	        if(game==0):
	            player_chips = Chips()

	        # Prompt the Player for their bet
	        
	        player_chips.bet = take_bet(player_chips)

	        # Show cards (but keep one dealer card hidden)
	        
	        show_some(player, dealer)
	        
	        playing = True
	        
	        while playing:  # recall this variable from our hit_or_stand function

	            # Prompt for Player to Hit or Stand
	            hit_or_stand(deck, player)

	            # Show cards (but keep one dealer card hidden)
	            
	            show_some(player, dealer)


	            # If player's hand exceeds 21, run player_busts() and break out of loop

	            if player.value > 21:
	                player_busts(player, dealer, player_chips)
	                break

	        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
	        if player.value <= 21:
	            while dealer.value < 17:
	                hit(deck, dealer)

	            # Show all cards

	            show_all(player, dealer)

	            # Run different winning scenarios

	            if dealer.value > 21:
	                dealer_busts(player, dealer, player_chips)
	            elif player.value>dealer.value:
	                player_wins(player, dealer, player_chips)
	            elif dealer.value>player.value:
	                dealer_wins(player, dealer, player_chips)
	            else:
	                push()
	                
	        # Inform Player of their chips total 

	        print(f"Yor chips total: {player_chips.total}")

	        # Ask to play again
	        
	        #variable that count ammount of games played
	        game = game+1
	        
	        again = input("Are you want to play again?(yes,no)")
	        if again == "yes":
	              continue
	        else:
	              break
