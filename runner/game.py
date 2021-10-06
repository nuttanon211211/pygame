# Simple pygame program
# Import and initialize the pygame library
import pygame
from pygame.locals import *
import random

pygame.init()
pygame.font.init() 
myfont = pygame.font.SysFont('comicsansms', 10)

print(pygame.font.get_fonts())

# Set up the drawing window
screen = pygame.display.set_mode([192, 192],RESIZABLE)
meowstic = pygame.image.load('MeowIcon.pbm')
meowstic1 = pygame.transform.flip(meowstic, True, False)
obst = pygame.image.load('obst.pbm')
particle = pygame.image.load('particles.pbm')
pygame.display.set_icon(meowstic)
pygame.display.set_caption('What a Game')
clock = pygame.time.Clock()
x= 50
x_change = 0
y_change = 0
x_change_last = 0
low = 100
y = low
up = 0
jump = 2
countjump = 0
control = False
x_obs = 200
lastscore = 0
highscore = 0
firsttime = True
screensize = 192
scalefactor = 1.0
scalepadding = [0,0]

#img sizex sizey posx posy
obslist = []
particles = []

for i in range(20):
    particles.append([random.randint(0,192),random.randint(0,192)])

 

# Run until the user asks to quit
running = True

while running:
    # Did the user click the window close button?

    for event in pygame.event.get():
        
    
    
        if event.type==VIDEORESIZE:
            #print(event.dict['size'])
            screensize = min (event.dict['size'])
            scalefactor = screensize / 192
            scalepadding = [0,0]
            for i in range(2):
                if scalepadding[i] != event.dict['size'][i]:
                    scalepadding[i] = 0.5* (event.dict['size'][i] - screensize )
            print(scalepadding)
            myfont = pygame.font.SysFont('comicsansms', int(10*scalefactor))
            #screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            #screen.blit(pygame.transform.scale(pic,event.dict['size']),(0,0))
            #pygame.display.flip()
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            control = True
            if event.key == pygame.K_LEFT:
                x_change = -1
            elif event.key == pygame.K_RIGHT:
                x_change = 1
                
            elif event.key == pygame.K_SPACE:
                if jump > 0:
                    y_change = 6
                    jump-= 1
                    countjump += 1
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if (x_change<0):
                    x_change_last = x_change
                    x_change = 0
            elif event.key == pygame.K_RIGHT:
                if (x_change>0):
                    x_change_last = x_change
                    x_change = 0
            
            elif event.key == pygame.K_SPACE:
                #y_change = -1
                pass
              


    # Game logic and display 
    if not control and countjump<=0:
        if x < -64:
            x_change_last = x_change
            x_change = 1
        elif x > 192:
            x_change_last = x_change
            x_change = -1
        elif random.random() < 0.1:
            x_change_last = x_change
            x_change = random.randint(-1,1)
    x += x_change
    y -= y_change
    y_change -= 0.2
    if y > low:
        y = low   
        jump = 2
    x = min(x,190)
    x = max(x,0) 
   
    screen.fill((0, 0, 0))
     
    
    if countjump <=0 and not firsttime:
        textsurface = myfont.render('Last Score : '+str(lastscore), False, (255, 255, 255))
        screen.blit(textsurface,(0*scalefactor+scalepadding[0], 0*scalefactor+scalepadding[1])) 
        
        textsurface = myfont.render('High Score : '+str(highscore), False, (255, 255, 255))
        screen.blit(textsurface,(0*scalefactor+scalepadding[0], 12*scalefactor+scalepadding[1]))
    elif countjump >0:
        textsurface = myfont.render('jumps : '+str(countjump), False, (255, 255, 255))
        screen.blit(textsurface,(0*scalefactor+scalepadding[0], 0*scalefactor+scalepadding[1]))     
    
    if x_change > 0:
        #screen.blit(meowstic, (x,low))
        screen.blit(pygame.transform.scale(meowstic,(screensize//3,screensize//3)),(x*scalefactor+scalepadding[0],y*scalefactor+scalepadding[1]))
        #screen.blit(pygame.transform.scale((meowstic,(x,low)),(screensize,screensize))
        
    elif x_change < 0:
        #screen.blit(meowstic1, (x,low))
        screen.blit(pygame.transform.scale(meowstic1,(screensize//3,screensize//3)),(x*scalefactor+scalepadding[0],y*scalefactor+scalepadding[1]))
    else:
        if x_change_last >= 0:
            #screen.blit(meowstic, (x,low))
            screen.blit(pygame.transform.scale(meowstic,(screensize//3,screensize//3)),(x*scalefactor+scalepadding[0],y*scalefactor+scalepadding[1]))
        elif x_change_last < 0:
            #screen.blit(meowstic1, (x,low))
            screen.blit(pygame.transform.scale(meowstic1,(screensize//3,screensize//3)),(x*scalefactor+scalepadding[0],y*scalefactor+scalepadding[1]))
        
    if countjump>0:
        #x_obs
        if len(obslist)< 1+countjump//22:
            obslist.append([obst,32,64,random.randint(192,250),low])
        for e in obslist:
            screen.blit(pygame.transform.scale(e[0],(int(e[1]*scalefactor),int(e[2]*scalefactor)) ),(e[3]*scalefactor+scalepadding[0],e[4]*scalefactor+scalepadding[1])) 
        
        for i in range(len(obslist)):
            obslist[i][3] -= 1+ 0.1*countjump**0.5
            if obslist[i][3] < -64:
                obslist[i][3] =  30*i + random.randint(180,200+5*i)
            
        for e in obslist:
            if abs((e[3]+e[1]//2) - (x+32)) < 10 and abs((e[4]+e[2]//2)-(y+32)) < 10:
                lastscore = countjump
                highscore = max(highscore,lastscore)
                firsttime = False
                countjump = 0
                obslist = []
                print(x,y,x_obs,low)
    
    if sum(pygame.key.get_pressed()) == 0:
        control = False
    
    for i in range(len(particles)):
        particles[i][0] += random.randint(-1,1)
        if countjump>0:
            particles[i][0] += -1
        if particles[i][0] < -5:
            particles[i][0] = random.randint(192,198)    
        particles[i][1] += 1
        if particles[i][1]> low+64:
            particles[i][1] = random.randint(-5,-1)
            if particles[i][0] > 198:
                particles[i][0] = random.randint(0,192)
        
    for e in particles:
        screen.blit(pygame.transform.scale(particle,(int(3*scalefactor),int(3*scalefactor))),(e[0]*scalefactor+scalepadding[0],e[1]*scalefactor+scalepadding[1]))

    # Flip the display
    pygame.display.flip()
    
    pygame.display.update()
    clock.tick(60)


# Done! Time to quit.
pygame.quit()
