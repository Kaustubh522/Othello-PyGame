# Othello Game (2 player) Using PyGame Module
# By Kaustubh Kulkarni

''' Following things are left:
6. Game record
9. Graphics changing facility (not essential) '''

# importing modules
import pygame
from tkinter import *
from tkinter import filedialog

# Initialize PyGame
pygame.init()

# Main Loop Variable
running = True

# Set up the window
pygame.display.set_caption("Othello") # wn title
wn = pygame.display.set_mode((1200, 720), pygame.RESIZABLE)

# Set up colors, fonts, sound
boardcolor = (0, 158, 42)
new_game_button_color = (180, 30, 180)
settings_button_color = (180, 30, 180)
font_size = 25
font = pygame.font.SysFont("courier", font_size)
popup_font = pygame.font.SysFont("arial", 30) 
score_font = pygame.font.SysFont("arial", 100)
btn_font = pygame.font.SysFont("arial", 50)
tab = "     "
flip_sound = pygame.mixer.Sound("flip.mp3")

# Board properties
block_size = 85
file_list = ["A", "B", "C", "D", "E", "F", "G", "H"]
white_img = pygame.image.load("rsz_white.png") #Can replace with any 80px img
black_img = pygame.image.load("rsz_black.png") #Can replace with any 80px img
high_img = pygame.image.load("turn_high.png")
spk_on = pygame.image.load("Speaker_on32.png")
spk_off = pygame.image.load("Speaker_off32.png")
spk_img = spk_on

x_coords_dic = {"A":252.5, "B":337.5, "C":422.5, "D":507.5, "E":592.5, "E":677.5, 
                "F": 762.5, "G": 847.5, "H": 932.5}
y_coords_dic = {0:2.5, 1:87.5, 2:172.5, 3:257.5, 4:342.5, 5:427.5, 6:512.5, 7:597.5}
x_coords_list = [252.5, 337.5, 422.5, 507.5, 592.5, 677.5, 762.5, 847.5, 932.5]
y_coords_list = [2.5, 87.5, 172.5, 257.5, 342.5, 427.5, 512.5, 597.5]

black_turn = True
moved = False
score_white = 2
score_black = 2
winner = "None"
gameover = False
popup_done = False
sound_on = True
highlight_legal_moves = True
highlight_last_move = True
show_coordinates = True
handicap = 0

# The main game grid
def new_grid():
    global handicap
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, "W", "B", 0, 0, 0],
        [0, 0, 0, "B", "W", 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    if handicap == 1:
        grid[0][0] = "B"
    elif handicap == 2:
        grid[0][0] = "B"
        grid[0][7] = "B"
    elif handicap == 3:
        grid[0][0] = "B"
        grid[0][7] = "B"
        grid[7][0] = "B"
    elif handicap == 4:
        grid[0][0] = "B"
        grid[0][7] = "B"
        grid[7][0] = "B"
        grid[7][7] = "B"
    return grid
grid = new_grid()

# Draw Board Function
def draw_board():

    for y in range (8): #draw the squares
        for x in range (8):
            rect = pygame.Rect((250+x*(block_size), y*(block_size), block_size, block_size))
            pygame.draw.rect(wn, boardcolor, rect)
            pygame.draw.rect(wn, (0, 0, 0), rect, 2)
    
    if show_coordinates:
        for num in range(8, 0, -1): # write rank nos.
            rank = font.render(str(num), True, (255, 255, 255))
            wn.blit(rank, (225, int((num-1) * block_size + block_size/2 - font_size/2)))

        for num in range(1, len(file_list)+1): # write file letters
            file_let = font.render(file_list[num-1], True, (255, 255, 255))
            wn.blit(file_let, ((250 + int((num-1) * block_size + block_size/2 - font_size/2), 680)))

    for i in range(8): # draw the pieces
        for j in range(8):
            if grid[i][j] == "B":
                #draw black circle image
                wn.blit(black_img, (int(x_coords_list[i]), int(y_coords_list[j])))
            elif grid[i][j] == "W":
                # draw white circle image
                wn.blit(white_img, (int(x_coords_list[i]), int(y_coords_list[j])))

    # Highlight legal moves
    if highlight_legal_moves:
        for i in range(8):
            for j in range(8):
                if grid[i][j] == "L":
                    wn.blit(high_img, (int(x_coords_list[i]+15), int(y_coords_list[j]+15)))

    # highlight last move
    if moved and highlight_last_move:
        try:
            highlight_rect = pygame.Rect((high_x, high_y, block_size, block_size))
            pygame.draw.rect(wn, (255, 0, 0), highlight_rect, 2)
        except:
            pass

# Get square function
def getsquare_x(x):
    if x > 250 and x < 335:
        return 0
    elif x > 335 and x < 420:
        return 1
    elif x > 420 and x < 505:
        return 2
    elif x > 505 and x < 590:
        return 3
    elif x > 590 and x < 675:
        return 4
    elif x > 675 and x < 760:
        return 5
    elif x > 760 and x < 845:
        return 6
    elif x > 845 and x < 930:
        return 7
def getsquare_y(y):
    if y > 0 and y < 85:
        return 0
    elif y > 85 and y < 170:
        return 1
    elif y > 170 and y < 255:
        return 2
    elif y > 255 and y < 340:
        return 3
    elif y > 340 and y < 425:
        return 4
    elif y > 425 and y < 510:
        return 5
    elif y > 510 and y < 595:
        return 6
    elif y > 595 and y < 680:
        return 7

# Score function
def write_score():
    global score_white
    global score_black
   
    score_white = sum(x.count("W") for x in grid)
    score_black = sum(x.count("B") for x in grid)

    score_white_text = score_font.render(tab+str(score_white),True, (255,255,255), (230, 169, 48))
    score_black_text = score_font.render(tab+str(score_black),True, (0,0,0), (230, 169, 48))
    wn.blit(score_black_text, (10, 100))
    wn.blit(score_white_text, (950, 520))
    wn.blit(black_img, (15,115))
    wn.blit(white_img, (955,535))

# Winner popup function
def won_popup():
    global popup_done
    if gameover and not popup_done:
        if winner == "None":
            winner_text = score_font.render("Draw!", True, (255, 69, 0), (0, 255, 255))
        else:
            winner_text = score_font.render(winner+" Won!", True, (255, 69, 0,), (0, 255, 255))
        text_rect = winner_text.get_rect(center=(600, 360))
        wn.blit(winner_text, text_rect)   

# Winner function
def check_winner():
    global winner
    global gameover
    if loop_turns >= 2:
        gameover = True
        if score_white == score_black:
            winner = "None"
        elif score_white > score_black:
            winner = "White"
        elif score_black > score_white:
            winner = "Black"      

# Legal moves functions

def find_legal_moves():
    global flippable
    global black_turn
    global grid
    global loop_turns

    # Initialize legality moves
    for i in range(8):
        for j in range(8):
            if grid[i][j] == "L":
                grid[i][j] = 0
    
    # Set flippable to false
    flippable = False

    # If black's turn is there
    if black_turn:
        turnvar = "B"
        checkvar = "W"
    elif not black_turn:
        turnvar = "W"
        checkvar = "B"

    for i in range(8):
        for j in range(8):
            if grid[i][j] != turnvar and grid[i][j] != checkvar:
                if i != 7:
                    if grid[i+1][j] == checkvar:
                            # horizontal fwd
                            for m in range(1, 8-i, 1):
                                    if grid[i+m][j] == turnvar:       
                                        flippable = True
                                        grid[i][j] = "L"
                                        break
                                        break
                                        break
                                    elif grid[i+m][j] == 0:
                                        break
                                        break
                                        break
                        
                if i != 0:
                    if grid[i-1][j] == checkvar:
                        #horizontal bwd
                        for m in range(1, i+1, 1):
                                if grid[i-m][j] == turnvar:
                                    flippable = True
                                    grid[i][j] = "L"
                                    break
                                    break
                                    break
                                elif grid[i-m][j] == 0:
                                    break
                                    break
                                    break
    
                if j != 7:
                    if grid[i][j+1] == checkvar:
                        #vertical up
                        for m in range(1, 8-j, 1):
                                if grid[i][j+m] == turnvar:
                                    flippable = True
                                    grid[i][j] = "L"
                                    break
                                    break
                                    break
                                elif grid[i][j+m] == 0:
                                    break
                                    break
                                    break
                            
                if j != 0:
                    if grid[i][j-1] == checkvar:
                        # vertical down
                        for m in range(1, j+1, 1):
                                if grid[i][j-m] == turnvar:
                                    flippable = True
                                    grid[i][j] = "L"
                                    break
                                    break
                                    break
                                elif grid[i][j-m] == 0:
                                    break
                                    break
                                    break
                            
                if i!= 7 and j != 7:
                    if grid[i+1][j+1] == checkvar:
                        # diagonal 
                            for m in range (1, min(8-i, 8-j), 1):                  
                                    if grid[i+m][j+m] == turnvar:
                                        flippable = True
                                        grid[i][j] = "L"
                                        break
                                        break
                                        break
                                    elif grid[i+m][j+m] == 0:
                                        break
                                        break
                                        break
                                
                if i != 0 and j != 0:
                    if grid[i-1][j-1] == checkvar:
                        # diagonal 
                            for m in range (1, min(i+1, j+1), 1):                            
                                    if grid[i-m][j-m] == turnvar:
                                        flippable = True
                                        grid[i][j] = "L"
                                        break
                                        break
                                        break
                                    elif grid[i-m][j-m] == 0:
                                        break
                                        break
                                        break
                                
                if i != 7 and j != 0:
                    if grid[i+1][j-1] == checkvar:
                        # diagonal 
                            for m in range (1, min(8-i, j+1), 1):
                                    if grid[i+m][j-m] == turnvar: 
                                        flippable = True
                                        grid[i][j] = "L"
                                        break
                                        break
                                        break
                                    elif grid[i+m][j-m] == 0:
                                        break
                                        break
                                        break
                                
                if i != 0 and j != 7:
                    if grid[i-1][j+1] == checkvar:
                        # diagonal 
                            for m in range (1, min(i+1, 8-j), 1):
                                    if grid[i-m][j+m] == turnvar:
                                        flippable = True
                                        grid[i][j] = "L"
                                        break
                                        break
                                        break
                                    elif grid[i-m][j+m] == 0:
                                        break
                                        break
                                        break
                             
    if flippable == False:  
        black_turn = not black_turn
        loop_turns += 1
    else:
        loop_turns = 0

# Edit grid function
def edit_grid(i, j):
    global black_turn
    global grid
    global high_x
    global high_y
    global moved

    moved = True

    if black_turn:
        turnvar = "B"
        checkvar = "W"
    elif not black_turn:
        turnvar = "W"
        checkvar = "B"

    if grid[i][j] == "L":
        if sound_on:
            flip_sound.play()  

        high_x = int(x_coords_list[i] - 2.5)
        high_y = int(y_coords_list[j] - 2.5)

        grid[i][j] = turnvar

        if i != 7:
            if grid[i+1][j] == checkvar:
                # horizontal fwd
                for m in range(1, 8-i, 1):
                        if grid[i+m][j] == turnvar:
                            for n in range(m+1):
                                grid[i+n][j] = turnvar
                            break
                        elif grid[i+m][j] == 0:
                            break
                       
        if i != 0:
            if grid[i-1][j] == checkvar:
                #horizontal bwd
                for m in range(1, i+1, 1):               
                    if grid[i-m][j] == turnvar:
                        for n in range(m+1):
                            grid[i-n][j] = turnvar
                        break
                    elif grid[i-m][j] == 0:
                        break
                   
        if j != 7:
            if grid[i][j+1] == checkvar:
                #vertical up
                for m in range(1, 8-j, 1):      
                    if grid[i][j+m] == turnvar:
                        for n in range(m+1):
                            grid[i][j+n] = turnvar
                        break
                    elif grid[i][j+m] == 0:
                        break
                   
        if j != 0:
            if grid[i][j-1] == checkvar:
                # vertical down
                for m in range(1, j+1, 1):
                    if grid[i][j-m] == turnvar:
                        for n in range(m+1):
                            grid[i][j-n] = turnvar
                        break
                    elif grid[i][j-m] == 0:
                        break
                    
        if i!= 7 and j != 7:
            if grid[i+1][j+1] == checkvar:
                # diagonal 
                    for m in range (1, min(8-i, 8-j), 1):
                        if grid[i+m][j+m] == turnvar:
                            for n in range (m+1):
                                grid[i+n][j+n]= turnvar
                            break
                        elif grid[i+m][j+m] == 0:
                            break

        if i != 0 and j != 0:
            if grid[i-1][j-1] == checkvar:
                # diagonal 
                    for m in range (1, min(i+1, j+1), 1):
                        if grid[i-m][j-m] == turnvar:
                            for n in range (m+1):
                                grid[i-n][j-n]= turnvar
                            break
                        elif grid[i-m][j-m] == 0:
                            break
                        
        if i != 7 and j != 0:
            if grid[i+1][j-1] == checkvar:
                # diagonal 
                    for m in range (1, min(8-i, j+1), 1):
                        if grid[i+m][j-m] == turnvar:
                            for n in range (m+1):
                                grid[i+n][j-n]= turnvar
                            break
                        elif grid[i+m][j-m] == 0:
                            break
                       
        if i != 0 and j != 7:
            if grid[i-1][j+1] == checkvar:
                # diagonal 
                    for m in range (1, min(i+1, 8-j), 1):
                        if grid[i-m][j+m] == turnvar:
                            for n in range (m+1):
                                grid[i-n][j+n]= turnvar
                            break
                        elif grid[i-m][j+m] == 0:
                            break
        
        black_turn = not black_turn

# Draw buttons function
def draw_buttons():
    # New game button
    new_game_text = btn_font.render("New Game", True, (255, 255, 255), new_game_button_color)
    wn.blit(new_game_text, (950, 10))
    # Speaker button
    wn.blit(spk_img, (10, 10))
    # Settings button 
    settings_text = btn_font.render("Settings", True, (255, 255, 255), settings_button_color)
    wn.blit(settings_text, (950, 80))

def new_game():
    global grid
    global black_turn 
    global moved 
    global score_white 
    global score_black
    global winner 
    global gameover
    global popup_done 
    grid = new_grid()
    if handicap == 0:
        black_turn = True
    else:
        black_turn = False
    moved = False
    score_white = 2
    score_black = 2
    winner = "None"
    gameover = False
    popup_done = False

def whose_turn_popup():
    if not gameover:
        if black_turn:
            popup_text = popup_font.render("Black's Turn", True, (0, 0, 0),(255, 255, 255))
            wn.blit(popup_text, (10, 230))
        else:
            popup_text = popup_font.render("White's Turn", True, (0, 0, 0),(255, 255, 255))
            wn.blit(popup_text, (950, 470))

def check_spk_img():
    global spk_img
    if sound_on: 
            spk_img = spk_on
    else:
        spk_img = spk_off

def launch_settings_window():
    global highlight_legal_moves
    global highlight_last_move
    root = Tk()
    root.geometry("400x400")
    root.title("Settings")
    root.iconbitmap("gear.ico")
    root.lift()
    root.attributes('-topmost',True)
    def set_value_to_h(val):
        global highlight_legal_moves
        highlight_legal_moves = val
    def set_value_to_hl(val):
        global highlight_last_move
        highlight_last_move = val
    def set_value_to_coords(val):
        global show_coordinates
        show_coordinates = val
    # Highlight legal moves radio buttons
    h = BooleanVar()
    h.set(highlight_legal_moves)
    legal_move_label = Label(root, text="Highlight Legal Moves").grid(row=0, column=0)
    legal_move_btn_on = Radiobutton(root, text="On", variable=h, value=True, indicator=0, selectcolor="gold", command=lambda:set_value_to_h(h.get())).grid(row=0, column=1)
    legal_move_btn_off = Radiobutton(root, text="Off", variable=h,value=False, indicator=0,selectcolor="gold", command=lambda:set_value_to_h(h.get())).grid(row=0, column=2)
    # Highlight last move
    hl = BooleanVar()
    hl.set(highlight_last_move)
    last_move_label = Label(root, text="Highlight Last Move").grid(row=1, column=0)
    last_move_btn_on = Radiobutton(root, text="On", variable=hl, value=True, indicator=0, selectcolor="gold", command=lambda:set_value_to_hl(hl.get())).grid(row=1, column=1)
    last_move_btn_off = Radiobutton(root, text="Off", variable=hl,value=False, indicator=0,selectcolor="gold", command=lambda:set_value_to_hl(hl.get())).grid(row=1, column=2)
    # Show coorinates
    sc = BooleanVar()
    sc.set(show_coordinates)
    sc_move_label = Label(root, text="Show Coordinates").grid(row=2, column=0)
    sc_move_btn_on = Radiobutton(root, text="On", variable=sc, value=True, indicator=0, selectcolor="gold", command=lambda:set_value_to_coords(sc.get())).grid(row=2, column=1)
    sc_move_btn_off = Radiobutton(root, text="Off", variable=sc,value=False, indicator=0,selectcolor="gold", command=lambda:set_value_to_coords(sc.get())).grid(row=2, column=2)
    # Choose black image and white image
    def change_black_img():
        global black_img
        root.filename = filedialog.askopenfilename(initialdir="D:/Python/Games/Othello (PyGame)", title="Select An Image", filetypes=(("PNG Images", "*.png"),("JPG Images", "*.jpg")))
        try:
            black_img = pygame.image.load(root.filename)
        except pygame.error:
                pass
    def change_white_img():
        global white_img
        root.filename = filedialog.askopenfilename(initialdir="D:/Python/Games/Othello (PyGame)", title="Select An Image", filetypes=(("PNG Images", "*.png"),("JPG Images", "*.jpg")))
        try:
            white_img = pygame.image.load(root.filename)
        except pygame.error:
            pass
    def set_default_img():
        global black_img
        global white_img
        white_img = pygame.image.load("rsz_white.png") 
        black_img = pygame.image.load("rsz_black.png")
    def set_all_default():
        global highlight_legal_moves
        global highlight_last_move
        global show_coordinates
        highlight_legal_moves = True
        highlight_last_move = True
        show_coordinates = True
        h.set(True)
        hl.set(True)
        sc.set(True)
        set_default_img()
    black_label = Label(root, text="Black Image").grid(row=3, column=0)
    black_btn = Button(root, text="Choose Image", command=change_black_img).grid(row=3, column=1)
    white_label = Label(root, text="White Image").grid(row=4, column=0)
    white_btn = Button(root, text="Choose Image", command=change_white_img).grid(row=4, column=1)
    default_img_btn = Button(root, text="Reset Images to Default", command=set_default_img).grid(row=5, column=0)
    default_btn = Button(root, text="Reset All Settings to Default", command=set_all_default).grid(row=6, column=0)

    root.mainloop()

    # New Game Window
def launch_new_game_window():
    global handicap
    ngw = Tk()
    ngw.title("New Game")
    ngw.geometry("300x300")
    ngw.overrideredirect(True)
    ngw.lift()
    ngw.attributes("-topmost",True)
    hnd = IntVar()
    hnd.set(handicap)
    def set_value_to_hnd(val):
        global handicap
        handicap = val
    handicap_label = Label(ngw, text="Handicap").grid(row=0, column=0)
    btn_none = Radiobutton(ngw, text="None", variable=hnd, value=0, indicator=0, selectcolor="lime", command=lambda:set_value_to_hnd(0)).grid(row=0, column=1)
    btn_none = Radiobutton(ngw, text="1", variable=hnd, value=1, indicator=0, selectcolor="lime", command=lambda:set_value_to_hnd(1)).grid(row=0, column=2, ipadx=5, ipady=5)
    btn_none = Radiobutton(ngw, text="2", variable=hnd, value=2, indicator=0, selectcolor="lime", command=lambda:set_value_to_hnd(2)).grid(row=0, column=3, ipadx=5, ipady=5)
    btn_none = Radiobutton(ngw, text="3", variable=hnd, value=3, indicator=0, selectcolor="lime", command=lambda:set_value_to_hnd(3)).grid(row=0, column=4, ipadx=5, ipady=5)
    btn_none = Radiobutton(ngw, text="4", variable=hnd, value=4, indicator=0, selectcolor="lime", command=lambda:set_value_to_hnd(4)).grid(row=0, column=5, ipadx=5, ipady=5)
    start_btn = Button(ngw, text="Start Game", bg="aqua", command = lambda:[new_game(), ngw.destroy()]).grid(row=1, column=0,padx=5, pady=5,)
    cancel_btn = Button(ngw, text = "Cancel", bg="blue", command = ngw.destroy).grid(row=1, column=1, padx=5, pady=5,)
    ngw.mainloop()

# Game Loop
while running:
    wn.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: # mouse click
            if event.button == 1:

                if gameover and not popup_done:
                    popup_done = True
               
                coords = pygame.mouse.get_pos()
                #print(coords)

                if coords[0] > 250 and coords[0] < 930 and coords[1] > 0 and coords[1] < 680:
                    if getsquare_x(coords[0]) != None and getsquare_y(coords[1]) != None:
                        edit_grid(getsquare_x(coords[0]), getsquare_y(coords[1]))
                elif coords[0] > 950 and coords[0] <1155 and coords[1] > 10 and coords[1] < 70:
                    launch_new_game_window() # new game button
                elif coords[0] > 10 and coords[0] <42 and coords[1] > 10 and coords[1] < 42:
                    sound_on = not sound_on
                elif coords[0] > 950 and coords[0] <1090 and coords[1] > 80 and coords[1] < 140:
                    launch_settings_window()
        if event.type == pygame.MOUSEMOTION: # mouse movement

                move_coords = pygame.mouse.get_pos()

                #if move_coords[0] > 250 and move_coords[0] < 930 and move_coords[1] > 0 and move_coords[1] < 680:
                    #if getsquare_x(coords[0]) != None and getsquare_y(coords[1]) != None:
                        #edit_grid(getsquare_x(coords[0]), getsquare_y(coords[1]))
                if move_coords[0] > 950 and move_coords[0] <1155 and move_coords[1] > 10 and move_coords[1] < 70:
                    new_game_button_color = (240, 10, 240)
                else:
                    new_game_button_color = (180, 30, 180)
                if move_coords[0] > 950 and move_coords[0] <1090 and move_coords[1] > 80 and move_coords[1] < 140:
                    settings_button_color = (240, 10, 240)
                else:
                    settings_button_color = (180, 30, 180)
    # Check legal moves
    find_legal_moves()

    # Check winner
    check_winner()

    # Drawing the board
    draw_board()

    # Winner popup
    won_popup()

    # Count and write the score
    write_score()

    # Buttons
    draw_buttons()

    # popup for whose turn
    whose_turn_popup()

    # Speaker images
    check_spk_img()

    # Update the window
    pygame.display.update()