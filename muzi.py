# -*- coding: utf-8 -*-
"""
This great game is made by muzi
"""

from sys import exit
import pygame
from pygame.locals import *
from Role import *
import random

#1	init the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('拯救小丹丹')
shoot_frequency = 0
enemy_frequency = 0
bomb_frequence = 0
player_down_index = 16
score = 0
clock = pygame.time.Clock()
running = 1  
win = 0
level = 0
final_score = 10000
flag = 1


#2	load the music 
bullet_sound = pygame.mixer.Sound('resources/sound/bullet,wav')
enemy_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down_sound')
gameover_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
get_bomb = pygame.mixer.Sound('resources/sound/get_bomb.wav')

bullet_sound.set_volume(0.3)
enemy_down_sound.set_volume(0.3)
gameover_sound.set_volume(0.3)
get_bomb.set_volume(0.3)

pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.3)

#3	load the images 
background = pygame.image.load("resources/image/background.png").convert()
game_over = pygame.image.load("resources/image/gameover.png")
youwin = pygame.image.load("resources/image/youwin.png")
plane_img = pygame.image.load("resources/image/shoot.png")
welcome = pygame.image.load("resources/image/shoot_background.png")
welcome_rect = pygame.Rect(460, 440, 500, 560)
welcome_img = welcome.subsurface(welcome_rect).convert_alpha()


#4 	set the game
player_rect = []  #use for save the player images
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))

player_pos = [190,480]
player = Player(plane_img, player_rect, player_pos)

bomb_rect = pygame.Rect(267, 390, 60, 95)
bomb_img = plane_img.subsurface(bomb_rect)

#5	bullet's surface
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

#6  enemy's surface
enemy_rect = pygame.Rect(534, 612, 57, 43)
enemy_img = plane_img.subsurface(enemy_rect)
enemy_down_imgs = []
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies = pygame.sprite.Group()
#use for describe the crash.
enemies_down = pygame.sprite.Group()
bombs = pygame.sprite.Group()

#second =time/1000

while flag:
	time = pygame.time.get_ticks()
	
	# show the welcome
	screen.fill(0)
 	screen.blit(background, (0, 0))

 	pygame.font.init()
	font = pygame.font.Font(None, 48)
	text = font.render("Made by muzi",True, (128,100,128))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 65
	screen.blit(bomb_img, (100,100))
	screen.blit(welcome_img, (0, 0))
	#screen.blit(text_2, text_rect_2)
	screen.blit(text, text_rect)
	#screen.blit(text, text_rect)

 	pygame.display.update()
 	for event in pygame.event.get():
 		if event.type == pygame.QUIT:
 			pygame.quit()
 			exit()
 	pygame.display.update()
 	if time>5000:
 		flag = 0

while running:
	# the bigest flip is 60

	clock.tick(60)
	time = pygame.time.get_ticks()
	second =time/1000
	level = score/1000

	#shoot
	if not player.is_attacked:
	 	if shoot_frequency%15 ==0:
	 		bullet_sound.play()
	 		player.shoot(bullet_img)
	 	shoot_frequency+=1
	 	if shoot_frequency > 20:
	 		shoot_frequency = 0
	#creat the enemy
	if enemy_frequency %50 ==0:
 		enemy_pos =  [random.randint(0,SCREEN_WIDTH - enemy_rect.width), 0]
 		enemy = Enemy(enemy_img, enemy_down_imgs, enemy_pos)
 		enemies.add(enemy)  #add the enemy to the enemys
 	enemy_frequency+=1

 	if enemy_frequency>80:
 		enemy_frequency+=1
 	#delete the bullet if it has go out the screen
 	if bomb_frequence % 1000 == 0:
 		bomb_pos =  [random.randint(30, SCREEN_WIDTH - 100), 0]
 		bomb_1 = Bomb(bomb_img, bomb_pos)
 		bombs.add(bomb_1)  									#add the bomb to the bombs
 	bomb_frequence+=1
 	if bomb_frequence >= 1999:
 		bomb_frequence = 0
 	for bomb in bombs:
 		bomb.move()
 		if pygame.sprite.collide_circle(bomb, player):
 			bombs.remove(bomb)
 			get_bomb.play()	
 			if player.equ<3:
 				player.equ += 1
 			

 		if bomb.rect.top > SCREEN_HEIGHT:
 			bombs.remove(bomb)

 	for bullet in player.bullets:
 		bullet.move()
 		if bullet.rect.bottom < 0:
 			player.bullets.remove(bullet)
 	#manipulate the enemy
 	for enemy1 in enemies:
 		enemy1.move()
 		if pygame.sprite.collide_circle(enemy1, player):
 			enemies_down.add(enemy1)
 			enemies.remove(enemy1)	
 			player.is_attacked = True
 			gameover_sound.play()
 			break
 		if enemy1.rect.top > SCREEN_HEIGHT:
 			enemies.remove(enemy1)
 	# add the crash enemy into the set of enemy_down
 	enemies1_down = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
 	for enemy_down in enemies1_down:
 		enemies_down.add(enemy_down)
	#draw the backgroud

 	screen.fill(0)
 	screen.blit(background, (0, 0))
 	#____________________________________________draw anything below this_____________________________
 	#change the win flag
 
 	if score == final_score:
 		win = 1
 		running = 0 
 	#draw the player's plane
 	if not player.is_attacked:
 		screen.blit(player.image[player.img_index], player.rect)
 		player.img_index =shoot_frequency/8
 	else:
 		player.img_index =player_down_index /8
 		screen.blit(player.image[player.img_index], player.rect)
 		player_down_index += 1
 		if player_down_index >47:
 			running = 0
 	#draw the crash
 	for enemy_down in enemies_down:
 		if enemy_down.down_index == 0:
 			enemy_down_sound.play()
 		if enemy_down.down_index > 7:
 			enemies_down.remove(enemy_down)
 			score += 100
 			continue
 		screen.blit(enemy_down.down_imgs[enemy_down.down_index / 2], enemy_down.rect)
 		enemy_down.down_index += 1
 	#draw the bullet and enmeies
 	for bomb in bombs:
 		screen.blit(bomb.image, bomb.rect.midbottom)

 	player.bullets.draw(screen)
 	enemies.draw(screen)

 	#show the score
 	font = pygame.font.Font(None, 40)
 	score_text = font.render("Score:" + str(score) , True, (128, 128, 128))
 	text_rect = score_text.get_rect()
 	text_rect.topleft = [10, 10]
 	screen.blit(score_text, text_rect)

 	level_text =font.render("Level:"+str(level+1), True, (128, 128, 128))
 	text_rect = score_text.get_rect()
 	text_rect.topleft = [350, 10]
 	screen.blit(level_text, text_rect)
 	#Update the screen
 	pygame.display.update()
 	#control your plane
	for event in pygame.event.get():
 		if event.type ==pygame.QUIT:
 			pygame.quit()
 			exit()
 	#listen to the key event
 	key = pygame.key.get_pressed()
 	if not player.is_attacked:
 		if key[K_w] or key[K_UP]:
 			player.moveup()
 		if key[K_s] or key[K_DOWN]:
 			player.movedown()
 		if key[K_a] or key[K_LEFT]:
 			player.moveleft()
 		if key[K_d] or key[K_RIGHT]:
 			player.moveright()

#win or lose

if win:
	font = pygame.font.Font(None, 48)
	text = font.render("Score:" + str(score)+"   level:" +str(level), True, (128,100,128))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 24
	screen.blit(youwin, (0, 0))
	screen.blit(text, text_rect)
else:
	font = pygame.font.Font(None, 48)
	text = font.render("Score:" + str(score)+"   level:" +str(level), True, (128,100,128))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 24
	screen.blit(game_over, (0, 0))
	screen.blit(text, text_rect)


#you can go into the next 


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
































