import pygame, sys, os, time, math
from pygame.locals import *
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((900, 600))
timer1 = 0
timer2 = 0

#music = pygame.mixer.music.load('sound/fighttheme.mp3')
#pygame.mixer.music.play(-1)
#hit_sound = pygame.mixer.sound('aua.wav')
# hammer_sound = pygame.mixer.Sound('sound/hammer.wav')
# fireball_sound = pygame.mixer.Sound('sound/fireball.wav')e

mage_score = 0
warrior_score = 0
font = pygame.font.SysFont('comicsans', 40, True)
#mage_score_l = font.render(("Mage:" +str(mage_score)),1,(255,0,0),(0,0,0))
# mage_score_l = font.render('Mage:' + str(mage_score), 1, (0,0,0))
# warrior_score_l = font.render('Warrior:' + str(warrior_score), 1, (0,0,0))
isJump = False
jumpCount = float(50)
sun = pygame.image.load('img/sunun.png')
fireball = pygame.image.load('img/fireball.png')
hammer = pygame.image.load('img/hammer.png')

bullets=[]
bulletCount=0

# def restart():
#    if keys_putting[pygame.K_j]:
#          mage_health=10
#          warrior_health=10

def blit():
   global mage_score, warrior_score
   mage_score_l = font.render('Mage:' + str(mage_score), 1, (0,0,0))
   warrior_score_l = font.render('Warrior:' + str(warrior_score), 1, (0,0,0))  
   screen.blit(moja_grafika, (0,0))
   if mage_health >0:
      screen.blit(mage, (mage_class.x, mage_class.y))
      pygame.draw.rect(window, (255,0,0), (mage_class.x - 15, mage_class.y, 150, 5))
      pygame.draw.rect(window, (0,255,0), (mage_class.x - 15, mage_class.y, 150 - (15 * (10 - mage_health)), 5))      
   else: 
      screen.blit(dead_mage, (mage_class.x, mage_class.y + 20))
      #warrior_score += 1
      

   if warrior_health >0:
      screen.blit(warrior,(warrior_class.x, warrior_class.y))
      pygame.draw.rect(window, (255,0,0), (warrior_class.x, warrior_class.y, 150, 5))
      pygame.draw.rect(window, (0,255,0), (warrior_class.x, warrior_class.y, 150 - (15 * (10 - warrior_health)), 5))
   else: 
      screen.blit(dead_warrior, (warrior_class.x, warrior_class.y - 20))
      #mage_score += 1

   screen.blit(sun, (-50,-40))
   screen.blit(warrior_score_l, (750, 35))
   screen.blit(mage_score_l, (750,10))
   for bullet in bullets:
      bullet.show()

   pygame.display.flip()

class Player(object):
   def __init__(self,x,y):
     self.x = x
     self.y = y

mage_class = Player(700, 450)
mage = pygame.image.load('img/mage.png')
dead_mage = pygame.image.load('img/meat.png')

warrior_class = Player(50,450)
warrior = pygame.image.load('img/warrior.png')
dead_warrior = pygame.image.load('img/ashez.png')

mage_health = 10
mage_visible = True
warrior_health = 10
warrior_visible = True

class projectile(object):
    def __init__(self,x,y,image,facing):
        self.x = x
        self.y = y+75
        self.facing = facing
        self.image = image
        self.vel = 8 * facing

    def show(self):
         screen.blit(self.image,(self.x,self.y))
         
def collision(warriorX, warriorY, mageX, mageY):
   distance = math.sqrt((math.pow(warriorX - mageX,2)) + (math.pow(warriorY - mageY,2)))
   if warriorY != mageY:
      if distance < 45:
         return True
      else:
         return False 

# ustawiamy etykietę
pygame.display.set_caption('Grand Battle for Honor')

# ładujemy plik graficzny
moja_grafika = pygame.image.load('img/bg.jpg')

# pobieramy informacje o ekranie - tle
screen = pygame.display.get_surface()

# przypisanie grafiki do określonego miejsca ekranu
screen.blit(moja_grafika, (0,0))

while True:

   #checking inputs
   keys_putting = pygame.key.get_pressed()

   for event in pygame.event.get():
      if event.type == QUIT:
         sys.exit(0)
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
         sys.exit(0)

   for bullet in bullets:
      if bullet.x < 900 and bullet.x > 0:
         bullet.x += bullet.vel  
      else:
         bullets.pop(bullets.index(bullet))
         bulletCount -= 1

   #korekty startu pociskow
   if (warrior_class.x<mage_class.x):
      facing = 1
      cor1= 90
      cor2= 0
   else:
      facing = -1
      cor1= -20
      cor2= 120
   
   #WARRIOR MOVEMENT AND FALLING
   if warrior_class.y < 450:
      warrior_class.y+=2.1

   if keys_putting[pygame.K_d] and warrior_class.x < 785:
      warrior_class.x += 1
   if keys_putting[pygame.K_a] and warrior_class.x > 0:
      warrior_class.x -= 1
   if keys_putting[pygame.K_e]:
 #      if len(bullets)<2:
        if timer1>45 :
         # hammer_sound.play()
         bullets.append(projectile(warrior_class.x+cor1,warrior_class.y,hammer,facing))
         bulletCount += 1
         timer1=0

   if not (isJump):
      if keys_putting[pygame.K_w] and warrior_class.y > 260:
         isJump = True
   else:
      if jumpCount >= 50:
         mage_class.y -= jumpCount * float(0.3) 
         jumpCount -= 1    
      else:
         isJump = False
         jumpCount = 50

   #MAGE MOVEMENT AND FALLING
   if mage_class.y < 450:
      mage_class.y +=2.1

   if keys_putting[pygame.K_RIGHT] and mage_class.x < 795:
      mage_class.x += 1
   if keys_putting[pygame.K_LEFT] and mage_class.x > -10:
      mage_class.x -= 1
   if keys_putting[pygame.K_RSHIFT]:
       if timer2>45:
         # fireball_sound.play()
         bullets.append(projectile(mage_class.x+cor2,mage_class.y,fireball,facing*(-1)))
         bulletCount += 1
         timer2=0
   if not (isJump):
      if keys_putting[pygame.K_UP] and mage_class.y > 260:
         isJump = True
   else:
      if jumpCount >= 50:
         warrior_class.y -= jumpCount * float(0.3) 
         jumpCount -= 1    
      else:
         isJump = False
         jumpCount = 50
   if keys_putting[pygame.K_j] and (mage_health<=0 or warrior_health<=0):
         if mage_health<=0:
            warrior_score+=1
         if warrior_health<=0:
            mage_score+=1
         mage_health=10
         warrior_health=10

   #bullet_collision = collision(warrior_collisionX, warrior_collisionY, mage_collisionX, mage_collisionY)

   for i in range(0,bulletCount):
      warriorHit = collision(bullets[i-1].x+22, bullets[i-1].y+22, warrior_class.x + 58, warrior_class.y+60)
      mageHit = collision(bullets[i-1].x+22, bullets[i-1].y+22, mage_class.x + 60, mage_class.y+60)
      if warriorHit:
         # print("War")
         bullets.pop(i-1)
         bulletCount-=1
         warrior_health > 0
         warrior_health -= 1
      else:
         warrior_visible = False  

      if mageHit:
         # print("Mage")
         bullets.pop(i-1)
         bulletCount-=1
         mage_health > 0
         mage_health -= 1
      else:
         maga_visible = False
            
   timer1 += 1
   timer2 += 1

   blit()

