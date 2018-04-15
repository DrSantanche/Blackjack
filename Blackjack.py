# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 18:21:07 2018

@author: Marco Santanché
"""

from random import shuffle

#Card ranks and suits:
Ranks = [i for i in range(2,11)] + ['J','Q','K','A']
Suits = ['SPADES','DIAMONDS','CLUBS','HEARTS']

def deck_start():
    return [[rank, suit] for rank in Ranks for suit in Suits]

def Score(hand):
    Value = 0
    Aces = 0
    for i in hand:
        if i[0] in Ranks[:-4]:
            Value += i[0]
        if i[0] in Ranks[-4:-1]:
            Value += 10
        if i[0] == Ranks[-1]:
            Value += 11
            Aces += 1
    while Aces > 0:
        if Value > 21:
            Value -= 10
            Aces -= 1
        else:
            Aces -= 1
    return Value

#FOR PART II:
#The best strategy, provided the dealer's behaviour, is:
    # always hit if he is higher than us and will stay
    # stand if we are higher than him
    # in the other cases (he is higher than us and will hit) hit only if the probability
    # to beat him is higher than the probability of losing being lower or being busted.
    # Infact, if we are lower but we could lose and he will hit, it's better to wait
    # and let him play: he would also be more likely to lose than winning. Otherwise, this
    # means that he has arrived over 16 and we need to hit as much as possible to beat him.
    
def AutomaticMove(deck,playerhand,dealerhand):
    l = len(deck)
    if Score(playerhand) > Score(dealerhand):
        MyMove = "Stand"
    elif Score(playerhand) <= Score(dealerhand) and Score(dealerhand) > 16:
        MyMove = "Hit"
    else:
        poss_scores = []
        for i in deck:
            playerhand.append(i)
            newhand = list(playerhand)
            poss_scores.append(Score(newhand))
            newhand.pop()
            playerhand.pop()
        wins = sum(score > Score(dealerhand) and score <= 21 for score in poss_scores)
        if float(wins)/float(l) > 0.5:
            MyMove = "Hit"
        else:
            MyMove = "Stand"
    return(MyMove)

#Automatic moves? (For part II)
Auto = True #just change in true for the automatic strategy    
Match = True
while Match:
    #If any player goes over 21, this will be true:
    Bust=False    
    
    #Start: have a deck and shuffle it
    deck = deck_start()
    shuffle(deck)
    
    #Pick cards (player and dealer) and show them
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    print("Your hand: " + str(player_hand))
    print("Dealer's hand: " + str(dealer_hand))
    
    #Hand values
    player_value = Score(player_hand)
    dealer_value = Score(dealer_hand)
    
    #Counting the turns (end if Blackjack or Busted or stand 2 times)
    PlayerTurn = 0
    while PlayerTurn < 2:
        print('Your current score is: ' + str(player_value))
        print("Dealer's score is: " + str(dealer_value))
        
        #Choose your move or automate that
        if Auto == False and player_value < 21:
            Move = raw_input('Make your move: hit or stand? ')
        else:
            Move=AutomaticMove(deck,player_hand,dealer_hand)
            print("The Move chosen is: " + Move)
        
        while Move not in ['Hit','hit','Stand','stand']:
            Move=raw_input('Move not valid. Make your move: hit or stand? ')
            
        if Move in ['Hit','hit']:
            
            #Get new card
            player_hand.append(deck.pop())
            print(player_hand)
            
            #Get new value
            player_value = Score(player_hand)
            
            #Check the value of the hand!
            if player_value > 21:
                print("Busted! The DEALER wins")
                PlayerTurn = 2
                Bust = True
                Move = "Stand"
                
            if player_value == 21:
                print("BLACKJACK for the player!")
                PlayerTurn = 2
                Move = "Stand"
            
            if Bust == False:               
                print('Your current score is: ' + str(player_value))
                print("Dealer's score is: " + str(dealer_value))
            
        if Move in ['Stand','stand']:
            PlayerTurn = PlayerTurn + 1

            if PlayerTurn > 0 and Bust == False:
                #Dealer moves are forced
                while dealer_value <= 16:
                    #Get new card
                    print("The dealer picks up a new card")
                    dealer_hand.append(deck.pop())
                    print(dealer_hand)
                    
                    #Get new value
                    dealer_value = Score(dealer_hand)
                    print("Dealer score: " + str(dealer_value))
                
                if dealer_value > 21:
                    print("Busted! The PLAYER wins")
                    PlayerTurn = 2
                    Bust = True
                    
                if dealer_value == 21:
                    print("BLACKJACK for the dealer!")
                
    if PlayerTurn >= 2 and not Bust:
        if player_value > dealer_value:
            print("The PLAYER wins!")
        if player_value < dealer_value:
            print("The DEALER wins!")
        if player_value == dealer_value:
            print("It's a DRAW!")
                        
    print("Player score: " + str(player_value))
    print("Dealer score: " + str(dealer_value))
            
    Rematch = raw_input('Rematch? ')
    
    while Rematch not in ['Yes','yes','No','no']:
        Rematch = raw_input('Choice not correct. Type yes or no. Rematch? ')
    if Rematch in ['Yes','yes']:
        Match = True
    if Rematch in ['No','no']:
        Match = False