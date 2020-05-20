import pygame
from keeper import keeper
from slider import Slider

pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
maroon = (128,0,0)
orange = (255,165,0)
green = (0,128,0)
teal = (0,128,128)

def scaleCord(gamePos, offset):
    gx = gamePos[0]
    gy = gamePos[1]
    scaledX = gx + offset[0]
    scaledY = gy + offset[1]
    scaledGamePos = [scaledX, scaledY]
    return(scaledGamePos)

def updateSlides(slides):
    # Move slides
    for s in slides:
        if s.hit:
            s.move()

def updateScreen(nodes, sliders):
    dis.fill(white)
    for node in nodes:
        #node.nodeState()
        cord = [int(node.pos[0]), int(node.pos[1])]
        pygame.draw.circle(dis, node.color, scaleCord(cord, parameterBounds), nSize)
    for slider in sliders:
        slider.draw()
    pygame.draw.rect(dis, black, playSquare, 1)
    pygame.display.update()
    clock.tick(framerate)  

def updateGameParameters(sliders, arena):
    for slider in sliders:
        if((slider.name == "Clustering") and (slider.hit)):
            arena.enableClustering(slider.val)
        elif((slider.name == "Avoidance")  and (slider.hit)):
            arena.enableAvoidance(slider.val)
        elif((slider.name == "Vectors")  and (slider.hit)):
            arena.enableAngleMatching(slider.val)
        elif((slider.name == "Max Angle")  and (slider.hit)):
            arena.enableMaxAngle(slider.val)
    

#WINDOW SIZING
                #   L    T    R    B
parameterBounds = [20, 10, 20, 80]
gameBounds = [1000, 900]
windowX = gameBounds[0]+parameterBounds[0]+parameterBounds[2]
windowY = gameBounds[1]+parameterBounds[1]+parameterBounds[3]
windowBounds = (windowX, windowY)
startXY = scaleCord([0, 0], parameterBounds)
endXY = [gameBounds[0], gameBounds[1]]
playSquare = [startXY[0], startXY[1], endXY[0], endXY[1]]

#MAKING THE WINDOW
dis = pygame.display.set_mode(windowBounds)
pygame.display.set_caption('Emergent Nodes')
 
#ADDING SLIDERS
sliderOffset = [parameterBounds[0], parameterBounds[1]+gameBounds[1]]
font = pygame.font.SysFont("Verdana", 12)


s_cluster = Slider("Clustering", 200, 500, 0, scaleCord([0, 10], sliderOffset),font,dis)
s_avoidance = Slider("Avoidance", 10, 500, 0, scaleCord([120, 10], sliderOffset),font,dis)
s_angleMatching = Slider("Vectors", 150, 500, 0, scaleCord([240, 10], sliderOffset),font,dis)
s_maxAngle = Slider("Max Angle", 360, 360, 0, scaleCord([360, 10], sliderOffset),font,dis)
slides = [s_cluster, s_avoidance, s_angleMatching, s_maxAngle]

game_over = False
 
clock = pygame.time.Clock()
framerate = 30

nSize = 4

arena = keeper(gameBounds)

# arena.generateNode(nSize, pos = [200, 100], speed = 5, angle = 90,  color=maroon)
# arena.generateNode(nSize, pos = [200, 790], speed = 5, angle = 270,  color=teal)

# arena.enableAngleMatching(0)
# arena.enableClustering(0)
# arena.enableMaxAngle(360)
# arena.enableAvoidance(50)
# arena.lock_avoidance = True
# arena.lock_angleMatching = True
# arena.lock_clustering = True

# arena.generateNode(nSize, pos = [200, 500], speed = 5, angle = 270, color=teal)
# arena.generateNode(nSize, pos = [220, 500], speed = 5, angle = 270, color=teal)
arena.addRandomizedNodes(nSize, 150, speed=15, color=green)



while not game_over:
    updateGameParameters(slides, arena)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for s in slides:
                if s.button_rect.collidepoint(pos):
                    s.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for s in slides:
                s.hit = False
    updateSlides(slides)
    nodes = arena.updateHerd()
    updateScreen(nodes, slides)
pygame.quit()
quit()