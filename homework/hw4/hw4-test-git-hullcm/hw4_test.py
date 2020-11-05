
#########################################
##### Name: Chloe Hull              #####
##### Uniqname: hullcm@umich.edu    #####
#########################################


import unittest
import hw4_cards as cards

# SI 507 Winter 2020
# Homework 4 - Code

## You can write any additional debugging/trying stuff out code here...
## OK to add debugging print statements, but do NOT change functionality of existing code.
## Also OK to add comments!

class TestCard(unittest.TestCase):
    # this is a "test"
    def test_0_create(self):
        card = cards.Card()
        self.assertEqual(card.suit_name, "Diamonds")
        self.assertEqual(card.rank, 2)

    # Add methods below to test main assignments. 
    def test_1_queen(self):
        c1 = cards.Card(rank=12)
        self.assertEqual(c1.rank_name, "Queen")

    def test2_clubs(self):
        c2 = cards.Card(suit=1)
        self.assertEqual(c2.suit_name, "Clubs")
        
    def test3(self):
        c3 = cards.Card(suit=3, rank=13)
        self.assertEqual(str(c3), "King of Spades")
    
    def test4(self):
        d = cards.Deck()
        self.assertEqual(len(d.cards), 52)
    
    def test5(self):
        d2 = cards.Deck()
        self.assertIsInstance(d2.deal_card(), cards.Card)
    
    def test6(self): ## is this okay, bc technically its two different instances?
        d4 = cards.Deck()
        length_before = len(d4.cards)
        d4.deal_card()
        length_after = len(d4.cards)
        self.assertEqual((length_before - 1), length_after)

    def test7(self):
        d5 = cards.Deck()
        c_removed = d5.deal_card()
        length_before = len(d5.cards)
        d5.replace_card(c_removed)
        length_after = len(d5.cards)
        self.assertEqual((length_before + 1), length_after)

    def test8(self):
        d7 = cards.Deck()
        length_before = len(d7.cards)
        d7.replace_card(cards.Card())
        length_after = len(d7.cards)
        self.assertEqual(length_before, length_after)




############
### The following is a line to run all of the tests you include:
if __name__ == "__main__":
    unittest.main()
