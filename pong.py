import pygame
pygame.font.init()

WIDTH, HEIGHT = 1300, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
fps = 60
light_blue = (210,255,255)
red = (255,0,50)
blue = (0,0,255)
black = (0,0,0)
rect1 = pygame.Rect(20, HEIGHT/2-93.75, 20, 187.5)
rect2 = pygame.Rect(WIDTH-40, HEIGHT/2-93.75, 20, 187.5)
ball = pygame.Rect(50, HEIGHT/2, 10, 10)
COLLIDE_1 = pygame.USEREVENT + 1
COLLIDE_2 = pygame.USEREVENT + 2
COLLIDE_3 = pygame.USEREVENT + 3
COLLIDE_4 = pygame.USEREVENT + 4
COLLIDE_5 = pygame.USEREVENT + 5
COLLIDE_6 = pygame.USEREVENT + 6
GAME_OVER = pygame.USEREVENT + 7
game_over = False
score_font = pygame.font.SysFont("comicsans", 30)
collision_index = 0
round_index = 0
x_traj = 7
y_traj = 10
score_1 = 0
score_2 = 0

def draw_window(rect1, rect2, ball, score_1, score_2):
    WIN.fill(light_blue)
    pygame.draw.rect(WIN, red, [rect1.x,rect1.y,rect1.width,rect1.height], 10)
    pygame.draw.rect(WIN, red, [rect2.x,rect2.y,rect2.width,rect2.height], 10)
    pygame.draw.circle(WIN, blue, (ball.x+ball.width/2, ball.y+ball.height/2), ball.width, 10)
    score1_txt = score_font.render(str(score_1), 1, black)
    WIN.blit(score1_txt, (WIDTH/2-score1_txt.get_width()-40, 30))
    score2_txt = score_font.render(str(score_2), 1, black)
    WIN.blit(score2_txt, (WIDTH/2-score2_txt.get_width()+40, 30))
    pygame.display.update()

def move_rect1(keys_pressed, rect1):
    if game_over!=True:
        if keys_pressed[pygame.K_w] and rect1.y>0:
            rect1.y -= 5
        elif keys_pressed[pygame.K_s] and rect1.y<HEIGHT-rect1.height:
            rect1.y += 5

def move_rect2(keys_pressed, rect2):
    if game_over!=True:
        if keys_pressed[pygame.K_UP] and rect2.y>0:
            rect2.y -= 5
        elif keys_pressed[pygame.K_DOWN] and rect2.y<HEIGHT-rect2.height:
            rect2.y += 5

def ball_mov(ball, collision, x_traj):
    if game_over!=True:
        if collision==0:
            ball.x += x_traj
            ball.y += y_traj
        elif collision==1:
            ball.x += x_traj
            ball.y -= y_traj
        elif collision==2:
            x_traj = -7
            ball.x += x_traj
            ball.y -= y_traj
        elif collision==3:
            ball.x += x_traj
            ball.y += y_traj
        elif collision==4:
            ball.x -= x_traj
            ball.y += y_traj
        elif collision==5:
            ball.x -= x_traj
            ball.y += y_traj
        elif collision==6:
            ball.x -= x_traj
            ball.y -= y_traj

def collision(ball, rect1, rect2):
    global score_1, score_2
    if ball.y>HEIGHT-ball.height:
        pygame.event.post(pygame.event.Event(COLLIDE_1))
    elif ball.colliderect(rect2):
        if ball.y<rect2.y+rect2.height/2:
            pygame.event.post(pygame.event.Event(COLLIDE_2))
        else:
            pygame.event.post(pygame.event.Event(COLLIDE_5))
    elif ball.y<0:
        pygame.event.post(pygame.event.Event(COLLIDE_3))
    elif ball.colliderect(rect1):
        if ball.y<rect1.y+rect1.height/2:
            pygame.event.post(pygame.event.Event(COLLIDE_6))
        else:
            pygame.event.post(pygame.event.Event(COLLIDE_4))
    if game_over == False:
        if ball.x<0:
            score_2 += 1
            pygame.event.post(pygame.event.Event(COLLIDE_4))
        elif ball.x>WIDTH-ball.width:
            score_1 += 1
            pygame.event.post(pygame.event.Event(COLLIDE_2))

def gameOver(score_1, score_2):
    if score_1==5 or score_2==5:
        pygame.event.post(pygame.event.Event(GAME_OVER))

def main():
    global collision_index, score_1, score_2, game_over, x_traj
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == COLLIDE_1:
                if collision_index==5:
                    x_traj = -7
                elif collision_index==4:
                    x_traj = 7
                collision_index = 1
            elif event.type == COLLIDE_2:
                collision_index = 2
            elif event.type == COLLIDE_3:
                if collision_index==2:
                    x_traj = -7
                elif collision_index==6:
                    x_traj = 7
                collision_index = 3
            elif event.type == COLLIDE_4:
                collision_index = 4
            elif event.type == COLLIDE_5:
                collision_index = 5
            elif event.type == COLLIDE_6:
                collision_index = 6
            elif event.type == GAME_OVER:
                game_over = True
                if score_1==5:
                    winner_txt = score_font.render("Left side wins!", 1, black)
                    WIN.blit(winner_txt, (WIDTH/2-winner_txt.get_width()/2, HEIGHT/2))
                elif score_2==5:
                    winner_txt = score_font.render("Right side wins!", 1, black)
                    WIN.blit(winner_txt, (WIDTH/2-winner_txt.get_width()/2, HEIGHT/2))
                pygame.display.update()

        keys_pressed = pygame.key.get_pressed()
        move_rect1(keys_pressed, rect1)
        move_rect2(keys_pressed, rect2)
        ball_mov(ball, collision_index, x_traj)
        collision(ball, rect1, rect2)
        draw_window(rect1, rect2, ball, score_1, score_2)
        gameOver(score_1, score_2)

    pygame.quit()

if __name__ == "__main__":
    main()