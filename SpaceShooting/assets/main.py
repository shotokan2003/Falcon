
import pygame
import os
import random
import time
pygame.font.init()
width,height=1000,800
pygame.display.set_caption('SPACE SHOOTER')
win=pygame.display.set_mode((width,height))
#load images
RED_SS=pygame.transform.scale(pygame.image.load(os.path.join('assets','pixel_Enemyred.png')),(100,100))
GREEN_SS=pygame.transform.scale(pygame.image.load(os.path.join('assets','pixel_Enemygreen.png')),(100,100))
BLUE_SS=pygame.transform.scale(pygame.image.load(os.path.join('assets','pixel_Enemyblue.png')),(100,100))
YELLOW_SS=pygame.transform.scale(pygame.image.load(os.path.join('assets','pixel_mainship.png')),(100,100))

#load lasers
Red_laser=pygame.transform.scale(pygame.image.load(os.path.join('assets','red_laser.png')),(13,37))
Green_laser=pygame.transform.scale(pygame.image.load(os.path.join('assets','green_laser.png')),(14,37))
Yellow_laser=pygame.image.load(os.path.join('assets','pixel_laser_yellow.png'))
Blue_laser=pygame.transform.scale(pygame.image.load(os.path.join('assets','blue_laser.png')),(15,37))

#load bg
BG=pygame.transform.scale(pygame.image.load(os.path.join('assets','background-black.png')),(width,height))

class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y+=vel

    def off_screen(self,height):
        return  not(self.y<=height and self.y>=0)

    def collision(self,obj):
        return collide(self,obj)

class Ship:
    COOLDOWN=30
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers= []
        self.cool_down_counter=0

    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health-=5
                self.lasers.remove(laser)
    
    def cooldown(self):
        if self.cool_down_counter>= self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x , self.y ,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter=1

    def get_width(self):
        return self.ship_img .get_width()

    def get_height(self):
        return self.ship_img.get_height()
       
class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img=YELLOW_SS
        self.laser_img=Yellow_laser
        self.mask= pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj ):
                        objs.remove(obj)
                                                
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height() +10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height() +10,self.ship_img.get_width()*(self.health/self.max_health),10))                 
   
class Enemy(Ship):
    color_map={'red':(RED_SS,Red_laser)   ,  'green':(GREEN_SS,Green_laser)  , 'blue':(BLUE_SS,Blue_laser)}

    def __init__(self, x, y , color , health=100):
        super().__init__(x, y, health)
        self.ship_img,self.laser_img=self.color_map[color]
        self.mask=pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y+=vel

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x-10 , self.y ,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter=1

def collide(obj1,obj2):
    offset_x=obj2.x - obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None

def main():
    score = 0
    run= True
    FPS=60
    level=0
    lives=5
    enemies=[]
    enemy_vel=1
    wave_length= 5
    elen = len(enemies)

    main_font=pygame.font.SysFont('Brush Script MT',50)
    lost_font=pygame.font.SysFont('Brush Script MT',60)
    player_vel=8
    lost=False
    lost_count=0
    player=Player(300,650)
    laser_vel=10
    clock=pygame.time.Clock()

    def redraw_window():
        win.blit(BG,(0,0))
        #draw text in it
        score_label=main_font.render(f'Score:{score}',1,(255,255,255)) 
        level_label=main_font.render(f'levels:{level}',1,(255,255,255))
        lives_label=main_font.render(f'lives:{lives}',1,(255,255,255))
        win.blit(lives_label,(10,10))
        win.blit(level_label,(width-lives_label.get_width()-25,10))
        win.blit(score_label,((width/2)-50,10)) 

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)
        if lost :
            lost_label=lost_font.render('You Lost!!',1,(255,255,255))
            win.blit(lost_label,(width/2-lost_label.get_width()/2,350))
    
    
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        if player.health==0:
            lives=lives-1
            player.health=player.max_health
        
        if lives==0 :
            lost=True
            lost_count+=1
        if lost:
            if lost_count>FPS*3:
                run=False
            else:
                continue

        if len(enemies)==0:
            level+=1
            wave_length+=5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(['red','green','blue']))
                enemies.append(enemy)
        
        for i in pygame.event.get():
            if i.type==pygame.QUIT:
                quit()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT ] and player.x - player_vel > 0:
            player.x-=player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel+player.get_width()<width:
            player.x+=player_vel
        if keys[pygame.K_UP] and player.y - player_vel>0:
            player.y-=player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height()+15< height:
            player.y+=player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if len(enemies) != elen:
                score += 5
                elen = len(enemies)

            if random.randrange(0,2*FPS)==0:
                enemy.shoot()

            if collide(enemy,player):
                player.health-=10            
                enemies.remove(enemy)
                score += 5
                
            elif enemy.y + enemy.get_height() > height:
                lives-=1
                enemies.remove(enemy)
        player.move_lasers(-laser_vel,enemies)

def main_menu():
    title_font=pygame.font.SysFont('Brush Script MT',60)
    run=True
    while run:
        win.blit(BG,(0,0))
        title_label=title_font.render("Click to start!!",1,(255,255,255))
        win.blit(title_label,(width/2-title_label.get_width()/2,350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run= False
            if event.type==pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()       
main_menu()