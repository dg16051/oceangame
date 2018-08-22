#Program:
#Author: Ginnsy
#Date: 09/08/2018
#Version: 0.1
#-----------------


import arcade
import math
import random

#global vars
windowSize = [800,600]

#org classes
class palette:
    ocean = [0,119,190]

class texture:
    class player:
        ship = "res/ship/player/nemedship.png"

    #universal
    arrow = "res/bullet/arrow.png"

class Projectile(arcade.Sprite): #use for all proj
    def __init__(self, texture, scale, startX, startY, angle, speed):
        super().__init__(texture, scale)
        self.center_x = startX
        self.center_y = startY
        self.angle = angle
        self.changeX = getCirSect(self.angle)[0] * speed
        self.changeY = getCirSect(self.angle)[1] * speed

    def update(self):
        self.center_x += self.changeX
        self.center_y += self.changeY
        if self.center_x < -50 or self.center_x > 850 or self.center_y < -50 or self.center_y > 650:
            self.kill()

def getCirSect(angle): #get co-ords of where a line drawn from the center intersects with the circumference
    theta = math.radians(angle + 90)
    x = math.cos(theta)
    y = math.sin(theta)
    return [x,y]

#-------------------------------------------------------------------------------
class game(arcade.Window):
    def __init__(self):
        super().__init__(windowSize[0],windowSize[1], "Hi")
        arcade.set_background_color(palette.ocean)

    def setup(self):
        self.playerList = arcade.SpriteList()
        self.playerSprite = arcade.Sprite(texture.player.ship, 2)
        self.playerSprite.x = 400
        self.playerSprite.y = 300
        self.playerList.append(self.playerSprite)

        self.projectileList = arcade.SpriteList()

        self.fireCooldownLEFT = 0
        self.fireCooldownRIGHT = 0
    class player:
        speed = 1
        x = 0
        y = 0
        changeX = 0
        changeY = 0
        changeDIR= 0
        changeForward = 0
        arrowSpeed = 4
        arrowCooldown = 1

    def on_draw(self):
        arcade.start_render()

        self.playerList.draw()
        self.projectileList.draw()

    def on_key_press(self, key, modifiers):

        #movement
        if key == arcade.key.W:
            if self.player.changeForward != 3:
                self.player.changeForward += self.player.speed
        if key == arcade.key.D:
            self.player.changeDIR += -self.player.speed
        if key == arcade.key.S:
            if self.player.changeForward != 0:
                self.player.changeForward += -self.player.speed
        if key == arcade.key.A:
            self.player.changeDIR += self.player.speed

        #firing
        if key == arcade.key.LEFT:
            if self.fireCooldownLEFT <= 0:
                for i in range(-1,2):
                    localX = getCirSect(self.playerSprite.angle)[0] * 20 * i
                    localY = getCirSect(self.playerSprite.angle)[1] * 20 * i
                    arrow = Projectile(texture.arrow, 0.375, self.playerSprite.x + localX, self.playerSprite.y + localY, self.playerSprite.angle + 90, self.player.arrowSpeed)
                    self.projectileList.append(arrow)
                    
                self.fireCooldownLEFT = self.player.arrowCooldown

        if key == arcade.key.RIGHT:
            if self.fireCooldownRIGHT <= 0:
                for i in range(-1,2):
                    localX = getCirSect(self.playerSprite.angle)[0] * 20 * i
                    localY = getCirSect(self.playerSprite.angle)[1] * 20 * i
                    arrow = Projectile(texture.arrow, 0.375, self.playerSprite.x + localX, self.playerSprite.y + localY, self.playerSprite.angle + -90, self.player.arrowSpeed)
                    self.projectileList.append(arrow)

                self.fireCooldownRIGHT = self.player.arrowCooldown

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.player.changeDIR += self.player.speed
        if key == arcade.key.A:
            self.player.changeDIR += -self.player.speed


    def update(self, delta_time):
        self.projectileList.update()

        print(self.fireCooldownLEFT, self.fireCooldownRIGHT)

        self.player.changeX = getCirSect(self.playerSprite.angle)[0] * self.player.changeForward
        self.player.changeY = getCirSect(self.playerSprite.angle)[1] * self.player.changeForward

        self.playerSprite.angle += self.player.changeDIR
        self.playerSprite.x += self.player.changeX
        self.playerSprite.y += self.player.changeY
        self.playerSprite.center_x = self.playerSprite.x #shortcuts
        self.playerSprite.center_y = self.playerSprite.y #shortcuts

        if self.playerSprite.angle > 360 or self.playerSprite.angle < -360:
            self.playerSprite.angle = 0

        if self.fireCooldownLEFT > 0:
            self.fireCooldownLEFT += -delta_time
        if self.fireCooldownRIGHT > 0:
            self.fireCooldownRIGHT += -delta_time

#-------------------------------------------------------------------------------

def main():
    window = game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
