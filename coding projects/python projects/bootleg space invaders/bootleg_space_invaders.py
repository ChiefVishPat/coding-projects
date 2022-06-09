import pygame
import os
import time
import random
pygame.font.init()

#making the window that the game will take place on
WIDTH, HEIGHT = 600,600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bootleg Space Invaders")

#the background of the whole game
BACKGROUND = pygame.image.load(os.path.join("images", "space_background_1.png"))
#user ship
SPACE_SHIP = pygame.image.load(os.path.join("images", "ship_1.png"))
SPACE_SHIP = pygame.transform.scale(SPACE_SHIP, (75,75))
#enemy image
ENEMY = pygame.image.load(os.path.join("images", "enemy_1.png"))
ENEMY = pygame.transform.scale(ENEMY, (50,50))
#what the ship will be shooting (red laser)
USER_LASER = pygame.image.load(os.path.join("images", "red_laser.png"))
USER_LASER = pygame.transform.scale(USER_LASER, (50,50))
#what the enemy ships will be shooting at the user (green laser)
ENEMY_LASER = pygame.image.load(os.path.join("images", "green_laser.png"))

#setting up my ship class to be utilized by all ships (hereditary class)
class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    #drawing any ship that calls to this class with these general properties
    def draw(self, window):
        window.blit(self.ship_img, (self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    #move each laser on the screen down the screen
    def move_lasers(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):        #if laser is off screen
                self.lasers.remove(laser)       #then remove it from list of active lasers
            elif laser.collision(obj):          #if laser collides with user
                obj.health -= 25               #take away health
                self.lasers.remove(laser)       #remove laser after collision

    #creating a cooldown function
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter +=1

    #creates a laser and only shoots if cooldown is at 0
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y ,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1  #starts cooldown to 1 second

    #getter methods for width and height of the ship that is calling these methods
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


#setting up the player ship class which calls to the Ship class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = SPACE_SHIP
        self.laser_img = USER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    #move each laser on the screen down the screen
    def move_lasers(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):    # if laser is off screen
                self.lasers.remove(laser)   # then remove it from list of active lasers
            else:
                for obj in objs:
                    if laser.collision(obj):      # if laser collides with user
                        objs.remove(obj)
                        self.lasers.remove(laser)   # remove laser after collision

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width(),10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() *(self.health/self.max_health), 10))
        
        

#setting up enemy ship class which calls to the Ship class
class Enemy(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = ENEMY
        self.laser_img = ENEMY_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
    

    def move(self, velocity):    #movement of enemy ships
        self.y += velocity

    #creates a laser and only shoots if cooldown is at 0
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-25, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1  # starts cooldown to 1 second

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img 
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):         #draws each laser on screen
        window.blit(self.img, (self.x,self.y))

    def move(self,velocity):        #gives the laser up or down movement
        self.y += velocity
    
    def off_screen(self,height):        #tells if the laser is off the screen or not
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):       #tells us if two objects have collided
        return collide(self, obj)

#returns if two objects are overlapping or not
def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

#######################################################################

def main():
    #setting up some fonts for different screens
    main_font = pygame.font.SysFont("phosphate", 30)
    lost_font = pygame.font.SysFont("phosphate", 75)
    #defining some variables
    run = True
    FPS = 60
    level = 0
    lives = 3
    player_velocity = 10    #how fast the user will move
    enemy_velocity = 1      #how fast the enemies move
    laser_velocity = 8      #how fast each laser should move
    wave_length = 0         #amount of enemies per round
    lost = False
    lost_count = 0
    enemies = []            #establishing a list for all the enemies to be generated inside of

    player = Player(WIDTH/2 -38, 500)   #setting player at the center of the screen
    clock = pygame.time.Clock()         #setting up the clock speed

    ###################################################################

    #drawing everything on the screen that I need
    def refresh_window():
        WINDOW.blit(BACKGROUND,(0,0))
        #drawing all of my texts
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        WINDOW.blit(lives_label, (10,570))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 570))
        
        for enemy in enemies:           #drawing enemy ships
            enemy.draw(WINDOW)

        player.draw(WINDOW)     #drawing player

        if lost:
            lost_label = lost_font.render("YOU LOST!", 1, (255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - 100))

        pygame.display.update()

    ###################################################################

    #refreshing the screen for these actions
    while run:
        clock.tick(FPS)     #clock speed
        refresh_window()

        if lives <= 0 or player.health <= 0:       #this is basically setting up
            lost = True                            # a timer for when to close
            lost_count += 1                        # the game after we lose



        if lost:
            if lost_count > FPS * 5:            #shows lost screen for 5 seconds
                run = False
            else:
                continue


        if len(enemies) == 0:   #increasing level if there are no enemies on screen
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(100, WIDTH-100), random.randrange(-1000, -100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #allows user to close the game window
                run = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player_velocity > 0: #moving left while also setting window barrier
            player.x -= player_velocity
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player_velocity + player.get_width() < WIDTH:  # moving right while also setting window barrier
            player.x += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:               #adding movement to the enemies
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            #lets enemy shoot at random
            if random.randrange(0, 2*60) ==1:
                enemy.shoot()

            if collide(enemy,player):   #if enemy and player collide, decrement health and remove enemy
                player.health -= 25
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:   #if enemy passed bottom of screen
                lives -= 1                              #decrement lives by 1
                enemies.remove(enemy)                   #removing the enemy from the list
        
        player.move_lasers(-laser_velocity, enemies) #ability to shoot up at enemies and check collision

#######################################################################

#creating a main menu screen
def main_menu():
    title_font = pygame.font.SysFont("phosphate", 60)
    direction_font = pygame.font.SysFont("phosphate", 30)
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Bootleg Space Invaders", 1, (255, 255, 255))
        title_label = pygame.transform.scale(title_label, (500,150))

        direction_label = direction_font.render("Use the left/right arrow keys or A/D to move", 1, (255,255,255))
        direction_label = pygame.transform.scale(direction_label, (500, 50))

        start_label = direction_font.render("Press any mouse button to begin", 1, (255, 255, 255))
        start_label = pygame.transform.scale(start_label, (500, 50))


        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 50))
        WINDOW.blit(direction_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2))
        WINDOW.blit(start_label, (WIDTH/2 - title_label.get_width()/2, 500))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    quit()
#######################################################################

main_menu()