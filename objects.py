import pygame
import random

class World:
    def __init__(self, screenWidth, screenHeight):
        self.objects = {}
        self.win = 0
        self.score = 0
        self.highscore = 0
        self.begin = False
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def add(self, object, name):
        self.objects[name] = object

    def draw(self, surface):
        for obj in self.objects.values():
            obj.draw(surface)

    def update(self, dt, screenHeight):
        for obj in self.objects.values():
            obj.update(dt, screenHeight)

    def updateEnemyDir(self):
        enemyPos = self.objects["EnemyRect"].position.y + self.objects["EnemyRect"].height // 2
        if (self.objects["Ball"].position.y > enemyPos):
            self.objects["EnemyRect"].direction.y = 1.0
        elif self.objects["Ball"].position.y < enemyPos:
            self.objects["EnemyRect"].direction.y = -1.0
        else:
            self.objects["EnemyRect"].direction.y = 0

    def gameOver(self):
        if (self.objects["Ball"].position.x <= self.objects["PlayerRect"].position.x):
            self.begin = False
            if self.score > self.highscore:
                self.highscore = self.score
            self.score = 0
            self.reset()

        elif (self.objects["Ball"].position.x >= self.objects["EnemyRect"].position.x):
            self.score += 1
            self.reset()

    def reset(self):
        self.objects["PlayerRect"] = Rectangle(pygame.Vector2(20,20), [255,0,0], 200, 50)
        self.objects["EnemyRect"] = Rectangle(pygame.Vector2(self.screenWidth - 20 - 50 ,0 + 20), [0,0,255], 200, 50)
        self.objects["Ball"] = Circle(pygame.Vector2(self.screenWidth//2, self.screenHeight//2), [0,255,0], 20)

        print("Score: ", self.score)
        print("HighScore: ", self.highscore)



class Object:
    def __init__(self, position, color):
        self.position = position
        self.color = color

class Rectangle(Object):
    def __init__(self, position, color, height, width):
        super().__init__(position, color)
        self.height = height
        self.width = width
        self.direction = pygame.Vector2(0,0)
        self.speed = 5

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)

    def update(self, dt, screenHeight):
        if(self.direction.y == 1.0 and self.position.y + self.height > screenHeight or
           self.direction.y == -1.0 and self.position.y < 0):
            return
        self.position.y += self.direction.y * self.speed 

class Circle(Object):
    def __init__(self, position, color, radius):
        super().__init__(position, color)
        self.radius = radius
        self.direction = pygame.Vector2(-random.random(), 2*random.random()-1).normalize()
        self.speed = 5

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
    
    def update(self, dt, screenHeight = 0):
        self.position += self.direction * self.speed
        #self.position.y += self.direction.y * self.speed

    def collision(self, playerRect, enemyRect, screenHeight):
        # player collision
        if (self.position.y - self.radius < playerRect.position.y + playerRect.height and
            self.position.y + self.radius > playerRect.position.y and
            self.position.x - self.radius < playerRect.position.x + playerRect.width):
            self.direction.reflect_ip(pygame.Vector2(1.0, 0.0))
            self.speed += 0.5

        # enemy collision
        if(self.position.y - self.radius < enemyRect.position.y + enemyRect.height and
            self.position.y + self.radius > enemyRect.position.y and
            self.position.x + self.radius > enemyRect.position.x):
            self.direction.reflect_ip(pygame.Vector2(1.0, 0.0))
            self.speed += 0.5

        # wall collision
        if (self.position.y + self.radius > screenHeight or
            self.position.y - self.radius < 0):
            self.direction.reflect_ip(pygame.Vector2(0.0, 1.0))


    