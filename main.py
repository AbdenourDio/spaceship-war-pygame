global red
global yellow
import pygame


pygame.init()
pygame.mixer.init()
WHITE = (255, 255, 255)
YELlOW = (255, 255, 0)
RED = (255, 0, 0)
MOVING_SPEED = 8
HEALTH = 8
FONT = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((640, 640))
YELLOW_SPACESHIP_IMG = pygame.image.load('Assets/spaceship_yellow.png')
RED_SPACESHIP_IMG = pygame.image.load('Assets/spaceship_red.png')
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 44)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
pygame.display.set_caption('A GAME!')
clock = pygame.time.Clock()
yellow = pygame.Rect(5, 320, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
red = pygame.Rect(580, 320, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
BG_IMG = pygame.image.load('Assets/space.png')
BG = pygame.transform.scale(BG_IMG, (640, 640))
bullet_sound = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
hit_sound = pygame.mixer.Sound('Assets/Grenade+1.mp3')
red_bullets = []
yellow_bullets = []

def draw_window(yellow, red):
    screen.blit(BG, (0, 0))
    pygame.draw.line(screen, (0, 0, 0), (320, 0), (320, 640), width=3)
    screen.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    screen.blit(RED_SPACESHIP, (red.x, red.y))

def moving_yellow_spaceship():
    keys = pygame.key.get_pressed()
    if yellow.left > 0 and keys[pygame.K_q]:
        yellow.x -= MOVING_SPEED
    if yellow.right < 320 and keys[pygame.K_d]:
        yellow.x += MOVING_SPEED
    if yellow.top > 0 and keys[pygame.K_z]:
        yellow.y -= MOVING_SPEED
    if yellow.bottom < 640 and keys[pygame.K_s]:
        yellow.y += MOVING_SPEED
        return None

def moving_red_spaceship():
    keys = pygame.key.get_pressed()
    if red.left > 320 and keys[pygame.K_LEFT]:
        red.x -= MOVING_SPEED
    if red.right < 640 and keys[pygame.K_RIGHT]:
        red.x += MOVING_SPEED
    if red.top > 0 and keys[pygame.K_UP]:
        red.y -= MOVING_SPEED
    if red.bottom < 640 and keys[pygame.K_DOWN]:
        red.y += MOVING_SPEED
        return None

def game_over():
    okay = False
    play_again_text = FONT.render('PRESS ENTER TO PLAY AGAIN...', True, WHITE)
    screen.blit(play_again_text, (140, 400))
    pygame.display.update()
    if not okay:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()
            else:

                okay = True
    return None

def reset_game():
    global yellow
    global red
    global yellow_health
    global red_health
    yellow_health = HEALTH
    red_health = HEALTH
    yellow = pygame.Rect(5, 320, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(580, 320, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets.clear()
    yellow_bullets.clear()
    pygame.display.update()

def main():
    global yellow_health
    global red_health
    running = True
    yellow_health = HEALTH
    red_health = HEALTH
    winner = None

    while running:
        if winner is None:
            clock.tick(60)
            draw_window(yellow, red)
            moving_yellow_spaceship()
            moving_red_spaceship()
            red_bullet_x = red.x - 7
            red_bullet_y = red.y
            for bullet in red_bullets:
                pygame.draw.rect(screen, (255, 69, 0), bullet)
            for bullet in yellow_bullets:
                pygame.draw.rect(screen, (255, 69, 0), bullet)
            for bullet in yellow_bullets:
                pygame.draw.rect(screen, (255, 69, 0), bullet)
                bullet.x += 10
                if bullet.colliderect(red):
                    red_health -= 1
                    hit_sound.play()
                    yellow_bullets.remove(bullet)
                elif bullet.x > 640:
                    yellow_bullets.remove(bullet)
                else:
                    pass
            for bullet in red_bullets:
                bullet.x -= 10
                if bullet.colliderect(yellow):
                    yellow_health -= 1
                    hit_sound.play()
                    red_bullets.remove(bullet)
                elif bullet.x < 0:
                    red_bullets.remove(bullet)
                else:
                    pass
            yellow_health_text = FONT.render(f'HEALTH: {yellow_health}', True, WHITE)
            red_health_text = FONT.render(f'HEALTH: {red_health}', True, WHITE)
            screen.blit(yellow_health_text, (20, 5))
            screen.blit(red_health_text, (500, 5))
            red_win_text = FONT.render('RED WINS THE GAME\n       SUUUUUU!!!!', True, RED)
            yellow_win_text = FONT.render('YELLOW WINS THE GAME\n          SUUUUUU!!!!', True, YELlOW)
            if red_health == 0:
                winner = "YELLOW"
                screen.blit(yellow_win_text, (10, 300))
                pygame.display.update()
                game_over()
            if yellow_health == 0:
                winner = "RED"
                screen.blit(red_win_text, (340, 300))
                pygame.display.update()
                game_over()
            pygame.display.update()
            for event in pygame.event.get():
                running = False if event.type == pygame.QUIT else True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        bullet_rect = pygame.Rect(yellow.x + 43, yellow.y + 26, 8, 3.5)
                        yellow_bullets.append(bullet_rect)
                        bullet_sound.play()
                    if event.key == pygame.K_RCTRL:
                        bullet_rect = pygame.Rect(red_bullet_x, red_bullet_y + 26, 8, 3.5)
                        red_bullets.append(bullet_rect)
                        bullet_sound.play()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("i am listening boy but...")
                reset_game()
                winner = None
            elif event.type == pygame.QUIT:
                pygame.quit()
main()