import pygame
from keeper import keeper

pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
maroon = (128,0,0)
orange = (255,165,0)
green = (0,128,0)
teal = (0,128,128)

bounds = [1000, 900]

dis = pygame.display.set_mode((bounds[0], bounds[1]))
pygame.display.set_caption('Emergent Nodes')
 
game_over = False
 
clock = pygame.time.Clock()
framerate = 30

nSize = 4

def updateScreen(nodes):
    dis.fill(white)
    for node in nodes:
        #node.nodeState()
        pygame.draw.circle(dis, node.color, [int(node.pos[0]), int(node.pos[1])], nSize)
    pygame.display.update()
    clock.tick(framerate)  

arena = keeper(bounds)
arena.enableClustering(200)
arena.enableAvoidance(10)
arena.enableAngleMatching(150)

# arena.generateNode(nSize, pos = [200, 100], speed = 5, angle = 90,  color=maroon)
# arena.generateNode(nSize, pos = [215, 790], speed = 0, angle = 90,  color=teal)
# arena.generateNode(nSize, pos = [200, 500], speed = 5, angle = 270, color=teal)
# arena.generateNode(nSize, pos = [220, 500], speed = 5, angle = 270, color=teal)
arena.addRandomizedNodes(nSize, 150, speed=15, color=green)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    nodes = arena.updateHerd()
    updateScreen(nodes)
pygame.quit()
quit()