add_library('minim')
import os, time
path=os.getcwd()
player = Minim(this)

class Creature:
    def __init__(self,x,y,r,g,img,w,h,F):
        self.x=x # X position
        self.y=y # Y position
        self.r=r # Radius
        self.g=g # Ground level
        self.vx=0 # Change of x
        self.vy=0 # Change of y
        self.w=w # Width of image
        self.h=h # Height of image
        self.F=F # Frame count
        self.f=0 # Cycles through frames
        self.img = loadImage(path+"/images/"+img)
        self.dir = 1 # Direction of image
    
    def gravity(self):
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0 #-10
            
        for p in game.platforms:
            if self.x in range(p.x, p.x+p.w) and self.y+self.r <= p.y:
                self.g = p.y
                break
            else:
                self.g = game.g
    
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
        
        if self.y >= game.h/2 and self.vy > 0:
            game.y += self.vy
        elif self.y >= game.h/2 and self.vy < 0:
            game.y += self.vy
        
    def display(self):
        self.update()
        
        if isinstance (self, Bat):
            self.f = (self.f+0.3)%self.F
        elif self.vx != 0:
            self.f = (self.f+0.3)%self.F
        else:
            self.f = 3
            
        if self.dir > 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
            
        strokeWeight(5)
        stroke(255)
        noFill()
        ellipse(self.x-game.x,self.y-game.y,2*self.r,2*self.r)

class Enemy(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,dmg,health): 
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.dmg = dmg
        self.health = health
            
class Quote(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.recentlyDamaged = False
        self.inDialog = False
        self.timerSet = False
        self.startTime = time.time()
        self.endTime = time.time()
        self.currentLives = 3
        self.currentLevel = 1
        self.currentHealth = 100
        self.currentXP = 0
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}
    def update(self):
        self.gravity()
        
        if self.keyHandler[LEFT]:
            self.vx = -5
            self.dir = -1
        elif self.keyHandler[RIGHT]:
            self.vx = 5
            self.dir = 1
        else:
            self.vx = 0
        
        if self.keyHandler[UP] and self.y+self.r == self.g:
            self.vy = -10
        
        self.x += self.vx
        self.y += self.vy

        if self.x > game.w/2:
            game.x += self.vx
            
        if self.y >= game.h/2:
            game.y += self.vy
        elif self.y <= game.h/2:
            game.y += self.vy
        
        # On player collision
        for e in game.enemies:
            if self.distance(e) <= self.r + e.r: # Update the timer on every collision
                self.endTime = time.time()
            if round(self.endTime - self.startTime, 1) >= 1: # You can only get damaged once per second
                self.recentlyDamaged = False
            
            if self.distance(e) <= self.r + e.r and self.recentlyDamaged == False: # If you hit an enemy, you take damage
                self.currentHealth -= e.dmg
                self.recentlyDamaged = True
                self.startTime = time.time()
                if self.currentHealth <= 0 and self.currentLives > 0:
                    self.currentLives -= 1
                    self.currentHealth = 100

        for g in game.guns:
            if self.distance(g) <= self.r + g.r:
                game.equippedGuns.append(g) # Removes it from the floor, adds it to the equipped list
                game.guns.remove(g)
                del g
                game.gunAcquired = True
                game.quote = Quote(200,525,75,self.g,"quotewithPS.png",128,120,4)
                
        for x in game.xpdrops:
            if self.distance(x) <= self.r + x.r:
                self.currentXP += 40
                game.xpdrops.remove(x)
                del x
                self.levelUp()
                
    def levelUp(self):
        if self.currentXP >= 100:
            self.currentLevel += 1
            self.currentXP = self.currentXP - 100 # Extra XP carries over
            game.equippedGuns[0].dmg += 2 # Leveling up increases gun damage
                
        # for n in game.npcs:
        #     if self.distance(n) <= self.r + n.r and self.inDialog == True and self.midDialog == False:
        #         self.midDialog = True
        #         print('in dialog')
        #         game.display()
        #         break
    
    def distance(self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class NPC(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)    
        
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy

class DialogBox:
    def __init__(self,x,y,w,h, img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img = loadImage(path+"/images/"+img)
        
    def display(self):
        textSize(80)
        fill(0)
        rect(self.x, self.y, self.w, self.h)
        image(self.img, self.x, self.y)
        fill(255)
        text("Hi Quote!", self.x + 200, self.y + 100)

class Bat(Enemy):
    def __init__(self,x,y,r,g,img,w,h,F,y1,y2,dmg,health):
        Enemy.__init__(self,x,y,r,g,img,w,h,F,dmg,health)
        self.y1=y1
        self.y2=y2
        self.dir = -1
        
    def update(self):
        
        if self.y < self.y1:
            self.vy = 3
        elif self.y > self.y2:
            self.vy = -3
            
        self.y += self.vy

class Platform:
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h 
        self.img = loadImage(path+"/images/stonetile.png")
        
    def display(self):
        image(self.img,self.x-game.x,self.y-game.y, self.w, self.h) 

class Item:
    def __init__(self,x,y,r,g,img,w,h):
        self.x=x
        self.y=y
        self.r=r
        self.g=g
        self.vx=0
        self.vy=0
        self.w=w
        self.h=h
        print(img)
        self.img = loadImage(path+"/images/"+img)
        
    def gravity(self):
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0 #-10
            
        for p in game.platforms:
            if self.x in range(p.x, p.x+p.w) and self.y+self.r <= p.y:
                self.g = p.y
                break
            else:
                self.g = game.g

    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy    
    
    def display(self):
        self.update()
        image(self.img,self.x - game.x,self.y - game.y)
        
        strokeWeight(5)
        stroke(255)
        noFill()
        ellipse(self.x - game.x,self.y - game.y,2*self.r,2*self.r)

class Gun(Item): # Almost the same as Creature, but without needing frame count.
    def __init__(self,x,y,r,g,img,w,h,dmg,fireRate):
        Item.__init__(self,x,y,r,g,img, w,h)
        self.vx = 0
        self.vy = 0
        self.dmg = dmg
        self.fireRate = fireRate
        self.gunReloading = False
        self.reloadStart = time.time()
        self.reloadEnd = time.time()
        
    def fire(self):    
        if self.gunReloading == False:
            game.bullets.append(Bullet(game.quote.x+game.quote.dir*game.quote.r,game.quote.y,50,1,"polarstarbullet.png",116,90,1,game.quote.dir*8))
            self.gunReloading = True
            self.reloadStart = time.time()
            self.reload()
        
    def reload(self):
        if (self.reloadEnd - self.reloadStart) >= self.fireRate:
            self.gunReloading = False
        
class XPDrop(Item):
    def __init__(self,x,y,r,g,img, w,h):
        Item.__init__(self,x,y,r,g,img, w,h)
        self.vx = 0
        self.vy = 0

class Bullet(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,vx):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.vx = vx
        self.dir = vx
        self.ttl = 60
        
    def update(self):
        # self.dmgNumberEnd = time.time()
        self.x += self.vx
        self.ttl -= 1
        
        if self.ttl == 0:
            game.bullets.remove(self)
            del self
            return
                
        for e in game.enemies:
            if self.distance(e) <= self.r + e.r: # If a bullet hits an enemy, the enemy takes damage
                e.health -= game.equippedGuns[0].dmg                    
                # self.dmgNumberStart = time.time()
                game.enemyHit = True
                # textSize(48)
                # fill(255)
                # text(str(game.equippedGuns[0].dmg), e.x - 10, e.y - 10)
                game.bullets.remove(self)
                del self
                if e.health <= 0:
                    game.enemies.remove(e)
                    for i in range(3):
                        game.xpdrops.append(XPDrop(e.x - i*25, e.y, 23, game.g, "xpdrop.png", 46, 46))
                    del e
                                    
    def distance(self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
        
class Game:
    def __init__ (self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.x = 0
        self.y = 0
        self.gunAcquired = False
        self.quote = Quote(50,self.g,75,self.g,"quote.png",120,120,4)
        self.npcs = []
        self.npcs.append(NPC(200,50,75,self.g, "curlybrace.png",125,125,6))
        self.enemies = []
        self.enemies.append(Bat(300,50,35,self.g,"bat.png",80,80,6,200,500,5,20))
        self.guns = [] # Guns lying on the ground
        self.guns.append(Gun(200,570,30,self.g - 20,"polarstar.png",109,75, 5, 0.1)) 
        self.equippedGuns = [] # Guns equipped by the player   
        self.bullets = []
        self.dmgNumberStart = 0
        self.enemyHit = False
        self.xpdrops = []
        self.dialogBox = DialogBox(100, 100, 700, 175, "curlybraceFace.png")
        self.platforms=[]
        for i in range(5):
            self.platforms.append(Platform(250+i*250,450-150*i,200,50))
        
    def display(self):
        stroke(255)
        line(0,self.g - self.y,self.w,self.g - self.y)
            
        self.quote.display()
        if self.quote.inDialog == True:
            self.dialogBox.display()
            
        for p in self.platforms:
            p.display()
                    
        for g in self.guns:
            g.display()

        for e in self.enemies:
            e.display()
            
        for b in self.bullets:
            b.display()
            # print(self.enemyHit)
            # if self.enemyHit == True or self.dmgNumberStart != 0:
            #     print('in loop')
            #     self.dmgNumberStart = time.time()
            #     textSize(48)
            #     fill(255)
            #     text(str(game.equippedGuns[0].dmg), b.x - 10, b.y - 10)
            #     game.bullets.remove(b)
            #     del b
            # if time.time() == self.dmgNumberStart + 2:
            #     self.enemyHit = False
            
            
        for n in self.npcs:
            n.display()
            
        for x in self.xpdrops:
            x.display()
        
        # Experience bar; starts empty
        fill(102,0,51) # Colour of the full bar
        rect(50,30,100,20) # The full bar
        fill(255,255,0) # Colour of the current progress
        rect(50,30,min(self.quote.currentXP * 1, 100), 20) # Current progress
        
        # Health bar; starts full
        fill(102,0,51) # Colour of the full bar
        rect(50,60,100,20) # The full bar
        fill(255,0,0) # Colour of the current progress
        rect(50,60,min(self.quote.currentHealth * 1, 100), 20) # Current progress

        # Current level; starts at 1
        textSize(36)
        fill(255)
        text(str(game.quote.currentLevel), 20, 50)        
                        
        # Current lives; starts at 3
        textSize(36)
        fill(255)
        text(str(game.quote.currentLives), 20, 80)
        
game = Game(1024,768,600)

def setup():
    size(game.w, game.h)
    background(0)
    
def draw():
    background(100)
    game.display()
    for g in game.equippedGuns:
        if g.gunReloading == True:
            g.reloadEnd = time.time()
            g.reload() # Updates reload timer until gun is reloaded.
    if game.quote.currentLives == 0:
        game.__init__(1024,768,600)
        game.display()
        
    
def keyPressed():
    # if game.quote.y+game.quote.r == game.quote.g: # Disallows movement when mid-air. WIP.
    if keyCode == LEFT:
        game.quote.keyHandler[LEFT]=True
    elif keyCode == RIGHT:
        game.quote.keyHandler[RIGHT]=True
    elif keyCode == UP:
        game.quote.keyHandler[UP]=True
    elif keyCode == 32 and game.gunAcquired == True:
        for g in game.equippedGuns:
            g.fire()
    elif key == ENTER:
        for n in game.npcs:
            if (game.quote.distance(n) <= game.quote.r + n.r and game.quote.inDialog == True) or game.quote.inDialog == True: # If in dialog, close dialog box.
                game.quote.inDialog = False
                game.display()
            elif game.quote.distance(n) <= game.quote.r + n.r and game.quote.inDialog == False: # If not in dialog and near an NPC, open dialog box.
                game.quote.inDialog = True
                game.display()
                break


def keyReleased():
    if keyCode == LEFT:
        game.quote.keyHandler[LEFT]=False
    elif keyCode == RIGHT:
        game.quote.keyHandler[RIGHT]=False   
    elif keyCode == UP:
        game.quote.keyHandler[UP]=False
