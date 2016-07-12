from termcolor import colored


class Card:
    RED = 'Red'
    BLUE = 'Blue'
    WHITE = 'White'
    YELLOW = 'Yellow'
    GREEN = 'Green'
    RAINBOW = 'Rainbow'
    
    COLORS = [RED, BLUE, WHITE, YELLOW, GREEN, RAINBOW]
    
    PRINTABLE_COLORS = {
            RED: 'red',
            BLUE: 'blue',
            WHITE: 'grey',
            YELLOW: 'yellow',
            GREEN: 'green',
            RAINBOW: 'magenta'
        }
    
    def __init__(self, id, color, number):
        assert color in self.COLORS
        assert 1 <= number <= 5
        
        self.id = id
        self.color = color
        self.number = number
    
    
    def __repr__(self):
        return colored("%d %s" % (self.number, self.color), self.PRINTABLE_COLORS[self.color])

    
    def __hash__(self):
        return self.id

    
    def __eq__(self, other):
        return self.id == other.id


    def __ne__(self, other):
        return self != other



def deck():
    deck = []
    id = 0
    for color in Card.COLORS:
        for number in xrange(1, 6):
            if color == Card.RAINBOW:
                quantity = 1
            elif number == 1:
                quantity = 3
            elif 2 <= number <= 4:
                quantity = 2
            elif number == 5:
                quantity = 1
            else:
                raise Exception("Unknown card parameters.")
            
            for i in xrange(quantity):
                deck.append(Card(id, color, number))
                id += 1
    
    return deck

