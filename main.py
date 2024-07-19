import objects
import pygame

aspectRatio = 16/9
screenWidth = 1280
screenHeight = screenWidth / aspectRatio
borderPadding = 20

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True
framerate = 60


# object creation
world = objects.World(screenWidth, screenHeight)
world.add(objects.Rectangle(pygame.Vector2(0 + borderPadding,0 + borderPadding), [255,0,0], 200, 50), "PlayerRect")
world.add(objects.Rectangle(pygame.Vector2(screenWidth - borderPadding - 50 ,0 + borderPadding), [0,0,255], 200, 50), "EnemyRect")
world.add(objects.Rectangle(pygame.Vector2(screenWidth//2 - 10,0 + borderPadding), [255,255,255],
                             screenHeight - (2 * borderPadding), 20), "Divider")
world.add(objects.Circle(pygame.Vector2(screenWidth//2, screenHeight//2), [0,255,0], 20), "Ball")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                world.objects["PlayerRect"].direction.y = -1.0
            if event.key == pygame.K_s:
                world.objects["PlayerRect"].direction.y = 1.0
            if event.key == pygame.K_SPACE:
                world.begin = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                world.objects["PlayerRect"].direction.y = 0


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    if(world.begin):
        world.update(1/framerate, screenHeight)
        world.updateEnemyDir()
        world.objects["Ball"].collision(world.objects["PlayerRect"], world.objects["EnemyRect"], screenHeight)
        world.gameOver()


    world.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(framerate)  # limits FPS to 60

pygame.quit()
