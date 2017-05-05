# implementation of card game - Memory

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

cards=[0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7]
exposed=[0]*len(cards)
state=0
turns=0

# helper function to initialize globals
def new_game():
    global cards,state,turns
    random.shuffle(cards)
    state=0
    turns=0
    exposed=[False for i in range(len(cards))]
    pass  

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global cards,exposed,state,card1,card2,turns
    card_index=pos[0]//50
    if state==0:        
        state=1
        exposed[card_index]=True
        card1=card_index
    
    elif state==1:
        card2=card_index
        if card1!=card2:
            exposed[card2]=True
            state=2
            turns+=1
            label.set_text('Turns: '+str(turns))
    else:
        if cards[card1]!=cards[card2]:
            exposed[card1]=False
            exposed[card2]=False
        card1=card_index
        if exposed[card1]==False:
            state=1
            exposed[card1]=True  
     
    pass
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards,exposed
    for i in range(len(cards)):
        card_pos=50*i
        if exposed[i]==True:
            canvas.draw_text(str(cards[i]),[card_pos+16,64],48,"White")
        else :
            canvas.draw_polygon(([card_pos,0],[card_pos,100],[card_pos+50,100],[card_pos+50,0]),
                                2,"Black","Green")
    pass


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns: 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


