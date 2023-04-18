import pygame
import os 
pygame.mixer.init()
import threading
WIDTH_IMAGE_SPACE, HEIGHT_IMAGE_SPACE = 55,40
WIDHT, HEIGHT =  900, 500

life = 20
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
BORDER = pygame.Rect(WIDHT//2, 0, 10, HEIGHT)
WIN = pygame.display.set_mode((WIDHT, HEIGHT))
COLOR = (0,0,0)
RED_COLOR = (255,0,0)
YELLOW_COLOR = (255,255,0)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
FUNDO_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Fundosond.mp3'))
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
pygame.display.set_caption("Passando o tempo!")
pygame.font.init()
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 55)
YELLOW_SPACE_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACE_IMAGE,(WIDTH_IMAGE_SPACE,HEIGHT_IMAGE_SPACE)),90)

RED_SPACE_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACE_IMAGE,(WIDTH_IMAGE_SPACE,HEIGHT_IMAGE_SPACE)),270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','FUNDO2.JPG')),(WIDHT, HEIGHT))

def draw_windows(red, yellow, red_bullets, yellow_bullets, red_life, yellow_life):
    WIN.blit(SPACE, (0, 0)) 
    pygame.draw.rect(WIN, COLOR, BORDER)
   
    red_health_text = HEALTH_FONT.render("Vida: " + str(red_life), 1, (255,255,255))
    yellow_health_text = HEALTH_FONT.render("Vida: " + str(yellow_life), 1, (255,255,255))
    
    WIN.blit(red_health_text, (WIDHT - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))  
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    
  
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_COLOR, bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_COLOR, bullet)
    
    pygame.display.update()
    
def yellow_handle_moviment(key_pressed, yellow):
        if(key_pressed[pygame.K_a] and yellow.x - VEL > 0):
            yellow.x -= VEL

        if(key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 12):
            yellow.x += VEL
        
        if(key_pressed[pygame.K_w] and yellow.y - VEL > 0 ):
            yellow.y -= VEL
            
        if(key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 11):
            yellow.y += VEL

def red_handle_moviment(key_pressed, red):
        if(key_pressed[pygame.K_LEFT]  and red.x - VEL > 450 + 11):
            red.x -= VEL

        if(key_pressed[pygame.K_RIGHT] and red.x + VEL < WIDHT - 50):
            red.x += VEL
        
        if(key_pressed[pygame.K_UP]  and red.y - VEL > 0):
            red.y -= VEL
            
        if(key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 11):
            red.y += VEL
            
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1, (255,255,255))
    draw_text1 = WINNER_FONT.render("By: Filipe Carvalho :)",1, (255,255,255))
    WIN.blit(draw_text, (WIDHT/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    WIN.blit(draw_text1, (WIDHT/2 - draw_text1.get_width()/2, HEIGHT/2 - (draw_text1.get_height()/2) + 50))
    pygame.display.update()
    pygame.time.delay(5000)

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if(red.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            
        elif( bullet.x > WIDHT):
            yellow_bullets.remove(bullet)

  
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            
        elif( bullet.x < 0):
            red_bullets.remove(bullet)
def play_music():
    pygame.mixer.Sound(os.path.join('Assets', 'Fundosond.mp3'))
    pygame.mixer.music.play(loops=-1)  
            
def main():
    clock = pygame.time.Clock()
    run = True
    red = pygame.Rect(700,100, WIDTH_IMAGE_SPACE,HEIGHT_IMAGE_SPACE)
    yellow = pygame.Rect(100,300, WIDTH_IMAGE_SPACE,HEIGHT_IMAGE_SPACE)
    
    red_bullets = []
    yellow_bullets = []
    
    red_life = 20
    yellow_life = 20
    
    pygame.mixer.music.load('Assets/Fundosond.mp3')
    pygame.mixer.music.play(loops=-1)
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()
                
            if(event.type == pygame.KEYDOWN):
                
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if(event.type == RED_HIT):
                red_life -=1
                BULLET_HIT_SOUND.play()
                
            if(event.type == YELLOW_HIT):
                yellow_life -=1
                BULLET_HIT_SOUND.play()

                
        win_text = ""
        if(red_life <= 0):
            win_text = "O Jogador Amarelo Venceu!"

            
        if(yellow_life <= 0):
             win_text = "O Jogador Vermelho Venceu!"

            
        if(win_text !=""):
            draw_winner(win_text)
            break
              
        key_pressed = pygame.key.get_pressed()
        yellow_handle_moviment(key_pressed, yellow)
        red_handle_moviment(key_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_windows(red, yellow, red_bullets, yellow_bullets, red_life, yellow_life)    

    main()
    

if __name__ == '__main__':
    t = threading.Thread(target=play_music)
    t.start()
    main()
    
    