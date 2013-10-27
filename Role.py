# -*- coding: utf-8 -*-
"make the class of the Role"

import pygame
import random
import math
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

TYPE_S = 1
TYPE_M = 2
TYPE_B = 3

class Bullet(pygame.sprite.Sprite):
	def __init__(self, bullet_img, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.midbottom = init_pos
		self.speed = 10
	def move(self):
		self.rect.top -= self.speed
class Player(pygame.sprite.Sprite):

	def __init__(self, plane_img, player_rect, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = [] 							#init the images of player.
		for i in xrange(len(player_rect)):
			self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())  
		self.rect = player_rect[0]			#init the the rect of images
		self.rect.topleft = init_pos		
		self.speed = 8
		self.bullets = pygame.sprite.Group()  #the bullets of player.
		self.img_index = 0
		self.is_attacked = False			#check the status of the player.
		self.equ = 1
		self.Big_bomb = 0
	def shoot(self, bullet_img):
		bullet_width = 20
		if self.equ == 1:	
			bullet = Bullet(bullet_img,	(self.rect.midtop[0], self.rect.midtop[1]))
			self.bullets.add(bullet)
		elif self.equ == 2:
			bullet = Bullet(bullet_img,	(self.rect.midtop[0] - bullet_width/2, self.rect.midtop[1]))
			self.bullets.add(bullet)
			bullet = Bullet(bullet_img,	(self.rect.midtop[0] + bullet_width/2, self.rect.midtop[1]))
			self.bullets.add(bullet)
		elif self.equ == 3:
			bullet = Bullet(bullet_img,	(self.rect.midtop[0] - bullet_width, self.rect.midtop[1]))
			self.bullets.add(bullet)
			bullet = Bullet(bullet_img,	(self.rect.midtop[0], self.rect.midtop[1]))
			self.bullets.add(bullet)
			bullet = Bullet(bullet_img,	(self.rect.midtop[0] + bullet_width, self.rect.midtop[1]))
			self.bullets.add(bullet)
	def destroy(self):
		self.Big_bomb -= 1 

	def moveup(self):
		if self.rect.top <=0:
			self.rect.top = 0
		else:
			self.rect.top -= self.speed
	def movedown(self):
		if self.rect.top >=SCREEN_HEIGHT - self.rect.height:
			self.rect.top = SCREEN_HEIGHT -self.rect.height
		else:
			self.rect.top +=self.speed
	def moveleft(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		else:
			self.rect.left -= self.speed
	def moveright(self):
		if self.rect.left >=SCREEN_WIDTH - self.rect.width:
			self.rect.left = SCREEN_WIDTH -self.rect.width
		else:
			self.rect.right += self.speed
class Enemy(pygame.sprite.Sprite):
	def __init__(self, enemy_img, enemy_down_imgs, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_img
		self.rect = self.image.get_rect()
		self.rect.topleft = init_pos
		self.down_imgs = enemy_down_imgs
		self.speed = 3
		self.down_index = 0
	def move(self):
		self.rect.top += self.speed
class Bomb(pygame.sprite.Sprite):
	def __init__(self, bomb_img, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = bomb_img
		self.rect = self.image.get_rect()
		self.rect.midbottom = init_pos
		self.speed = 3
	def move(self):
		self.rect.top += self.speed
		self.rect.left += self.speed/4*random.randint(-3,  +3)
class Big_bomb(pygame.sprite.Sprite):
	def __init__(self, Big_bomb_img, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = Big_bomb_img
		self.rect = self.image.get_rect()
		self.rect.midbottom = init_pos
		self.speed = 3
	def move(self):
		self.rect.top += self.speed
		self.rect.left += self.speed/4*random.randint(-3,  +3)
class Enemy_m(pygame.sprite.Sprite):
	def __init__(self, enemy_m_img, enemy_m_down_imgs, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_m_img
		self.rect = self.image.get_rect()
		self.rect.topleft = init_pos
		self.down_imgs = enemy_m_down_imgs
		self.speed = 4
		self.down_index = 0
		self.life = 2
	def move(self):
		angle = 0                     #random.randint(30,60)
		velx = self.speed*math.cos(angle)
		vely = self.speed*math.sin(angle)
		self.rect.top  +=  velx
		self.rect.left += vely
class Enemy_l(pygame.sprite.Sprite):
	def __init__(self, enemy_l_img, enemy_l_down_imgs,init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_l_img
		self.rect = self.image.get_rect()
		self.rect.topleft = init_pos
		self.down_imgs = enemy_l_down_imgs
		self.speed = 1
		self.down_index = 0
		self.life = 10
	def move(self):
		angle = 0#random.randint(30,60)
		velx = self.speed*math.cos(angle)
		vely = self.speed*math.sin(angle)
		self.rect.top  +=  velx
		self.rect.left += vely