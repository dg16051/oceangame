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
deltaTime = 0

#org classes
class palette:
    ocean = [0,119,190]

class player:
    center_x = None
    center_y = None

class texture:
    class player:
        ship = "res/ship/player/nemedship.png"
    class enemy:
        ship = "res/ship/enemy/formorianship.png"

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

class Ship(arcade.Sprite):
    def __init__(self, texture, scale, projectileList):
        super().__init__(texture, scale)

        # const vars
        self.hp = 2
        self.speed = 1
        self.center_x = random.randint(100, windowSize[0] - 100)
        self.center_y = random.randint(100, windowSize[1] - 100)
        self.angle = random.randint(0, 359)
        self.changeX = 0
        self.changeY = 0
        self.changeDIR= 0
        self.changeSPD = 0
        self.arrowSpeed = 4
        self.arrowCooldown = 1
        self.number = random.random()
        self.projectileList = projectileList

    def update(self):
        self.changeX = getCirSect(self.angle)[0] * self.changeSPD
        self.changeY = getCirSect(self.angle)[1] * self.changeSPD
        self.center_x += self.changeX

        self.center_y += self.changeY
        self.angle += self.changeDIR

        # always a value 0-360 pls
        if self.angle > 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360

        if self.hp < 0:
            self.kill()

    def fire(self, angle):
        if self.hp > -1:
            for i in range(-1,2):
                localX = getCirSect(self.angle)[0] * 12 * i + getCirSect(self.angle - angle)[0] * 30#1st const is spread, 2nd const is distance from boat
                localY = getCirSect(self.angle)[1] * 12 * i + getCirSect(self.angle - angle)[1] * 30
                arrow = Projectile(texture.arrow, 0.375, self.center_x + localX, self.center_y + localY, self.angle - angle, self.arrowSpeed)
                self.projectileList.append(arrow)

class Enemy(Ship):
    def __init__(self, typeAI, projectileList):
        super().__init__(texture.enemy.ship, 1, projectileList)
        self.typeAI = typeAI
        self.leftTimer = Timer(self.arrowCooldown)
        self.rightTimer = Timer(self.arrowCooldown)
        self.changeSPD = 2

    def update(self):
        super().update()

        if self.typeAI == 1:
            self.distanceX = self.center_x - player.center_x
            self.distanceY = self.center_y - player.center_y
            self.angleTarget = round(math.degrees(math.atan(self.distanceY / self.distanceX)), 0)

            if self.angle != self.angleTarget:
                if self.angle < self.angleTarget:
                    self.angle += 1
                if self.angle > self.angleTarget:
                    self.angle += -1
            else:
                if self.leftTimer.update():
                    self.fire(-90)
                elif self.rightTimer.update():
                    self.fire(90)

        if self.typeAI == 2: #copier
            self.angle += random.random() * 2
            self.angle += -random.random() * 2
            if self.leftTimer.update():
                self.fire(-90)
            elif self.rightTimer.update():
                self.fire(90)
        if self.center_y > 500 or self.center_y < 100 or self.center_x > 700 or self.center_x < 100:
            self.angle += 2


class Timer():
    def __init__(self, target):
        self.time = 0
        self.target = target
    def update(self):
        self.time += deltaTime
        if self.time > self.target:
            self.time = 0
            return True
        else:
            return False


def getCirSect(angle): #get co-ords of where a line drawn from the center intersects with the circumference
    theta = math.radians(angle + 90)
    x = math.cos(theta)
    y = math.sin(theta)
    return [x,y]

#-------------------------------------------------------------------------------
class game(arcade.Window):
    def __init__(self):
        super().__init__(windowSize[0],windowSize[1], "Ocean Game")
        arcade.set_background_color(palette.ocean)

    def setup(self):
        self.projectileList = arcade.SpriteList()
        self.shipList = arcade.SpriteList()

        self.player = Ship(texture.player.ship, 1, self.projectileList)
        self.shipList.append(self.player)

        self.fireCooldownLEFT = 0
        self.fireCooldownRIGHT = 0
        self.fireCooldownUP = 0

    def on_draw(self):
        arcade.start_render()

        self.projectileList.draw()
        self.shipList.draw()

    def on_key_press(self, key, modifiers):

        #movement
        if key == arcade.key.W:
            if self.player.changeSPD != 3:
                self.player.changeSPD += self.player.speed
        if key == arcade.key.D:
            self.player.changeDIR += -self.player.speed
        if key == arcade.key.S:
            if self.player.changeSPD != 0:
                self.player.changeSPD += -self.player.speed
        if key == arcade.key.A:
            self.player.changeDIR += self.player.speed

        #firing
        if key == arcade.key.LEFT:
            if self.fireCooldownLEFT <= 0:
                self.player.fire(-90)
                self.fireCooldownLEFT = self.player.arrowCooldown

        if key == arcade.key.RIGHT:
            if self.fireCooldownRIGHT <= 0:
                self.player.fire(90)
                self.fireCooldownRIGHT = self.player.arrowCooldown

        #dev
        if key == arcade.key.E:
            for i in range(1):
                enemy = Enemy(1, self.projectileList)
                self.shipList.append(enemy)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.player.changeDIR += self.player.speed
        if key == arcade.key.A:
            self.player.changeDIR += -self.player.speed


    def update(self, delta_time):
        global deltaTime
        deltaTime = delta_time
        self.projectileList.update()
        self.shipList.update()

        player.center_x = self.player.center_x
        player.center_y = self.player.center_y

        if self.fireCooldownLEFT > 0:
            self.fireCooldownLEFT += -delta_time
        if self.fireCooldownRIGHT > 0:
            self.fireCooldownRIGHT += -delta_time

        for arrow in self.projectileList:
            hitList = arcade.check_for_collision_with_list(arrow, self.shipList)
            if len(hitList) > 0:
                arrow.kill()

            for enemy in hitList:
                enemy.hp += -1

#-------------------------------------------------------------------------------

def main():
    window = game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()