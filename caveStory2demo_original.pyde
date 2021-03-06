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
        self.leftCollided = False # These values are here as fallbacks, in case a movement check happens before hitWall is called
        self.rightCollided = False
        self.topCollided = False
        self.bottomCollided = False
    
    def gravity(self):
                
        for t in game.tiles:
            self.hittingWall = self.hitWall(self.x, self.y, self.r, t.x, t.y, t.w, t.h)
            if self.hittingWall == True:
                if self.topCollided == True: # Only set gravity to tile y if collided from the top, else reset to ground level; this fixes gravity
                    self.g = t.y
                    break
                else:
                    self.g = game.g
                    break
            elif self.hittingWall == False:
                self.g = game.g   
                
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0        
                
        for t in game.tiles: # Bounce back down off tile's bottom
            if self.bottomCollided == True:
                self.vy = 0.1
                
    
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
            self.f = (self.f+0.5)%self.F
        elif self.vx != 0:
            self.f = (self.f+0.5)%self.F
        else:
            self.f = 3
            
        if self.dir > 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
            
        # strokeWeight(5)
        # stroke(255)
        # noFill()
        # ellipse(self.x-game.x,self.y-game.y,2*self.r,2*self.r) # Used throughout making the game to check hitboxes
        
    def hitWall(self,x,y,r,x1,y1,w,h): # Checks for collision with tiles
        # Test values
        self.testX = x
        self.testY = y
    
        # Check sides and set type of collision
        if x <= x1:
            self.testX = x1
            self.leftCollided = True
        elif x >= x1+w:
            self.testX = x1+w 
            self.rightCollided = True
        if y <= y1:
            self.testY = y1
            self.topCollided = True
        elif y >= y1+h:
            self.testY = y1+h
            self.bottomCollided = True
    
        # Calculate distance
        self.distX = x-self.testX
        self.distY = y-self.testY
        distance = sqrt((self.distX ** 2) + (self.distY ** 2))
        
        # Collision
        if distance <= r:

            if self.leftCollided == True:
                self.rightCollided = False
                #print('Left collision')
                return True
            elif self.rightCollided == True:
                self.leftCollided = False
                #print('Right collision')
                return True
            elif self.topCollided == True:
                self.bottomCollided = False
                #print('Top collision')
                return True
            elif self.bottomCollided == True:
                self.topCollided = False
                #print('Bottom collision')
                return True
        
        # If there's no collision, reset the values
        self.rightCollided = False
        self.leftCollided = False
        self.topCollided = False
        self.bottomCollided = False
        return False

class Enemy(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,dmg,health): 
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.dmg = dmg
        self.health = health
            
class Quote(Creature):
    def __init__(self,x,y,r,g,img,w,h,F, currentLives):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.recentlyDamaged = False
        self.startingDialog = False
        self.midDialog = False
        self.rightCollided = False
        self.leftCollided = False
        self.selectedNPC = None
        self.timerSet = False
        self.startTime = time.time()
        self.endTime = time.time()
        self.currentLives = currentLives
        self.currentLevel = 1
        self.currentHealth = 100
        self.maxHealth = 100
        self.currentXP = 0
        self.displayedXP = 0 # Specifically for the XP display
        self.maxXP = 300
        self.keyHandler={LEFT:False, RIGHT:False, UP:False}
        self.xpCollected = player.loadFile(path+"/sounds/xpCollected.mp3")
    def update(self):
        self.gravity()

        for t in game.tiles:
            self.hittingWall = self.hitWall(self.x, self.y, self.r, t.x, t.y, t.w, t.h)
            if self.hittingWall == True:
                break
        if self.keyHandler[LEFT] and self.rightCollided == False and self.x > 50: # Can't move if you're at a wall or at the edges of the game area
            self.vx = -7
            self.dir = -1
        elif self.keyHandler[RIGHT] and self.leftCollided == False and self.x < 6500:
            self.vx = 7
            self.dir = 1
        else:
            self.vx = 0
        
        if self.keyHandler[UP] and (self.y+self.r == self.g or self.y+self.r >= self.g - 5 or self.y+self.r >= self.g + 5): # Added some leeway to the calculation so you can jump on tiles
            self.vy = -10
        
        self.x += self.vx
        self.y += self.vy

        if self.x > game.w/2:
            game.x += self.vx
            
        if self.y >= game.h/2:
            game.y += self.vy
            game.setY = game.y # The camera resets to this variable
        elif self.y <= game.h/2:
            game.y += self.vy
            game.setY = game.y # The camera resets to this variable
        
        # On player collision
        for e in game.enemies:
            if self.distance(e) <= self.r + e.r: # Update the timer on every collision
                self.endTime = time.time()
            if round(self.endTime - self.startTime, 1) >= 1: # You can only get damaged once per second
                self.recentlyDamaged = False
            
            if self.distance(e) <= self.r + e.r and self.recentlyDamaged == False: # If you hit an enemy, you take damage
                self.currentHealth -= e.dmg
                textSize(48)
                fill(255)
                text(str(e.dmg), self.x - 10, self.y - 10)
                self.recentlyDamaged = True
                self.startTime = time.time()
                if self.currentHealth <= 0 and self.currentLives > 0:
                    self.currentLives -= 1
                    self.currentHealth = self.maxHealth
        
        for s in game.spikes:
            if self.distance(s) <= self.r + s.r: # Update the timer on every collision
                self.endTime = time.time()
            if round(self.endTime - self.startTime, 1) >= 1: # You can only get damaged once per second
                self.recentlyDamaged = False
            
            if self.distance(s) <= self.r + s.r and self.recentlyDamaged == False: # If you hit an enemy, you take damage
                self.currentHealth -= s.dmg
                textSize(48)
                fill(255)
                text(str(s.dmg), self.x - 10, self.y - 10)
                self.recentlyDamaged = True
                self.startTime = time.time()
                if self.currentHealth <= 0 and self.currentLives > 0:
                    self.currentLives -= 1
                    self.currentHealth = self.maxHealth
                    
        for b in game.bossBullets:
            if self.distance(b) <= self.r + b.r: # Update the timer on every collision
                self.endTime = time.time()
            if round(self.endTime - self.startTime, 1) >= 1: # You can only get damaged once per second
                self.recentlyDamaged = False
            
            if self.distance(b) <= self.r + b.r and self.recentlyDamaged == False: # If you hit an enemy, you take damage
                self.currentHealth -= b.dmg
                textSize(48)
                fill(255)
                text(str(b.dmg), self.x - 10, self.y - 10)
                # self.currentXP -= 10
                # self.displayedXP -= 10
                self.recentlyDamaged = True
                self.startTime = time.time()
                game.bossBullets.remove(b)
                del b
                if self.currentHealth <= 0 and self.currentLives > 0:
                    self.currentLives -= 1
                    self.currentHealth = self.maxHealth

        for g in game.guns:
            if self.distance(g) <= self.r + g.r:
                game.equippedGuns.append(g) # Removes it from the floor, adds it to the equipped list
                game.guns.remove(g)
                del g
                game.gunAcquired = True
                self.ogPosX = game.quote.x
                self.ogPosY = game.quote.y
                game.quote = Quote(self.ogPosX,self.ogPosY,70,self.g,"quotewithPS.png",128,120,4, self.currentLives)
                
        for x in game.xpdrops:
            if self.distance(x) <= self.r + x.r:
                if self.currentXP + 30 <= self.maxXP: # Can only get XP to a certain level
                    self.currentXP += 30
                    self.displayedXP += 30
                    self.levelUp()
                self.xpCollected.rewind()
                self.xpCollected.play()
                game.xpdrops.remove(x)
                del x
                
        for h in game.heartdrops:
            if self.distance(h) <= self.r + h.r:
                self.currentHealth = 100
                game.heartdrops.remove(h)
                self.xpCollected.rewind()
                self.xpCollected.play()
                del h
                
        for h in game.heartcapsules:
            if self.distance(h) <= self.r + h.r:
                self.currentLives += 1
                game.heartcapsules.remove(h)
                del h
                
    def levelUp(self):
        if self.currentXP >= 100 * self.currentLevel:
            self.currentLevel += 1
            self.displayedXP = self.displayedXP - 100 # Extra XP carries over
            game.equippedGuns[0].dmg += 2 # Leveling up increases gun damage
    
    def distance(self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5
    
    def getNPC(self):
        for n in game.npcs:
            if self.distance(n) <= self.r + n.r:
                self.selectedNPC = n.name
                break

class NPC(Creature):
    def __init__(self,x,y,r,g,img,w,h,F, name):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.name = name    
        
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        image(self.img,self.x-self.r-game.x,self.y-self.r-game.y, self.w, self.h)

class DialogBox:
    def __init__(self,x,y,w,h,speaker,img,msg,txtSize):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.speaker = speaker # NPC's name who says the dialog
        self.img = loadImage(path+"/images/"+img) # NPC's image
        self.msg = msg
        self.txtSize = txtSize
        
    def display(self):
        self.txtSizeCalc = 60 - len(self.msg)
        textSize(self.txtSizeCalc)
        fill(0)
        rect(self.x, self.y, self.w, self.h)
        image(self.img, self.x, self.y)
        fill(255)
        text(self.msg, self.x + 200, self.y + 100)

class Spikes(Enemy):
    def __init__(self,x,y,r,g,img,w,h,F,dmg,health):
        Enemy.__init__(self,x,y,r,g,img,w,h,F,dmg,health)
        
    def display(self):
        image(self.img,self.x-self.r-game.x,self.y-self.r-game.y, self.w, self.h)

class Bat(Enemy):
    def __init__(self,x,y,r,g,img,w,h,F,y1,y2,dmg,health):
        Enemy.__init__(self,x,y,r,g,img,w,h,F,dmg,health)
        self.y1=y1
        self.y2=y2
        self.dir = -1
        self.timer = time.time()
        self.initial_y = self.y
        
    def update(self):
        new_y = 100*sin(10* (self.timer - time.time())/(2*PI)) + 0.5 * self.initial_y
        self.y = new_y
        for t in game.tiles:
            self.hittingWall = self.hitWall(self.x, self.y, self.r, t.x, t.y, t.w, t.h)
            if self.hittingWall == True:
                break
        if self.topCollided == True:
            self.vy = -3
        elif self.bottomCollided == True:
            self.vy = 3
        elif self.y < self.y1:
            self.vy = 3
        elif self.y > self.y2:
            self.vy = -3
            
        self.y += self.vy

class Critter(Enemy):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2,dmg,health):
        Enemy.__init__(self,x,y,r,g,img,w,h,F,dmg,health)
        self.x1=x1
        self.x2=x2
        self.vx = 2
        self.jump = player.loadFile(path+"/sounds/critterJump.mp3")
        
    def update(self):
        self.gravity()
        for t in game.tiles:
            self.hittingWall = self.hitWall(self.x, self.y, self.r, t.x, t.y, t.w, t.h)
            if self.hittingWall == True:
                break
        
        if int(random(50)) == 1 and self.y+self.r == self.g and game.quote.distance(self) <= 2 * (game.quote.r + self.r):
            self.vy = -10
            self.jump.rewind()
            self.jump.play()
        if self.leftCollided == True: # Checks collisions first, then regular movement
            self.vx = -2
        elif self.rightCollided == True:
            self.vx = 2
        elif self.x > self.x2:
            self.vx = -2
            self.dir = -1
        elif self.x < self.x1:
            self.vx = 2
            self.dir = 1
        
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        if self.dir > 0: # WIP; make sprite change directions
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h, 0, 0, 98, 98)
        elif self.dir < 0:
            image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h, 0, 0, 98, 98)
        
        if game.quote.distance(self) <= 2 * (game.quote.r + self.r):
            self.update()
            if self.dir > 0:
                image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,98,0,196,196)
            elif self.dir < 0:
                image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,98,0,196,196)
         
        if self.vy != 0:
            if self.dir > 0:
                image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,196,0,294,294)
            elif self.dir < 0:
                image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,196,0,294,294)
            
class Tile:
    def __init__(self,x,y,w,h,r,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h 
        self.r=r
        self.img = loadImage(path+"/images/"+img)
        
    def display(self):
        image(self.img,self.x-game.x,self.y-game.y, self.w, self.h) 

class Platform(Tile):
    def __init__(self,x,y,w,h,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h 
        self.img = loadImage(path+"/images/"+img)

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
        self.img = loadImage(path+"/images/"+img)
    
    def gravity(self):
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.vy > self.g - (self.y+self.r):
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0 #-10
            
        for t in game.tiles:
            if self.x in range(t.x, t.x+t.w) and self.y+self.r <= t.y:
                self.g = t.y
                break
            else:
                self.g = game.g

    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy    
    
    def display(self):
        self.update()
        image(self.img,self.x - self.r - game.x,self.y - self.r - game.y)

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
        self.shotSound = player.loadFile(path+"/sounds/polarStarSound.mp3")
        
    def fire(self):
        for t in game.tiles: # Fixes bug that let you shoot through walls when you were standing against them
            self.hittingWall = game.quote.hitWall(game.quote.x, game.quote.y, game.quote.r, t.x, t.y, t.w, t.h)
        if self.gunReloading == False and game.quote.leftCollided == False and game.quote.rightCollided == False:
            game.bullets.append(Bullet(game.quote.x+game.quote.dir*game.quote.r,game.quote.y + 30,10,1,"polarstarbullet.png",116,90,1,game.quote.dir*8, 0, game.equippedGuns[0].dmg, "quote"))
            self.shotSound.rewind()
            self.shotSound.play()
            self.gunReloading = True
            self.reloadStart = time.time()
            self.reload()
        
    def reload(self):
        if (self.reloadEnd - self.reloadStart) >= self.fireRate:
            self.gunReloading = False

class Boss(Enemy):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2,dmg,health):
        Enemy.__init__(self,x,y,r,g,img,w,h,F,dmg,health)
        self.x1=x1
        self.x2=x2
        self.vx = 5
        self.maxHealth = health
        self.bossRecharging = False
        self.rechargeStart = time.time()
        self.rechargeEnd = time.time()
        self.turnCount = 0
        
    def update(self):
        #self.gravity()
        # for t in game.tiles:
        #     self.hittingWall = self.hitWall(self.x, self.y, self.r, t.x, t.y, t.w, t.h)
        #     if self.hittingWall == True:
        #         break
        
        # if self.leftCollided == True: # Checks collisions first, then regular movement
        #     self.vx = -2
        # elif self.rightCollided == True:
        #     self.vx = 2
        
        #if self.x > self.x2:
        if self.turnCount % 15 == 0: # Moves to the middle for the circle attack
            self.bossRecharging = True # Doesn't shoot until in position
            if self.x > 5900:
                self.vx = - 10
            if self.x < 5900:
                self.vx = 10
            else:
                self.bossRecharging = False
        else:
            if self.health > 0:
                if self.x > game.quote.x:
                    if self.health < 10:
                        self.vx = -5
                    else:
                        self.vx = max(-500.0/self.health, -5) # Moves quicker as health decreases
                        self.dir = -1
                elif self.x < game.quote.x:
                    if self.health < 10:
                        self.vx = 5
                    else:
                        self.vx = min(500.0/self.health, 5)
                        self.dir = 1
                else:
                    self.vx = 0
        
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h)
                                 
        if self.health > 0:
            self.fire()
        else: # Falls to the ground on death
            self.vx = 0
            self.gravity()
        
        if self.health <= 0:
            if game.wantMusic == True:
                game.bossMusic.pause()
            game.npcs.append(NPC(self.x,self.y,62,self.g, "misery.png",125,125,6, "miserydef"))
            game.bossBattle = False
        
    def fire(self):
        for t in game.tiles: # Fixes bug that let you shoot through walls when you were standing against them
            self.hittingWall = game.quote.hitWall(game.quote.x, game.quote.y, game.quote.r, t.x, t.y, t.w, t.h)
        if self.bossRecharging == False:
            if self.turnCount % 15 == 0: # Circle attack every 15 turns
                for i in range(0, 11, 5):
                    for j in range(0, 11, 5):
                        game.bossBullets.append(Bullet(self.x+self.r,self.y + 30,40,1,"miseryBulletSmall.png",85,85,1,-5 + i, -5 + j, 20, "boss"))
                for b in game.bossBullets:
                    if b.vx == 0 and b.vy == 0:
                        game.bossBullets.remove(b)
                        del b
            if self.turnCount % 6 == 0: # Dropping crates on the player every 6 turns
                game.bossBullets.append(Bullet(game.quote.x,self.y - 150,40,1,"squaretile.png",85,85,1,0, 10, 20, "boss"))
            if self.health > self.maxHealth/2:
                game.bossBullets.append(Bullet(self.x+self.r,self.y + 30,40,1,"miseryBulletSmall.png",85,85,1,0, 5, 20, "boss"))
            elif self.health < self.maxHealth/2:
                game.bossBullets.append(Bullet(self.x+self.r,self.y + 30,50,1,"miseryBulletLarge.png",100,100,1,0, 5, 40, "boss"))
            self.bossRecharging = True
            self.turnCount += 1
            self.rechargeStart = time.time()
            self.recharge()

    
    def recharge(self):
        if (self.rechargeEnd - self.rechargeStart) >= max(self.health/500.0,0.3): # Recharge gets quicker as boss' health decreases
            self.bossRecharging = False

class Bullet(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,vx,vy,dmg,shooter):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.vx = vx
        self.vy = vy
        self.dir = vx
        self.ttl = 60
        self.dmg = dmg
        self.shooter = shooter
        
    def update(self):
        # self.dmgNumberEnd = time.time()
        self.x += self.vx
        self.y += self.vy
        self.ttl -= 1
        
        if game.gunAcquired == True:
            if self.ttl == 0:
                if self.shooter == "boss":
                    game.bossBullets.remove(self)
                elif self.shooter == "quote":
                    try:
                        game.bullets.remove(self)
                        #del self
                    except:
                        pass
                return
            
            for t in game.tiles: # Bullet rams into tile
                self.hittingWall = self.hitWall(self.x, self.y, self.r, t.x, t.y, t.w, t.h)
                if self.hittingWall == True:
                    if self.shooter == "boss":
                        try:
                            game.bossBullets.remove(self)
                        except:
                            break
                        #break
                    elif self.shooter == "quote":
                        try:
                            game.bullets.remove(self)
                            #del self
                        except:
                            break
                        break
                        break
            
            for e in game.enemies:
                if len(game.bullets) > 0 and self.distance(e) <= self.r + e.r: # Sanity check; sometimes the game crashed when hitting an enemy from too close
                        #self.bullet = game.bullets[0]
                        e.health -= game.equippedGuns[0].dmg # WIP: The game still crashes sometimes             
                        game.enemyDamaged.rewind()
                        game.enemyDamaged.play()
                        # self.dmgNumberStart = time.time()
                        game.enemyHit = True
                        textSize(48)
                        fill(255)
                        text(str(game.equippedGuns[0].dmg), e.x - 10, e.y - 10)
                        if len(game.bullets) > 0:
                            try:
                                game.bullets.remove(self)
                                #del self
                            except:
                                break
                        else:
                            break
                        if e.health <= 0:
                            game.enemies.remove(e)
                            game.enemyKilled.rewind()
                            game.enemyKilled.play()
                            for i in range(3):
                                game.xpdrops.append(XPDrop(e.x - i*25, e.y, 23, game.g, "xpdrop.png", 46, 46))
                            if random(20) == 1:
                                game.heartdrops.append(HeartDrop(e.x, e.y + 10, 43, game.g, "heartdrop.png", 46, 46))
                            del e
                            break
                        
            if self.shooter == "quote" and len(game.bullets) > 0 and self.distance(game.boss) <= self.r + game.boss.r: # Sanity check; sometimes the game crashed when hitting an enemy from too close
                    game.boss.health -= game.equippedGuns[0].dmg # WIP: The game still crashes sometimes             
                    # self.dmgNumberStart = time.time()
                    #game.enemyHit = True
                    # textSize(48)
                    # fill(255)
                    # #text(str(game.equippedGuns[0].dmg), e.x - 10, e.y - 10)
                    game.bullets.remove(self)
                    #del self
                    
        #del self
            
            
    def display(self):
        self.update()
        image(self.img,self.x-self.w//2-game.x,self.y-self.h//2-game.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        
    def distance(self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class XPDrop(Item):
    def __init__(self,x,y,r,g,img, w,h):
        Item.__init__(self,x,y,r,g,img, w,h)
        self.vx = 0
        self.vy = 0

class HeartDrop(Item):
    def __init__(self,x,y,r,g,img, w,h):
        Item.__init__(self,x,y,r,g,img, w,h)
        self.vx = 0
        self.vy = 0
        
class HeartCapsule(Item):
    def __init__(self,x,y,r,g,img, w,h):
        Item.__init__(self,x,y,r,g,img, w,h)
        
class Game:
    def __init__ (self,w,h,g):
        self.state = "menu"
        self.pause = False
        self.bossBattle = False
        self.w=w
        self.h=h
        self.g=g
        self.x = 0
        self.y = 0
        self.setY = 0
        self.gunAcquired = False
        self.enemyDamaged = player.loadFile(path+"/sounds/enemyDamaged.mp3")
        self.enemyKilled = player.loadFile(path+"/sounds/enemyKilled.mp3")
        self.wantMusic = False
        self.menuMusicOn = False
        self.levelMusicOn = False
        if self.wantMusic == True:
            self.menuMusic = player.loadFile(path+"/sounds/menuMusic.mp3")
            self.levelMusic = player.loadFile(path+"/sounds/levelMusic.mp3")
            self.bossMusic = player.loadFile(path+"/sounds/bossMusic.mp3")
        self.quote = Quote(50,self.g - 70,70,self.g,"quote.png",120,120,4, 3)
        self.npcs = []
        self.npcs.append(NPC(400,self.g - 62,62,self.g, "curlybrace.png",125,125,6, "curly"))
        self.npcs.append(NPC(2000,self.g - 125,62,self.g, "misery.png",125,125,6, "misery1"))
        self.npcs.append(NPC(2200,-1225,62,self.g, "misery.png",125,125,6, "misery2"))
        self.npcs.append(NPC(3900,-1200,62,self.g, "misery.png",125,125,6, "misery3"))
        self.npcs.append(NPC(5800,-330,62,self.g, "misery.png",125,125,6, "misery4"))
        self.npcs.append(NPC(2300,-600,75,self.g, "balrog.png",240,150,6, "balrog"))
        self.enemies = []
        self.spikes = []
        loadEnemies = open(path+"/objects/enemies.txt", "r")
        for e in loadEnemies:
            eval(e)
        self.boss = Boss(0,0, 62,self.g, "misery.png",125,125,6, 5300, 6500, 20, 500)
        self.guns = [] # Guns lying on the ground
        self.guns.append(Gun(150,-800,30,self.g,"polarstar.png",109,75, 5, 0.1)) 
        self.equippedGuns = [] # Guns equipped by the player   
        self.bullets = []
        self.bossBullets = []
        self.dmgNumberStart = 0
        self.enemyHit = False
        self.xpdrops = []
        self.heartdrops = []
        self.heartcapsules = []
        self.heartcapsules.append(HeartCapsule(950, -1730, 40, self.g, "heartcapsule.png", 96,76))
        self.dialogCount = 0
        self.totalDBoxesCurly = [] # All of the dialogue gets loaded here at once
        self.totalDBoxesMisery1 = []
        self.totalDBoxesMisery2 = []
        self.totalDBoxesMisery3 = []
        self.totalDBoxesMisery4 = []
        self.totalDBoxesMiserydef = []
        self.totalDBoxesBalrog = []
        self.dialogBoxesCurly = [] # What actually gets displayed, box by box
        self.dialogBoxesMisery1 = []
        self.dialogBoxesMisery2 = []
        self.dialogBoxesMisery3 = []
        self.dialogBoxesMisery4 = []
        self.dialogBoxesMiserydef = []
        self.dialogBoxesBalrog = []
        loadDialogue = open(path+"/objects/dialogue.txt", "r")
        for d in loadDialogue:
            eval(d)
        self.tiles = []
        loadTiles = open(path+"/objects/tiles.txt", "r")
        for t in loadTiles:
            eval(t)
        
    def dialogProgress(self,name,cnt):
        if cnt < len(self.totalList):
            self.displayList.append(self.totalList[0 + cnt])
        if cnt != 0 and cnt < len(self.totalList):
            self.displayList.remove(self.totalList[cnt - 1])
    
    def display(self):
        stroke(255)
        line(0,self.g - self.y,self.w,self.g - self.y)
            
        self.quote.display()
            
        for t in self.tiles:
            t.display()
                    
        for g in self.guns:
            g.display()

        for e in self.enemies:
            e.display()
            
        for s in self.spikes:
            s.display()
            
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
            
        if self.bossBattle == True:
            self.boss.display()
            for b in self.bossBullets:
                b.display()
            
        for n in self.npcs:
            n.display()
            
        for x in self.xpdrops:
            x.display()
            
        for h in self.heartdrops:
            h.display()
        
        for h in self.heartcapsules:
            h.display()
            
        if self.quote.midDialog == True:
            for i in self.displayList:
                i.display()
        
        if self.bossBattle == True:
            # Boss health
            fill(0,0,0) # Colour of the full bar
            rect(50,650,900,50) # The full bar
            fill(255,0,0) # Colour of the current progress
            rect(50,650,max(game.boss.health * 1.8, 0), 50) # Current progress
        
        # Experience bar; starts empty
        fill(102,0,51) # Colour of the full bar
        rect(50,30,100,20) # The full bar
        fill(255,255,0) # Colour of the current progress
        rect(50,30,min(self.quote.displayedXP * 1, 100), 20) # Current progress
        
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
    if game.state == "menu":
        game.menuImage = loadImage(path+"/images/menuImage.png")
        background(game.menuImage)
        textSize(36)
        fill(70)
        rect(game.w//2.5,game.h//3,250,50)
        if game.w//2.5 < mouseX < game.w//2.5+250 and game.h//3 < mouseY < game.h//3+50:
            fill(0,255,0)
        else:
            fill(255)
        text("Play Game",game.w//2.5+20,game.h//3+40)
        
        fill(70)
        rect(game.w//2.5,game.h//3+100,250,50)
        if game.w//2.5 < mouseX < game.w//2.5+250 and game.h//3+100 < mouseY < game.h//3+150:
            fill(0,255,0)
        else:
            fill(255)
        text("Instructions",game.w//2.5+20,game.h//3+140)
        if game.menuMusicOn == False and game.wantMusic == True:
            game.menuMusic.rewind()
            game.menuMusic.play()
            game.menuMusicOn = True
            
        
    elif game.state == "instructions":
        background(game.menuImage)
        textSize(50)
        fill(255)
        text('Movement = Left and Right Arrows', 100, 100)
        text('Jump = X', 100, 200)
        text('Shoot = C', 100, 300)
        text('Move camera = Up and Down Arrows', 100, 400)
        text('Talk = Enter', 100, 500)
        text('Press V to return to menu', 100, 600)
        
    elif game.state == "play":
        if game.pause == False:
            game.backgroundImage = loadImage(path+"/images/backgroundImage.png")
            background(game.backgroundImage)
            if game.levelMusicOn == False and game.wantMusic == True:
                game.levelMusic.rewind()
                game.levelMusic.play()
                game.levelMusicOn = True
            game.display()
            for g in game.equippedGuns:
                if g.gunReloading == True:
                    g.reloadEnd = time.time()
                    g.reload() # Updates reload timer until gun is reloaded.    
            if game.quote.currentLives == 0:
                if game.wantMusic == True:
                    game.bossMusic.pause()
                    game.levelMusic.pause()
                game.__init__(1024,768,600)
                game.state = "menu"
            if game.bossBattle == True:
                if game.boss.bossRecharging == True:
                    game.boss.rechargeEnd = time.time()
                    game.boss.recharge()
        else:
            textSize(30)
            fill(255,0,0)
            text("Paused",game.w//2,game.h//2)
    elif game.state == "victory":
        background(0)
        textSize(60)
        text("Congratulations!",game.w//4,game.h//4)
        text("You beat the game!",game.w//4,game.h//4 + 100)
        text("Thanks for playing!",game.w//4,game.h//4 + 200)
        game.state = "menu"
        
def mouseClicked():
    if game.w//2.5 < mouseX < game.w//2.5+250 and game.h//3 < mouseY < game.h//3+50:
        if game.wantMusic == True:
            game.menuMusic.pause()
        game.__init__(1024,768,600)
        game.state="play"
    elif game.w//2.5 < mouseX < game.w//2.5+250 and game.h//3+100 < mouseY < game.h//3+150:
        game.state = "instructions"
        
def keyPressed():
    if keyCode == LEFT:
        game.quote.keyHandler[LEFT]=True
    elif keyCode == RIGHT:
        game.quote.keyHandler[RIGHT]=True
    elif keyCode == 67:
        game.quote.keyHandler[UP]=True
    elif keyCode == 88 and game.gunAcquired == True:
        for g in game.equippedGuns:
            g.fire()
    elif keyCode == 86:
        if game.state == "instructions":
            game.state = "menu"
    elif keyCode == UP: # Moves camera
        game.ogY = game.setY
        if game.y >= game.setY:
            game.y += -10
    elif keyCode == DOWN:
        game.ogY = game.setY
        if game.y <= game.setY:
            game.y += 10
    elif key == ENTER:
        for n in game.npcs:
            if game.quote.distance(n) <= game.quote.r + n.r and (game.quote.startingDialog == False or game.quote.midDialog == True): # If not in dialog and near an NPC, open dialog box.
                game.quote.getNPC()
                game.quote.startingDialog = True
                game.quote.midDialog = True
                game.totalListName = "game.totalDBoxes" + game.quote.selectedNPC.capitalize()
                game.displayListName = "game.dialogBoxes" + game.quote.selectedNPC.capitalize()
                game.displayList = eval(game.displayListName) # Turns the string into a function expression
                game.totalList = eval(game.totalListName)
                if game.dialogCount < len(game.totalList):
                    if n.name == "misery4":
                        if game.wantMusic == True:
                            game.levelMusic.pause()
                    game.dialogProgress(game.quote.selectedNPC, game.dialogCount)
                    game.quote.midDialog = True
                    game.dialogCount += 1
                else:
                    game.quote.startingDialog = False
                    game.quote.midDialog = False
                    game.dialogCount = 0
                    if n.name == "misery4":
                        #n.vy = -10
                        game.boss = Boss(n.x, n.y - 600, 62,game.g, "misery.png",125,125,6, 5300, 6500, 20, 500)
                        game.npcs.remove(n)
                        del n
                        game.bossBattle = True
                        if game.wantMusic == True:
                            game.bossMusic.rewind()
                            game.bossMusic.play()
                    elif n.name == "miserydef":
                        game.npcs.remove(n)
                        del n
                        game.state = "victory"
                game.display()
        game.display()


def keyReleased():
    if keyCode == LEFT:
        game.quote.keyHandler[LEFT]=False
    elif keyCode == RIGHT:
        game.quote.keyHandler[RIGHT]=False   
    elif keyCode == 67:
        game.quote.keyHandler[UP]=False
    elif keyCode == UP: # Moves camera back to original position
        game.y = game.ogY
    elif keyCode == DOWN:
        game.y = game.ogY
