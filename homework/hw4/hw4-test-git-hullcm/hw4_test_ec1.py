
#########################################
##### Name: Chloe Hull              #####
##### Uniqname: hullcm@umich.edu    #####
#########################################


import unittest
import hw4_cards_ec1 as cards

# SI 507 Winter 2020
# Homework 4 - Extra Credit #1 - Code

## You can write any additional debugging/trying stuff out code here...
## OK to add debugging print statements, but do NOT change functionality of existing code.
## Also OK to add comments!

class TestHand(unittest.TestCase):
    # this is a test
    def testInitialize(self):
        d1 = cards.Deck()
        d1.shuffle()
        d1 = d1.cards[:5]
        h1 = cards.Hand(d1)
        self.assertEqual(d1, h1.init_cards)

    def testAddAndRemove(self):
        d2 = cards.Deck()
        d2.shuffle()
        new_card = d2.cards[6]
        d2 = d2.cards[:5]
        h1 = cards.Hand(d2)
        len_before = len(h1.init_cards)
        h1.add_card(new_card)
        len_after = len(h1.init_cards)
        h1.remove_card()
        len_after_removal = len(h1.init_cards)
        self.assertEqual(len_before, (len_after - 1))
        self.assertEqual(len_after, (len_after_removal + 1))
    
    def testDraw(self):
        d3 = cards.Deck()
        d4 = cards.Deck()
        d4 = d4.cards[:5]
        h1 = cards.Hand(d4)
        length_before = len(h1.init_cards)
        deck_length_before = len(d3.cards)
        h1.draw(d3)
        length_after = len(h1.init_cards)
        deck_length_after = len(d3.cards)
        self.assertEqual(length_before, (length_after - 1))
        self.assertEqual(deck_length_before, (deck_length_after +1))


############
### The following is a line to run all of the tests you include:
if __name__ == "__main__":
    unittest.main()
