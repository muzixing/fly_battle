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
shoot_frequency = 1
enemy_frequency = 1
bomb_frequence = 1
player_down_index = 16
score = 0
clock = pygame.time.Clock()
running = 1  
win = 0
level = 0
final_score = 100000
flag = 1
bomb_freze =10


#2	load the music 
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down_sound.wav')
gameover_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
get_bomb = pygame.mixer.Sound('resources/sound/get_bomb.wav')
get_double = pygame.mixer.Sound('resources/sound/get_double_laser.wav')
use_bomb = pygame.mixer.Sound('resources/sound/use_bomb.wav')

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

#4 	set the game
welcome_rect = pygame.Rect(460, 440, 500, 560)
welcome_img = welcome.subsurface(welcome_rect).convert_alpha()

player_rect = []  #use for save the player images
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))

player_pos = [190,480]
player = Player(plane_img, player_rect, player_pos)

bomb_rect = pygame.Rect(268, 399, 55, 85)
bomb_img = plane_img.subsurface(bomb_rect)

big_bomb_rect = pygame.Rect(105, 121, 55, 101)	#perfect rect
big_bomb_img = plane_img.subsurface(big_bomb_rect)
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
#6.1 m_enemy's surface
enemy_m_rect = pygame.Rect(0, 5, 68,90)
enemy_m_img = plane_img.subsurface(enemy_m_rect)
enemy_m_down_imgs = []
enemy_m_down_imgs.append(plane_img.subsurface(pygame.Rect(432, 530, 68, 90)))
enemy_m_down_imgs.append(plane_img.subsurface(pygame.Rect(535, 656, 68, 90)))
enemy_m_down_imgs.append(plane_img.subsurface(pygame.Rect(604, 656, 68, 90)))
enemy_m_down_imgs.append(plane_img.subsurface(pygame.Rect(672, 656, 68, 90)))
#6.2 l_enemy's surface

enemy_l_rect = pygame.Rect(338, 753,  165, 246)
enemy_l_img = plane_img.subsurface(enemy_l_rect)

enemy_l_imgs = []
enemy_l_imgs.append(plane_img.subsurface(pygame.Rect(338, 753, 165, 245)))
enemy_l_imgs.append(plane_img.subsurface(pygame.Rect(505, 753, 165, 246)))
enemy_l_down_imgs = []
enemy_l_down_imgs.append(plane_img.subsurface(pygame.Rect(165, 753, 165, 245)))
enemy_l_down_imgs.append(plane_img.subsurface(pygame.Rect(5, 490, 165, 245)))
enemy_l_down_imgs.append(plane_img.subsurface(pygame.Rect(5, 228, 165, 245)))
enemy_l_down_imgs.append(plane_img.subsurface(pygame.Rect(840, 753, 165, 246)))
enemy_l_down_imgs.append(plane_img.subsurface(pygame.Rect(167, 490,  165, 246)))
enemy_l_down_imgs.append(plane_img.subsurface(pygame.Rect(677, 753, 165, 246)))


enemies = pygame.sprite.Group()
enemies_m = pygame.sprite.Group()
enemies_l = pygame.sprite.Group()
#use for describe the crash.
enemies_down = pygame.sprite.Group()
enemies_m_down = pygame.sprite.Group()
enemies_l_down = pygame.sprite.Group()

bombs = pygame.sprite.Group()
big_bombs = pygame.sprite.Group()


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
	#screen.blit(bomb_img, (100,100))
	screen.blit(welcome_img, (0, 0))

	#screen.blit(enemy_l_img, (300, 10))

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


	#creat the enemy
	if enemy_frequency %30 ==0:
 		enemy_pos =  [random.randint(0,SCREEN_WIDTH - enemy_rect.width), 0]
 		enemy = Enemy(enemy_img, enemy_down_imgs, enemy_pos)
 		enemies.add(enemy)  #add the enemy to the enemys
 		if level>2:
 			if random.randint(-1,3):
 				enemy_m_pos = [random.randint(0,SCREEN_WIDTH - enemy_m_rect.width), 0]
 				enemy_m = Enemy_m(enemy_m_img, enemy_m_down_imgs, enemy_m_pos)
 				enemies_m.add(enemy_m)   #creat the middle scale enemy
 		if level>4:
 			if not random.randint(-1,8):
 				enemy_l_pos = [random.randint(0,SCREEN_WIDTH - enemy_l_rect.width), 0]
 				enemy_l = Enemy_l(enemy_l_img, enemy_l_down_imgs, enemy_l_pos)
 				enemies_l.add(enemy_l)   				
 	enemy_frequency+=1

 	if enemy_frequency>30:
 		enemy_frequency = 1
 	#draw the bomb
 	if bomb_frequence %500 == 0:
 		#add the bomb to the bombs
 		if not random.randint(-1,1):   							#creat the big_bomb by random
 			big_bomb_pos = [random.randint(30, SCREEN_WIDTH - 100), 0]
 			big_bomb_1 = Big_bomb(big_bomb_img, big_bomb_pos)
 			big_bombs.add(big_bomb_1) 
 		else:
 			bomb_pos =  [random.randint(30, SCREEN_WIDTH - 100), 0]
 			bomb_1 = Bomb(bomb_img, bomb_pos)
 			bombs.add(bomb_1)  		
 	bomb_frequence+=1
 	if bomb_frequence >= 600:
 		bomb_frequence = 1
 	for bomb in bombs:
 		bomb.move()
 		if pygame.sprite.collide_circle(bomb, player):
 			bombs.remove(bomb)
 			get_double.play()	
 			if player.equ<3:
 				player.equ += 1
 		if bomb.rect.top > SCREEN_HEIGHT:
 			bombs.remove(bomb)
 	for big_bomb in big_bombs:
 		big_bomb.move()
 		if pygame.sprite.collide_circle(big_bomb,player):
 			big_bombs.remove(big_bomb)
 			get_bomb.play()
 			if player.Big_bomb<2:
 				player.Big_bomb +=1
 		if big_bomb.rect.top> SCREEN_HEIGHT:
 			big_bombs.remove(Big_bomb)
 	#delete the bullet if it has go out the screen
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
 	#manipulate the enemy_m 
 	for enemy1 in enemies_m:
 		enemy1.move()
 		if pygame.sprite.collide_circle(enemy1, player):
 			enemies_m_down.add(enemy1)
 			enemies_m.remove(enemy1)	
 			player.is_attacked = True
 			gameover_sound.play()
 			break
 		if enemy1.rect.top > SCREEN_HEIGHT:
 			enemies_m.remove(enemy1)
 	# add the crash enemy_m into the set of enemy_m_down
 	enemies1_m_down = pygame.sprite.groupcollide(enemies_m, player.bullets, 0, 1)
 	for enemy_m_down in enemies1_m_down:
 		if enemy_m_down.life == 0:
 			enemies_m.remove(enemy_m_down)
 			enemies_m_down.add(enemy_m_down)
 		else:
 			enemy_m_down.life -= 1

 	#manipulate the enemy_l 
 	for enemy1 in enemies_l:
 		enemy1.move()
 		if pygame.sprite.collide_circle(enemy1, player):
 			enemies_l_down.add(enemy1)
 			enemies_l.remove(enemy1)	
 			player.is_attacked = True
 			gameover_sound.play()
 			break
 		if enemy1.rect.top > SCREEN_HEIGHT:
 			enemies_l.remove(enemy1)
 	enemies1_l_down = pygame.sprite.groupcollide(enemies_l, player.bullets, 0, 1)
 	for enemy_l_down in enemies1_l_down:
 		if enemy_l_down.life == 0:
 			enemies_l.remove(enemy_l_down)
 			enemies_l_down.add(enemy_l_down)
 		else:
 			enemy_l_down.life -= 1
	
	#draw the backgroud

 	screen.fill(0)
 	screen.blit(background, (0, 0))
 	#____________________________________________draw anything below this_____________________________
 	#change the win flag
 
 	if score >= final_score:
 		win = 1
 		running = 0 
 	#draw the player's plane
 	if not player.is_attacked:
 		screen.blit(player.image[player.img_index], player.rect)
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
 	#middle scale	
 	for enemy_m_down in enemies_m_down:
 		if enemy_m_down.down_index == 0:
 			enemy_down_sound.play()
 		if enemy_m_down.down_index > 7:
 			enemies_m_down.remove(enemy_m_down)
 			score += 400
 			continue
 		screen.blit(enemy_m_down.down_imgs[enemy_m_down.down_index / 2], enemy_m_down.rect)
 		enemy_m_down.down_index += 1

 	#large scale	
 	for enemy_l_down in enemies_l_down:
 		if enemy_l_down.down_index == 0:
 			enemy_down_sound.play()
 		if enemy_l_down.down_index > 7:
 			enemies_l_down.remove(enemy_l_down)
 			score += 1000
 			continue
 		screen.blit(enemy_l_down.down_imgs[enemy_l_down.down_index / 2], enemy_l_down.rect)
 		enemy_l_down.down_index += 1
 	#draw the bombs and big_bombs
 	for bomb in bombs:
 		screen.blit(bomb.image, bomb.rect.midbottom)
 	for big_bomb in big_bombs:
 		screen.blit(big_bomb.image, big_bomb.rect.midbottom)
 	#draw the bullet and enmeies
 	player.bullets.draw(screen)
 	enemies.draw(screen)
 	enemies_m.draw(screen)
 	enemies_l.draw(screen)

 	#show the score
 	font = pygame.font.Font(None, 36)
 	score_text = font.render("Score:" + str(score) , True, (128, 128, 128))
 	text_rect = score_text.get_rect()
 	text_rect.topleft = [10, 10]
 	screen.blit(score_text, text_rect)

 	level_text =font.render("Level:"+str(level+1), True, (128, 128, 128))
 	text_rect = score_text.get_rect()
 	text_rect.topleft = [350, 10]
 	screen.blit(level_text, text_rect)

 	bomb_text = font.render("bombs:"+str(player.Big_bomb), True, (128, 128, 128))
 	text_rect = bomb_text.get_rect()
 	text_rect.topleft = [230, 10]
 	screen.blit(bomb_text, text_rect)
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
 		if key[K_j]:
	 		if shoot_frequency >= 6:
	 			bullet_sound.play()
	 			player.shoot(bullet_img)
	 			screen.blit(player.image[1], player.rect)#there are some problems right here.
	 			shoot_frequency = 0
	 	shoot_frequency+=1
	 	if shoot_frequency>11:
	 		shoot_frequency = 0
	 	#screen.blit(player.image[0], player.rect)
 		if key[K_k]:
 			if bomb_freze >= 10:
 				if player.Big_bomb:
 					player.destroy()
 					use_bomb.play()
 					bomb_freze = 0
 					#destroy all small enemies
 					for enemy in enemies:
	 					enemies_down.add(enemy)
 						enemies.remove(enemy)
 					for enemy_m in enemies_m:
 						enemy_m.life-=1
 						if enemy_m.life == 0:
 							enemies_m_down.add(enemy_m)
 							enemies_m.remove(enemy_m)
 					for enemy_l in enemies_l:
 						enemy_l.life-=1
 						if enemy_l.life == 0:
 							enemies_l_down.add(enemy_l)
 							enemies_l.remove(enemy_l)
 						
 		bomb_freze+=1
 		if bomb_freze > 19:
 			bomb_freze = 0
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