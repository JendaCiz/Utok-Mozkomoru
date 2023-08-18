import pygame
import random

pygame.init()

width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dementor's attack")

# Nastaveni hry
fps = 60
clock = pygame.time.Clock()

# Zakladni hodnoty
player_start_lives = 5
dementor_start_speed = 2
dementor_speed_acceleration = 0.5
score = 0

# pohyb mozkomora
dementor_x = random.choice([-1, 1])
dementor_y = random.choice([-1, 1])

player_lives = player_start_lives
dementor_speed = dementor_start_speed

# Obrazky
background_image = pygame.image.load("img/hogwarts-castle.jpg")
background_image_rect = background_image.get_rect()
background_image_rect.center = (width//2, height//2)

dementor_img = pygame.image.load("img/mozkomor.png")
dementor_img_rect = dementor_img.get_rect()
dementor_img_rect.center = (width//2, height//2)

# Barvy
white = pygame.Color("#fff9f9")

# Fonty
potter_font_big = pygame.font.Font("fonts/Harry.ttf", 90)
potter_font_middle = pygame.font.Font("fonts/Harry.ttf", 50)


# Text
score_text = potter_font_middle.render(f"skore: {score}", True, white)
score_text_rect = score_text.get_rect()
score_text_rect.topright = (width - 30, 10)

lives_text = potter_font_middle.render(f"Lives: {player_lives}", True, white)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (width -30, 50)

game_over_text = potter_font_big.render("Game Over", True, white)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (width//2, height//2)

continue_text = potter_font_middle.render("Click for continue", True, white)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width//2, height//2 + 50)

# Zvuky
success_click = pygame.mixer.Sound("media/success_click.wav")
miss_click = pygame.mixer.Sound("media/miss_click.wav")
pygame.mixer.music.load("media/bg-music-hp.wav")
success_click.set_volume(0.1)
miss_click.set_volume(0.1)



#hlavni cyklus
lets_continue = True
pygame.mixer.music.play(-1, 0.00)
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x = event.pos[0]
            click_y = event.pos[1]

            # bylo kliknuto na mozkomora
            if dementor_img_rect.collidepoint(click_x, click_y):
                success_click.play()
                score += 1
                dementor_speed += dementor_speed_acceleration

                previous_x = dementor_x
                previous_y = dementor_y

                while previous_x == dementor_x and previous_y == dementor_y:
                    dementor_x = random.choice([-1, 1])
                    dementor_y = random.choice([-1, 1])
            else:
                miss_click.play()
                player_lives -= 1

    # Pohyb mozkomora
    dementor_img_rect.x += dementor_x * dementor_speed
    dementor_img_rect.y += dementor_y * dementor_speed
    
   # Pohybujeme mozkomorem
    if dementor_img_rect.left <= 0:
        dementor_x = 1
    elif dementor_img_rect.right >= width:
        dementor_x = -1

    if dementor_img_rect.top <= 0:
        dementor_y = 1
    elif dementor_img_rect.bottom >= height:
        dementor_y = -1


    # Update textu score a life
    score_text = potter_font_middle.render(f"skore: {score}", True, white)
    lives_text = potter_font_middle.render(f"Lives: {player_lives}", True, white)
    # Vykresleni obrazku
    screen.blit(background_image, background_image_rect)
    screen.blit(dementor_img, dementor_img_rect)


    # Texty
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)

    # update obrazvky
    pygame.display.update()


    # Zpomaleni cyklu
    clock.tick(fps)

    # Kontrola konce hry 
    if player_lives == 0:
        game_over = True
        pygame.mixer.music.stop()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    lets_continue = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Toto umožní hráči kliknout kdekoliv na obrazovce pro opětovné spuštění hry
                    game_over = False
                    pygame.mixer.music.play(-1, 0)
                    player_lives = player_start_lives
                    score = 0
                    dementor_speed = dementor_start_speed

            screen.blit(background_image, background_image_rect)
            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(continue_text, continue_text_rect)
            pygame.display.update()
            clock.tick(fps)
    


pygame.quit()