add_library("minim")
import os
import random
import time

path = os.getcwd()
player = Minim(this)

LASER_W = 20
LASER_H = 20

class Player:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/images/" + "playerShip1_red.png")
        self.img_w = 60
        self.img_h = 40
        self.SPACEBAR = False;
        self.key_handler = {LEFT:False, RIGHT:False, self.SPACEBAR: False}
        self.vx = 10
        self.r = 30
        self.collision = False   

    def move_side(self):
        if self.key_handler[RIGHT] == True and self.x + self.img_w <= width:
            self.vx = 10
        elif self.key_handler[LEFT] == True and self.x >= 0:
            self.vx = -1 * 10
        else:
            self.vx = 0
           
        self.x = self.x + self.vx
   
    def display(self):
        self.move_side()
        image(self.img, self.x, self.y, self.img_w, self.img_h)
        
        #initiate collision between enemy lasers and player
        for enemy_laser in game.enemy_laser_list:
            if self.distance(enemy_laser) <= self.r + enemy_laser.r:
                game.enemy_laser_list.remove(enemy_laser)
                self.collision = True
                
                #decrement lives
                game.lives-=1
            
        
    def distance(self, target):
        return((self.x+30 - target.x) **2 + (self.y+20 - target.y) ** 2) ** 0.5
        
class Alien:
    
    def __init__(self, img, x, y, w, h):
        self.x = x
        self.y = y
        self.w = 30
        self.h = 20
        self.vx = 1
        self.vy = 0
        self.img = loadImage(path + "/images/" + img)
        
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)
        
    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        
    
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/images/" + img)
        
    def display(self):
        #self.move_side()
        image(self.img, self.x, self.y, LASER_W, LASER_H)
        
        #shoot laser up
        self.y -=2
        
class EnemyLaser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 4
        
    def display(self):
        fill(73, 3, 252)
        circle(self.x,self.y,8)
        self.y +=2
        
class Game:
    def __init__(self):
        self.speed = 480
        self.lasers = [] 
        self.the_player = Player(270, 350)
        self.players = [self.the_player]        #list to append and remove instances of the player after life is lost
        self.y = 50
        self.x = 100
        self.score = 0
        self.lives = 3
        self.level = 1
        self.start_game = True                 
        self.game_over = False                 
        self.win_game = False
        self.game_over_screen = loadImage(path + "/images/" + "game_over.png")
        self.enemy_laser_list = []
        self.alien_list = []
        
        #append aliens to list, for ease of display
        for n in range(3):
            self.x = 100
            for i in range(10):
                self.alien_list.append(Alien("attack_spaceship.png", self.x + (40 * i), self.y + (40 * n), 30, 20))

    def display_player(self):
        for n in self.players:
            n.display()
        self.initiate_new_life()
    
    #initiate new object after loss of life
    def initiate_new_life(self):
        if self.the_player.collision == True:
            self.players.remove(self.the_player)
            
            #pause game for a second to indicate loss of life
            time.sleep(1)
            
            self.the_player = Player(270, 350)
            self.players.append(self.the_player)
                                
    def play(self):
        
        #display text above the game
        fill(255,255,255)
        score_text = createFont("OCR A Extended", 16)
        textFont(score_text, 16)
        
        lives_text = createFont("OCR A Extended", 16)
        textFont(lives_text, 16)
        
        level_text = createFont("OCR A Extended", 16)
        textFont(level_text, 16)
        
        text("Score: " + str(game.score), 10, 30)
        text("Lives: " + str(game.lives), 265, 30)
        text("Level: " + str(game.level), 515, 30)
        
        self.display_player()
        #display and shoot player lasers
        for laser in self.lasers:
            laser.display()
            
            #remove alien when collision occurs
            for alien in self.alien_list:
                if laser.x >= alien.x and laser.x < alien.x + 30 and laser.y >= alien.y and laser.y < alien.y+20:
                    self.alien_list.remove(alien)
                    self.score+=10 
        
        #display aliens                
        for alien in self.alien_list:
            alien.display()  
            
            #allow aliens to move clockwise within boundaries.
            alien.move()
            if alien.x >= 500:
                alien.vx = -2
            if alien.x <= 100:
                alien.vx = 2
            
            #sets the frequency of enemy lasers being shot based on probability
            if random.randrange(0, self.speed)== 1:
                self.enemy_laser_list.append(EnemyLaser(alien.x + 15, alien.y +25))

        for enemy_laser in self.enemy_laser_list:
            enemy_laser.display()
        
        self.end_game()
    
    def end_game(self):
        if self.lives <= 0:
            image(self.game_over_screen, 0, 0)
            self.game_over = True
            self.stage = 2
     
    #reset values for new game       
    def reset(self):
        self.speed = 480
        self.lasers = [] 
        self.the_player = Player(270, 350)
        self.players = [self.the_player]
        self.y = 50
        self.x = 100
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.start_game = False
        self.win_game = False
        self.game_over_screen = loadImage(path + "/images/" + "game_over.png")
        self.alien_list = []
        self.enemy_laser_list = []
        for n in range(3):
            self.x = 100
            for i in range(10):
                self.alien_list.append(Alien("attack_spaceship.png", self.x + (40 * i), self.y + (40 * n), 30, 20))
    
    #reset values for new level
    def advance(self):
        self.speed = 480
        self.lasers = [] 
        self.the_player = Player(270, 350)
        self.players = [self.the_player]
        self.y = 50
        self.x = 100
        self.game_over = False
        self.start_game = False
        self.win_game = False
        self.game_over_screen = loadImage(path + "/images/" + "game_over.png")
        self.alien_list = []
        self.enemy_laser_list = []
        for n in range(3):
            self.x = 100
            for i in range(10):
                self.alien_list.append(Alien("attack_spaceship.png", self.x + (40 * i), self.y + (40 * n), 30, 20))
    
    def move_levels1(self):
        if self.level == 1:
            if len(self.alien_list) == 0:
                self.level = 2
                self.speed = 360
                self.advance()
                
    def move_levels2(self):
        if self.level == 2:
            if len(self.alien_list) == 0:
                self.level = 3
                self.speed = 240
                self.advance()
                
    def game_won(self):
        if self.level == 3:
            if len(self.alien_list) == 0:
                self.win_game = True
    
game = Game()


def setup():
    size(600,400)
    background(0,0,0)
    
def draw():
    
    win_screen = loadImage(path + "/images/" + "win.png")
    
    #display start screen
    start_game_screen = loadImage(path + "/images/" + "start_page.png")
    image(start_game_screen, 0, 0)
   
    game.move_levels1()
    game.move_levels2()
    game.game_won()
    
    if game.start_game == False:
        background(0, 0, 0)
        game.play()
        
    #display game over page
    if game.game_over == True:
        background(210)
        image(game.game_over_screen, 0, 0)
        
    if game.win_game == True:
        image(win_screen, 0, 0)
        

def keyPressed():
    #we commented the sound out because it caused the code to hang, but it works.
    
    #sfx = player.loadFile(path + "/sounds/laser.wav")
    if keyCode == LEFT:
        game.the_player.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.the_player.key_handler[RIGHT] = True
    elif key == ' ':
        game.lasers.append(Laser(game.the_player.x+20, game.the_player.y-20, "laser.png"))
        #sfx.play()

def keyReleased():
    if keyCode == LEFT:
        game.the_player.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.the_player.key_handler[RIGHT] = False
        
def mouseClicked():
    if game.start_game == True:
        game.start_game = False
        background(0, 0, 0)
        game.play()
        
    if game.game_over == True:
        background(210)
        game.reset()
        
    if game.win_game == True:
        game.reset()
