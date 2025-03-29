#paint for lab9
import pygame 
import math

pygame.init()

#set color
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

COLOR = RED   

#fps
clock = pygame.time.Clock()
FPS = 30

# varibles
prev, cur = None, None  #for pen
prev1, cur1 = None, None #for eraser

#screen
lenght, weight = 1000, 600
screen = pygame.display.set_mode((lenght,weight))
screen.fill(WHITE)
running = True

pen = "mouse"
last_event = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #buttons to change modes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pen = "mouse"
            if event.key == pygame.K_w:
                pen = "rect"
            if event.key == pygame.K_e:
                pen = "circle"
            if event.key == pygame.K_r:
                pen = "eraser"
            
            #buttons to change color
            if event.key == pygame.K_z:
                COLOR = RED
            if event.key == pygame.K_x:
                COLOR = GREEN
            if event.key == pygame.K_c:
                COLOR  = BLUE
            if event.key == pygame.K_v:
                COLOR = BLACK

        #drawing by mouse  
        if pen == "mouse" :
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                cur = pygame.mouse.get_pos()
            if prev:
                pygame.draw.line(screen, COLOR, prev, cur, 1)
                prev = cur
            if event.type == pygame.MOUSEBUTTONUP:
                prev = None
            
        #drawing rectangle
        if pen == "rect":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y =pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 =pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.line(screen, COLOR, (x,y), (x1, y), 1)
                pygame.draw.line(screen, COLOR, (x1,y), (x1, y1), 1)
                pygame.draw.line(screen, COLOR, (x1,y1), (x, y1), 1)
                pygame.draw.line(screen, COLOR, (x,y1), (x, y), 1)
                last_event = 'None'

        #drawing circle
        if pen == "circle" :
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y =pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 =pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.circle(screen, COLOR, (x+(x1-x)/2, y+(y1-y)/2), (x1-x)/2 )
                pygame.draw.circle(screen, WHITE, (x+(x1-x)/2, y+(y1-y)/2), ((x1-x)/2)-1)
                last_event = 'None'

        #eraser
        if pen == "eraser" :
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev1 = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                cur1 = pygame.mouse.get_pos()
            if prev1:
                pygame.draw.line(screen, WHITE, prev1, cur1, 10)
                prev1 = cur1
            if event.type == pygame.MOUSEBUTTONUP:
                prev1 = None

        #drawing square
        if pen == "square":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y =pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 =pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                if(x1-x)<=(y1-y):
                    y1 = y+ (x1-x)
                else:
                    x1 = x+ (y1-y)
                pygame.draw.line(screen, COLOR, (x,y), (x1, y), 1)
                pygame.draw.line(screen, COLOR, (x1,y), (x1, y1), 1)
                pygame.draw.line(screen, COLOR, (x1,y1), (x, y1), 1)
                pygame.draw.line(screen, COLOR, (x,y1), (x, y), 1)

                last_event = 'None'

        #drawing equilateral_triangle
        if pen == "equilateral_triangle":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y =pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 =pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                h = y + (math.sqrt(3)*(x1-x)/2)
                a = ((x + (x1-x)/2), y)
                b = (x, h)
                c = (x1, h)
                pygame.draw.line(screen, COLOR, a, b, 1)
                pygame.draw.line(screen, COLOR, b, c, 1)
                pygame.draw.line(screen, COLOR, c, a, 1)
                last_event = "none"   


        #drawing right triangle
        if pen == "right triangle":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y =pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 =pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                pygame.draw.line(screen, COLOR, (x, y), (x, y1), 1)
                pygame.draw.line(screen, COLOR, (x, y1), (x1, y1), 1)
                pygame.draw.line(screen, COLOR, (x1, y1), (x, y), 1)   
                last_event = "none"

        #drawing rhombus
        if pen == "rhombus":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y =pygame.mouse.get_pos()
                last_event = "DOWN"
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 =pygame.mouse.get_pos()
                last_event = "UP"
            if last_event == "UP":
                a = (x+(x1-x)/2, y)
                b = (x1, y+(y1-y)/2)
                c = (x+(x1-x)/2, y1)
                d = (x, y+(y1-y)/2)
                pygame.draw.line(screen, COLOR, a, b, 1)
                pygame.draw.line(screen, COLOR, b, c, 1)
                pygame.draw.line(screen, COLOR, c, d, 1)
                pygame.draw.line(screen, COLOR, d, a, 1)
                last_event = "none"
    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()