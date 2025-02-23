## Code partially generated by ChatGPT (the design of grid)
## SMBus Integration
from smbus import SMBus

## Import pygame and other libaries
import pygame
import math
import time
import random
addr = 0x8 ## Bus address
bus = SMBus(11) ## Indicates /dev/ic2-11 (TFT IS 11)

##turn to true to enter the loop1!!!!
numb = 0

print("Enter 1 For ON or 0 For OFF")
#ledstate = input(" ")
while numb == 1:
    #ledstate = input(" ")
    try:
            
        #ledstate = input(" ")
        ##THIS SENDS DADTA TO ARRDUINO
        #data = bus.read_i2c_block_data(addr, 0, 32)
        #message = ''.join([chr(byte) for byte in data])
        #print("Success! ", message)

        if ledstate == "1":
            bus.write_byte(addr, 0x1) ## Switch it on
        elif ledstate == "0":
            bus.write_byte(addr, 0x0) ## Switch it on
        else:
            numb = 0
    except Exception as e:
        print("Error reading from arduino: ", e)
    time.sleep(1)


## Setup pygame (note to self, raspberry pi size = 480x800)
pygame.init()
screen = pygame.display.set_mode((480, 800))
clock = pygame.time.Clock()
status = True #truel?

##Fake target
def fake_input():
    return random.randint(200,400)

## Radar values
center = (480 // 2, 800 // 2)
max_radius = 480 // 2
start_angle = 150
end_angle = 30
num_sections = 4
section_angle = (start_angle - end_angle) // num_sections
num_horizontal_lines = 4
line_gap = max_radius // num_horizontal_lines

## Main loop
while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## If window is exited, will close program
            status = False


## Graphics
    screen.fill("black")

    ## Create / Display Arc
    points = [center]   
    for angle in range(start_angle, end_angle - 1, -2):
        x = center[0] + max_radius * math.cos(math.radians(angle))
        y = center[1] - max_radius * math.sin(math.radians(angle))
        points.append((x,y))
    points.append(center)
    pygame.draw.polygon(screen, "green", points, 2)
    
    

    ## Draw 3 lines dividing the radar (by creating a loop)
    for i in range(num_sections):
        angle = start_angle - (i + 1) * section_angle 
        x = center[0] + max_radius * math.cos(math.radians(angle))
        y = center[1] - max_radius * math.sin(math.radians(angle))

        pygame.draw.line(screen, "green", center, (x,y), 2)
    
    for i in range(1, num_horizontal_lines):
        radius = line_gap * i
        for angle in range(start_angle, end_angle -1, -2):
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] - radius * math.sin(math.radians(angle))

            pygame.draw.circle(screen, "green", (int(x), int(y)), 2)
    pygame.draw.circle(screen, "red", (fake_input()-50, fake_input()-20                     ), 6)
    time.sleep(1)    
    pygame.display.flip()
    clock.tick(30) ## FPS
