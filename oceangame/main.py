#Program:
#Author: Ginnsy
#Date: 09/08/2018
#Version: 0.1
#-----------------


import arcade
import math
import random

windowSize = [800,600]

class palette:
    ocean = [0,119,190]
    black = [0,0,0]

def getCirSect(angle): #get co-ords of where a line drawn from the center intersects with the circumference
    theta = math.radians(angle + 90)
    x = math.cos(theta)
    y = math.sin(theta)

    return [x,y]

class game(arcade.Window):
    def __init__(self):
        super().__init__(windowSize[0],windowSize[1], "Hi")
        arcade.set_background_color(palette.ocean)

    def setup(self):
        self.playerList = arcade.SpriteList()
        self.playerSprite = arcade.Sprite("res/ship/000.bmp", 0.5)
        self.playerSprite.x = 0
        self.playerSprite.y = 200
        self.playerList.append(self.playerSprite)

    class player:
        speed = 1
        x = 0
        y = 0
        changeX = 0
        changeY = 0
        changeDIR= 0
        changeForward = 0

    def on_draw(self):
        arcade.start_render()
        self.playerList.draw()

    def on_key_press(self, key, modifiers):
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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.player.changeDIR += self.player.speed
        if key == arcade.key.A:
            self.player.changeDIR += -self.player.speed


    def update(self, delta_time):
        print(self.player.changeForward)

        self.player.changeX = getCirSect(self.playerSprite.angle)[0] * self.player.changeForward
        self.player.changeY = getCirSect(self.playerSprite.angle)[1] * self.player.changeForward


        self.playerSprite.angle += self.player.changeDIR
        self.playerSprite.x += self.player.changeX
        self.playerSprite.y += self.player.changeY
        self.playerSprite.center_x = self.playerSprite.x
        self.playerSprite.center_y = self.playerSprite.y

        if self.playerSprite.angle > 360 or self.playerSprite.angle < -360:
            self.playerSprite.angle = 0


def main():

    window = game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
