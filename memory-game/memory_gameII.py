# Implementation of Memory Game

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

WIDTH = 600
HEIGHT = 400
width_height = (WIDTH/9,HEIGHT/4.5)
IMAGE_WIDTH = 175
IMAGE_HEIGHT = 240
Back_Center =  (910,660)

    
# load image from public domain picture of cards
image = simplegui.load_image("https://imgur.com/download/zchHPnd")


# helper function to initialize globals
def new_game():    
    global deck, first_click, second_click, first_index, second_index, new_game, show_all
    global winning_list, counter, screen_center_list, center_position 
    #List of tuples giving center position of each card in image and card value
    Center_List = [(91, 126,"A"),(296,126,"2"),(500,126,"3"),(705,126,"4"),(910, 393,"10"),(91, 660,"J"),(296, 660,"Q"),(501, 660,"K")]
    first_index = -1
    second_index = -1
    show_all = False
    first_click = False
    second_click = False
    new_game = True
    center_position = []
    winning_list = []
    deck = {}
    counter = 0    
    Center_List = Center_List * 2  #double the list
    for i in range(5):
        random.shuffle(Center_List)  
        
        # prepare a dictionary, deck, containing data needed 
        # ... to position and identify each card 
    for i in range(16):
        image_center = (Center_List[i][0], Center_List[i][1])
        
        # Set up grid - multipliers are empirically determined
        if 0 <= i < 4: 
            screen_center_position = (i * (WIDTH/5 )+ 100, HEIGHT/5 - 25 )
        elif 4 <= i < 8:
            screen_center_position = ((i - 4) * (WIDTH/5)+100, 2 * HEIGHT/5 - 7  )
        elif 8 <= i < 12:
            screen_center_position = ((i - 8) * (WIDTH/5 )+100, 3 * HEIGHT/5 + 12 )
        elif 12 <= i < 16:
            screen_center_position = ((i - 12) * (WIDTH/5 )+100, 4 * HEIGHT/5 + 30 )            
        
        center_position.append(screen_center_position)  # Put grid in a list
        face = Center_List[i][2]  
        deck[i] = [image, image_center, screen_center_position, face]
        
def is_in_rectangle(point):   # Check if mouseclick is within a card and return its index
        for i in range(16):   # Check coordinates of each card ...                
            left_x = center_position[i][0] - width_height[0]/2
            right_x = center_position[i][0] + width_height[0]/2
            upper_y = center_position[i][1] - width_height[1]/2
            lower_y = center_position[i][1] + width_height[1]/2
                #  ... and compare with mouse x & y coordinates
            if left_x <= point[0] <= right_x and  upper_y <= point[1] <= lower_y:
                return i            
        return -1
     
# define event handlers
def mouseclick(pos):
    global first_click, second_click, winning_list, first_index, second_index, new_game, counter   
    
    i = is_in_rectangle(pos)     # get index if click is within a card ...
    if not i == -1:   #  ...  if it is ...
        if not (i in winning_list or (i == first_index or i == second_index)):    # if card not already exposed ...                    
            if new_game == True or (first_click == True and second_click == True):
                new_game = False
                counter += 1                
                first_click = True   #  --> "State 1"
                first_index = i
                second_click = False  # -- > reset to "State 1"
                second_index = -1  

            elif first_click == True and second_click == False:  # If this is the second click ...
                second_click = True   #  --> "State 2"
                second_index = i
                
                  # Determine if there is a match, and add indices of matched cards to list
                if deck[first_index][3] == deck[second_index][3] and not first_index == second_index:                    
                    winning_list.append(first_index)
                    winning_list.append(second_index)                    
                    
def show_all():
    global show_all
    if show_all == False:
        show_all = True
    else:
        show_all = False
    
def draw(canvas):  
    global first_click, second_click
    
    for i in range (16):      # Draw backs of all cards  
        canvas.draw_image(image,Back_Center,(175,240),center_position[i],width_height)
        
    if show_all:
        for i in range(16):
            canvas.draw_image(image,deck[i][1],(175,240),deck[i][2],width_height)
        
    if new_game == False:       
        if first_click == True:          
            canvas.draw_image(image,deck[first_index][1],(175,240),deck[first_index][2],width_height)        
            
        if second_click == True:   
            canvas.draw_image(image,deck[second_index][1],(175,240),deck[second_index][2],width_height)
            
        for i in range(len(winning_list)):             
            canvas.draw_image(image,deck[winning_list[i]][1],(175,240),deck[winning_list[i]][2],width_height)
            
#        if show_all:
#            for i in range(16):
#                canvas.draw_image(image,deck[i][1],(175,240),deck[i][2],width_height)
            
    label.set_text("Turns = " + str(counter))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
frame.add_label("")  # Spacer
label = frame.add_label("Turns = 0")
frame.add_label("")     # Spacer
frame.add_button("Toggle Show All", show_all)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

