import pygame
from pygame.locals import *
import random
 
pygame.init()

play = True

#defining game constants 
HEIGHT = 500
WIDTH = 1000
FPS = pygame.time.Clock()
fps = 60                                                                    #frames per second

#colors!! uses the rgb (red, green, blue) system
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#variables
global player_pos, com_pos
player_speed = HEIGHT/100                                                   #speed P1's paddle moves
com_speed = HEIGHT/100                                                      #speed P2's paddle moves
player_bar_length = HEIGHT / 5                                              #length of P1's paddle
com_bar_length = HEIGHT / 5                                                 #length of P2's paddle
bar_width = WIDTH / 40                                                      #width of both paddles
player_pos = HEIGHT / 2                                                     #where P1's bar starts the game (center)
com_pos = HEIGHT / 2                                                        #where P2's bar starts the game
bar_distance = WIDTH / 20                                                   #how far the bars are from the left and right edges of the screen
big_range_x = round(WIDTH / 8)                                              #used for defining the bounds where the ball can spawn
big_range_y = round(HEIGHT / 8)                                             #other cord used for defining where the ball can spawn
p1_score = 0
p2_score = 0

global ball_speed_x, ball_speed_y, ball_pos_x, ball_pos_y
ball_radius = 50
ball_speed_x = -2                                                           #gets overwritten
ball_speed_y = -2                                                           #gets overwritten
ball_pos_x = (WIDTH/2)                                                      #gets overwritten
ball_pos_y = (HEIGHT/2)                                                     #gets overwritten
ball_speed_modifier = 5                                           #how much faster the ball goes when it hits a paddle
 

#setting the function for setting the ball's initial position
def settingUpBall():
    global ball_pos_x, ball_pos_y, ball_speed_x, ball_speed_y
    ball_pos_x = ((WIDTH/2) + random.randint(-big_range_x, big_range_x))    #sets the ball's position to a random spot
    ball_pos_y = ((HEIGHT/2) + random.randint(-big_range_y, big_range_y))   #random spot within our pre-defined area

    #setting the speed of the ball, this is done in a loop so it isn't too large or too small
    ok = False
    while (ok == False):
        ball_speed_x = round(random.uniform(-4, 4), 1)                      #a number between -4 and 4, rounded to the tenths place
        ball_speed_y = round(random.uniform(-4, 4), 1)
        if (abs(ball_speed_x) + abs(ball_speed_y)) < 5.5:                   #if the absolute value of the ball's speed in both directions added
            if (abs(ball_speed_x) + abs(ball_speed_y)) > 2.5:               #is less than 5.5 and more than 2.5
                if abs(ball_speed_x) > 1.5:
                    ok = True                                                   #it leaves the loop. Otherwise it rerolls until this limitation is met


#Creating the player's paddle
class Player(pygame.sprite.Sprite):
    def __init__(self):                                                     #__init__ runs when the game is loaded
        super().__init__()
        self.surf = pygame.Surface((bar_width,player_bar_length))           #defines size of the paddle
        self.surf.fill(BLUE) #defines it's color
        self.rect = self.surf.get_rect(center = (bar_distance, player_pos)) #tells the program where to draw the paddle
    def update(self):                                                       #function that makes the bars move
        global player_pos
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w]:                                               #fires whenever the w key is pressed
            if (player_pos - (player_bar_length /2)) > 0:                   #stops the bar from going up off-screen
                player_pos -= player_speed                                  #moves the bar
        if pressed_keys[K_s]:                                               #fires whenever the s key is pressed
            if (player_pos + (player_bar_length /2)) < HEIGHT:              #stops the bar from going down off-screen
                player_pos += player_speed                                  #moves the bar
        self.rect = self.surf.get_rect(center = (bar_distance, player_pos)) #tells the program where to redraw the paddle

#Player 2!! (they started as a com player when development started)
class Com(pygame.sprite.Sprite):                                                        #it's the same as player
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((bar_width, com_bar_length))
        self.surf.fill(RED)                                                             #except it's red
        self.rect = self.surf.get_rect(center = ((WIDTH - bar_distance), com_pos))
    def update(self):
        global com_pos
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            if (com_pos - (com_bar_length /2)) > 0:
                com_pos -= com_speed
        if pressed_keys[K_DOWN]:
            if (com_pos + (com_bar_length /2)) < HEIGHT:
                com_pos += com_speed
        self.rect = self.surf.get_rect(center = ((WIDTH - bar_distance), com_pos))

#the ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self): #this runs on start
        super().__init__()
        self.surf = pygame.Surface((ball_radius,ball_radius))               #makes the ball a square with that width and height
        self.surf.fill(BLACK)                                               #makes it black
        self.rect = self.surf.get_rect(center = (ball_pos_x, ball_pos_y))   #sets it's initial position
        settingUpBall()                                                     #runs that function from earlier
    def update(self):
        global ball_pos_x, ball_pos_y, ball_speed_x, ball_speed_y, p1_score, p2_score
        ball_pos_x += ball_speed_x                                          #moves the ball left/right
        ball_pos_y += ball_speed_y                                          #moves the ball up/down
        #bouncing off the walls
        if (ball_pos_y - (ball_radius /2)) > 0:                             #if the ball touches the bottom
            ball_speed_y *= -1                                              #it "bounces" up
        if (ball_pos_y + (ball_radius /2)) < HEIGHT:                        #if the ball touches the top
            ball_speed_y *= -1                                              #it "bounces" down
        #handling collision
        #PLayer 1                                                                               warning: this code's a doozy of arithmatic
        if (ball_pos_x) > (bar_distance + (bar_width / 2)):                                     #if the ball's left side's position is in line with P1's paddle
            if (ball_pos_x) < (bar_distance + bar_width):                                       #but not THROUGH P1's paddle
                if (ball_pos_y + (ball_radius/2)) > (player_pos - (player_bar_length/2)):       #and the top of the ball is above the bottom of P1's paddle
                    if (ball_pos_y - (ball_radius/2)) < (player_pos + (player_bar_length/2)):   #and the bottom of the ball is below the top of P1's paddle
                        if (ball_speed_x) < 0:                                                  #and it hasn't already bounced1
                            ball_speed_x *= -ball_speed_modifier                                    #THEN we have a bounce
                            ball_speed_y *= ball_speed_modifier
        #PLayer 2
        if (ball_pos_x) < ((WIDTH - bar_distance) - (bar_width / 2)): #back of bar              same logic with P2
            if (ball_pos_x) > (WIDTH - bar_distance - bar_width): #front of bar
                if (ball_pos_y + (ball_radius/2)) > (com_pos - (com_bar_length/2)): #top of ball, bottom of bar
                    if (ball_pos_y - (ball_radius/2)) < (com_pos + (com_bar_length/2)): #bottom of ball, top of bar
                        if ball_speed_x > 0:
                            ball_speed_x *= -ball_speed_modifier
                            ball_speed_y *= ball_speed_modifier
        #scoring goals
        if (ball_pos_x - (3 * ball_radius)) > WIDTH:                        #if the ball leaves the screen, with a little bit extra room for a buffer
            p1_score += 1                                                   #a player scores a point
            settingUpBall()                                                 #and the ball resets
        if (ball_pos_x + (3* ball_radius)) < 0:                             #and that applies to both players
            p2_score += 1
            settingUpBall()
        #redraws itself
        self.rect = self.surf.get_rect(center = (ball_pos_x, ball_pos_y))






#Now that every function and class has been defined,
#We can FINALLY start setting up the game loop. 



#setting up the game
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))       #creates a window "WIDTH" wide and "HEIGHT" tall
pygame.display.set_caption("Echo's Game")                       #names the window created "Echo's Game", after its creator, me

#these three lines of code create specific instances of the three classes. 
P1 = Player() 
B1 = Ball()
P2 = Com()

#this adds them all to a group that gets drawn
all_sprites = pygame.sprite.Group()
all_sprites.add(B1)
all_sprites.add(P1)
all_sprites.add(P2)


#game loop, every line of code here gets ran every frame
while play: 
    #drawing background
    displaysurface.fill(WHITE)

    #movement
    B1.update()
    P1.update()
    P2.update()

    #drawing sprites, since we used that group command earlier, this only takes two lines of code
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    #redraws the game
    pygame.display.update()
    
    #sets a tick limit so the speed doesn't fluctuate
    FPS.tick(fps)

    #the quit functionality
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exiting game")
            pygame.quit()
            play = False

    #player wins
    if p1_score == 2:
        pygame.quit()
        play = False
        print("")
        print("Good Game!!")
        print("Final Score:")
        print(f"{p1_score} - {p2_score}")
        print("Player 1 (blue) wins!!")
        print("")
        input("Press enter.")
    if p2_score == 2:
        pygame.quit()
        play = False
        print("")
        print("Good Game!!")
        print("Final Score:")
        print(f"{p1_score} - {p2_score}")
        print("Player 2 (red) wins!!")
        print("")
        input("Press enter.")
        
        