import sys
from os import walk
from turtledemo import clock

import pygame

image_path = '/data/data/Pixelfire.myapp/app'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("X game")
icon = pygame.image.load(image_path + 'images/icon.png')

ghost = pygame.image.load(image_path + 'images/ghost.png').convert_alpha()
ghost_list_in_game = []

pygame.display.set_icon(icon)

bg = pygame.image.load(image_path + 'images/bg.jpg').convert_alpha()
walk_left = [

    pygame.image.load(image_path + 'images/player.l/l1.PNG').convert_alpha(),
    pygame.image.load(image_path + 'images/player.l/l2.PNG').convert_alpha(),
    pygame.image.load(image_path + 'images/player.l/l3.PNG').convert_alpha(),
    pygame.image.load(image_path + 'images/player.l/l4.PNG').convert_alpha(),

]

walk_right = [
    pygame.image.load(image_path + 'images/player.R/r1.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player.R/r2.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player.R/r3.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player.R/r4.png').convert_alpha(),
]




player_anim_count = 0
bg_x = 0

player_speed = 7
player_x = 200
player_y = 200

is_jump = False
jump_count = 9

#Музика
jump_sound = pygame.mixer.Sound(image_path +'sound/8bit1.wav')
jump_sound.set_volume(0.1)

#Таймер мобов
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

#Шришты
label = pygame.font.Font(image_path + 'fonts/digital-match-sans-one.ttf', 50)
lose_label = label.render('YOU LOSE:(', False, (193, 196, 199))
restart_label = label.render('RESTART', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft = (195, 160))

bullet_left = 5
bullet = []
bullet_img = pygame.image.load(image_path + 'images/bullet1.png').convert_alpha()


gameplay = True

running = True
while True:

  screen.blit(bg, (bg_x, 0))
  screen.blit(bg, (bg_x + 640, 0))

  if gameplay:
      player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))


      if ghost_list_in_game:
             for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                  gameplay = False



      keys= pygame.key.get_pressed()

      if keys[pygame.K_LEFT]:
                screen.blit(walk_left[player_anim_count], (player_x, player_y))
      else:
                screen.blit(walk_right[player_anim_count], (player_x, player_y))

        # Рамки чек бокса
      if keys[pygame.K_LEFT] and player_x > 30:
                player_x -= player_speed
      elif keys[pygame.K_RIGHT] and player_x < 550:
                player_x += player_speed

      if not is_jump:
         if keys[pygame.K_SPACE]:
            is_jump = True
            jump_sound.play()
      else:
                if jump_count >= -9:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2)/2
                    else:
                        player_y += (jump_count ** 2)/2
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 9

      if player_anim_count == 3:
                player_anim_count = 0
      else:
                player_anim_count += 1

                bg_x -= 5
      if bg_x == -640:
                bg_x = 0

      if bullet:
          for (i, el) in enumerate (bullet):
              screen.blit(bullet_img,(el.x, el.y))
              el.x += 4

              if el.x > 640:
                  bullet.pop()

              if ghost_list_in_game:
                  for (index, ghost_el) in enumerate(ghost_list_in_game):
                      if el.colliderect(ghost_el):
                          ghost_list_in_game.pop(index)
                          bullet.pop(i)



  else:
      screen.fill((87, 88, 89))
      screen.blit(lose_label, (180, 100))
      screen.blit(restart_label, restart_label_rect)

      mouse = pygame.mouse.get_pos()
      if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
          gameplay = True
          player_x = 200
          ghost_list_in_game.clear()
          bullet.clear()
          bullet_left = 5


  pygame.display.update()

  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(645, 200)))
        if  gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullet_left > 0:
            new_bullet = (bullet_img.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullet.append(new_bullet)
            bullet_left -= 1


  clock.tick(20)