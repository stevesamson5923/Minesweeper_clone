import pygame
import random
pygame.init()

WIN_WIDTH = 300
WIN_HEIGHT = 400
TOTAL_BLOCKS = 100
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

pygame.display.set_caption('MINESWEEPER' )
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont2 = pygame.font.SysFont('Comic Sans MS', 48)

clock = pygame.time.Clock()
BODY_COLOR = (175, 184, 199)
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,bom,bom_count):
        super().__init__()
        self.x=x
        self.y=y
        self.bomb = bom
        self.bomb_count = bom_count
        self.width = 30
        self.height = 30
        self.image = (pygame.transform.scale(pygame.image.load("block.png"),(self.width,self.height))).convert()
        self.bomb_image = (pygame.transform.scale(pygame.image.load("bomb.png"),(self.width,self.height))).convert()
        self.flag_image = (pygame.transform.scale(pygame.image.load("flag.png"),(self.width,self.height))).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.flagged = False
        #self.surf = pygame.Surface((30, 30))
        #self.surf.fill((128,255,40))
        
    def update(self,win):
        self.draw(win)
    def draw(self,win):
        if self.flagged:
            win.blit(self.flag_image,(self.x,self.y))   
        else: 
            win.blit(self.image,(self.x,self.y))

timer_event = pygame.USEREVENT+1
#pygame.time.set_timer(timer_event, 1000)
running = True
counter=0

timer_rect_box = pygame.Rect(WIN_WIDTH-80, 10, 60, 30)
timer_text = myfont.render(str(counter), True, (232, 26, 12))
#text_rect = text.get_rect(center = win.get_rect().center)

class Start_Lost:
    def __init__(self):
        self.start_img = pygame.transform.scale(pygame.image.load('start.png'),(40,40))
        self.start_img.convert()
        self.lost_img = pygame.transform.scale(pygame.image.load('lost.png'),(40,40))
        self.lost_img.convert()

        self.start_img_rect = self.start_img.get_rect()
        self.start_img_rect.midtop = WIN_WIDTH//2, 10

        self.lost_img_rect = self.lost_img.get_rect()
        self.lost_img_rect.midtop = WIN_WIDTH//2, 10

        self.gamestate = 'ready'
    def update(self,win):
        self.draw(win)
    def draw(self,win):
        if self.gamestate == 'ready':
            win.blit(self.start_img, self.start_img_rect)
        elif self.gamestate == 'playing':
            win.blit(self.start_img, self.start_img_rect)
        elif self.gamestate == 'lost':
            print('LOST')
            win.blit(self.lost_img, self.lost_img_rect)

blocks_list = []
def create_bombs():    
    b_list = []
    for i in range(TOTAL_BLOCKS):    
        if i>=15:
            b_list.append('n')
            continue
        b_list.append('b')

    random.shuffle(b_list)
    return b_list

div_by_10 = []
div_by_9 = []
div_normal = []
def calculate_numbers(b_list):  # this function creates bombs count list
    neighbor_cell_list = []  
    bombs_count_list = []
    for i in range(TOTAL_BLOCKS):
        bombs_count_list.append(0)
    for index,b in enumerate(b_list):
        bomb_count = 0
        neighbor_cell_list.clear()
        if b == 'n':
            if index % 10 == 0:  #left edge blocks
                div_by_10.append(index)
                midtop = index-10
                neighbor_cell_list.append(midtop)
                topright = index-9
                neighbor_cell_list.append(topright)                
                right = index+1
                neighbor_cell_list.append(right)
                midbottom = index+10
                neighbor_cell_list.append(midbottom)
                bottomright = index+11
                neighbor_cell_list.append(bottomright)
                
                for cell in neighbor_cell_list:
                    try:
                        if b_list[cell] == 'b':
                            bomb_count = bomb_count + 1         
                    except IndexError as error:
                        pass
                bombs_count_list[index] = bomb_count

            elif index % 10 == 9:     #Right edge blocks
                div_by_9.append(index)
                topleft = index-11
                neighbor_cell_list.append(topleft)
                midtop = index-10
                neighbor_cell_list.append(midtop)
                
                left = index-1
                neighbor_cell_list.append(left)
                
                bottomleft = index+9
                neighbor_cell_list.append(bottomleft)
                midbottom = index+10
                neighbor_cell_list.append(midbottom)
                
                for cell in neighbor_cell_list:
                    try:
                        if b_list[cell] == 'b':
                            bomb_count = bomb_count + 1         
                    except IndexError as error:
                        pass
                
                bombs_count_list[index] = bomb_count

            else:
                div_normal.append(index)
                topleft = index-11
                if topleft >= 0:
                    neighbor_cell_list.append(topleft)
                midtop = index-10
                if midtop >= 0:
                    neighbor_cell_list.append(midtop)
                topright = index-9
                if topright >= 0:
                    neighbor_cell_list.append(topright)
                left = index-1
                neighbor_cell_list.append(left)
                right = index+1
                if right >= 0:
                    neighbor_cell_list.append(right)
                bottomleft = index+9
                if bottomleft >= 0:
                    neighbor_cell_list.append(bottomleft)
                midbottom = index+10
                if midbottom >= 0:
                    neighbor_cell_list.append(midbottom)
                bottomright = index+11
                if bottomright >= 0:
                    neighbor_cell_list.append(bottomright)
                
                for cell in neighbor_cell_list:
                    try:
                        if b_list[cell] == 'b':
                            bomb_count = bomb_count + 1         
                    except IndexError as error:
                        pass
                
                bombs_count_list[index] = bomb_count
    return bombs_count_list

bombs_list = create_bombs()
bom_count_list = calculate_numbers(bombs_list)

#print('div by 10',div_by_10)
#print('div by 9',div_by_9)
#print('div normal',div_normal)

for i in range(10):
    for j in range(10):
        j = 10 * i + j
        #print(bombs_list[j],end='')
    #print()

for i in range(10):
    for j in range(10):
        j = 10 * i + j
        #print(bom_count_list[j],end='')
    #print()

x = 0
y = 100
for i in range(TOTAL_BLOCKS):
    b = Block(x,y,bombs_list[i],bom_count_list[i])
    x = x + 30
    if i%10 == 9:
        y = y + 30
        x = 0
    
    blocks_list.append(b)

start_button = Start_Lost()

def redrawWindow():
    win.fill(BODY_COLOR)
    start_button.update(win)
    rect_surf = pygame.draw.rect(win, (0,0,0), timer_rect_box)
    timer_rect = timer_text.get_rect(center = rect_surf.center)
    win.blit(timer_text, timer_rect)
    for b in blocks_list:
        b.update(win)        
    pygame.display.update()


while running:
    #clock.tick(100)
    for event in pygame.event.get():
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            mouse_location = pygame.mouse.get_pos()
            #print("Left Mouse Key is being pressed")
            #print(pygame.mouse.get_pos())
            if start_button.start_img_rect.collidepoint(mouse_location):
                if start_button.gamestate == 'ready' or start_button.gamestate == 'playing':                
                        start_button.gamestate = 'playing'
                        pygame.time.set_timer(timer_event, 1000)
                elif start_button.gamestate == 'lost':
                    counter = 0
                    start_button.gamestate = 'playing'
                    pygame.time.set_timer(timer_event, 1000)
            else:
                for b in blocks_list:
                #print(b.rect.collidepoint(pygame.mouse.get_pos()))
                    if b.rect.collidepoint(mouse_location):
                        print('YES',b.rect,'MOUSE',mouse_location)
                        break
                #else:
                #    print('NO',b.rect,'MOUSE',pygame.mouse.get_pos())
        elif mouse_pressed[2]:
            mouse_location = pygame.mouse.get_pos()
            for b in blocks_list:
                #print(b.rect.collidepoint(pygame.mouse.get_pos()))
                    if b.rect.collidepoint(mouse_location):
                        print('YES',b.rect,'MOUSE',mouse_location)
                        break
            
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:            
            counter += 1
            timer_text = myfont.render(str(counter), True, (232, 26, 12))           
            if counter == 50:
                start_button.gamestate = 'lost'
                pygame.time.set_timer(timer_event, 0) 
                
        #elif event.type == pygame.MOUSEMOTION:
            #x,y  = pygame.mouse.get_pos()            
        #    rel_x,rel_y = pygame.mouse.get_rel()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        pass
    if keys[pygame.K_SPACE]:        
        pass
    if keys[pygame.K_r]:        
        pass
        
    redrawWindow()
    space = False
pygame.quit()
