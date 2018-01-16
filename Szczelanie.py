import arcade
import random

arcade.pyglet.font.add_file('Walk-Around-the-Block.ttf')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ALIEN_BULLET_SPEED = 6
BULLET_SPEED = 12
ALIEN_SPEED = 1

BEST_SCORE=0
BLUE = (140,200,245)
MENU = 0
GAME_RUNNING = 1
GAME_OVER = 2
GAME_WON = 3

class BulletPlayer(arcade.Sprite):
    def update(self):
        self.center_y += BULLET_SPEED

class BulletAlien(arcade.Sprite):
    def update(self):
        self.center_y -= ALIEN_BULLET_SPEED

class GameWindow(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Szczelanie")
        
        self.all_sprites_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.alien_bullet_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()
        self.mouse = [0,0]
        self.current_state = MENU
        self.level = 4
        self.HP = 100
        self.life = 3
        self.score = 0
        self.player_sprite = arcade.Sprite("images/SpaceShip.png", 0.2)
        self.player_sprite.speedr = 0
        self.player_sprite.speedl = 0
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 70
        self.all_sprites_list.append(self.player_sprite)
        self.Tut=1
        
        self.menu_background = arcade.Sprite("images/background2.jpg")
        self.menu_background.center_x=400
        self.menu_background.center_y=300
        self.background = arcade.Sprite("images/background1.png")
        self.background.center_x=400
        self.background.center_y=300

        self.sound_player = arcade.pyglet.media.Player()
        self.menu_sound = arcade.sound.load_sound("sounds/Metaruka.mp3")
        self.gun_sound = arcade.sound.load_sound("sounds/laser6.mp3")
        self.kill_sound = arcade.sound.load_sound("sounds/phaseJump5.mp3")
        self.dead_sound = arcade.sound.load_sound("sounds/highDown.mp3")
        self.levelup_sound = arcade.sound.load_sound("sounds/powerUp5.mp3")
        for i in range(5):
            self.sound_player.queue(self.menu_sound)
        self.sound_player.play()
        self.tut_mess="Use:\nRIGHT ARROW to go right\nLEFT ARROW to go left\nSPACE to shoot"
        
    def on_draw(self):

        arcade.start_render()

        if self.current_state == GAME_RUNNING:
            self.background.draw()
            self.draw_game()

        elif self.current_state == GAME_OVER:
            self.menu_background.draw()
            self.draw_game_over()
        
        elif self.current_state == GAME_WON:
            self.menu_background.draw()
            self.draw_game_won()
            
        else:
            self.menu_background.draw()
            self.draw_menu()
    
    def draw_game(self):
        if self.sound_player.volume > 0.1:
            self.sound_player.volume -= 0.03
        if(self.Tut==0):
            arcade.draw_text(self.tut_mess, 150, 275, arcade.color.WHITE, 25, font_name='Walk Around the Block')
        if(self.Tut==0 and len(self.alien_list) == 0):
            self.Tut += 1
            self.current_state = MENU
            
        elif(self.level == 0 and len(self.alien_list) == 0):
            for i in range(len(self.block_list)):
                self.block_list[0].kill()
            self.score = 0
            self.level += 1
            self.Level1()
            
        elif(self.level == 1 and len(self.alien_list) == 0):
            for i in range(len(self.block_list)):
                self.block_list[0].kill()
            arcade.play_sound(self.levelup_sound)
            self.level += 1
            self.Level2()
            
        elif(self.level == 2 and len(self.alien_list) == 0):
            for i in range(len(self.block_list)):
                self.block_list[0].kill()
            arcade.play_sound(self.levelup_sound)
            self.level += 1
            self.Level3()
            
        elif(self.level == 3 and len(self.alien_list) == 0):
            for i in range(len(self.block_list)):
                self.block_list[0].kill()
            global ALIEN_SPEED
            ALIEN_SPEED *= 2
            arcade.play_sound(self.levelup_sound)
            self.level += 1
            self.Level4()
            
        elif(self.level == 4 and len(self.alien_list) == 0):
            arcade.play_sound(self.levelup_sound)
            self.level +=1
            self.Boss()
            
        elif(self.level == 5 and len(self.alien_list) == 0):
            self.score += 100*self.life
            
            high_score_file = open("best.txt","r")
            global BEST_SCORE
            BEST_SCORE=int(high_score_file.read())
            high_score_file.close()
            if(self.score>BEST_SCORE):
                high_score_file = open("best.txt","w")
                high_score_file.write(str(self.score))
                BEST_SCORE=self.score
                high_score_file.close()
                    
            for i in range(len(self.block_list)):
                self.block_list[0].kill()
            self.current_state = GAME_WON
            
        self.all_sprites_list.draw()
        output = "Aliens Left: {}".format(len(self.alien_list))
        arcade.draw_text(output, 10, 580, arcade.color.WHITE, 20,font_name='Walk Around the Block')
        output = "Points: {}".format(self.score)
        arcade.draw_text(output, 10, 10, arcade.color.WHITE, 25,font_name='Walk Around the Block')
        output = "Lifes: {}".format(self.life)
        arcade.draw_text(output, 330, 10, arcade.color.WHITE, 25,font_name='Walk Around the Block')
        output = "HP: {}".format(self.HP)
        arcade.draw_text(output, 650, 10, arcade.color.WHITE, 25,font_name='Walk Around the Block')
        if(self.player_sprite.center_x<800):
            self.player_sprite.center_x += self.player_sprite.speedr
        if(self.player_sprite.center_x>0):
            self.player_sprite.center_x += self.player_sprite.speedl
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.speedl = -5
        elif key == arcade.key.RIGHT:
            self.player_sprite.speedr = 5
        if key == arcade.key.SPACE:
            bullet = BulletPlayer("images/laser1.png",0.6)
            bullet.angle = 90
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            self.all_sprites_list.append(bullet)
            self.bullet_list.append(bullet)
            arcade.play_sound(self.gun_sound)
        if self.Tut==0:
            self.tut_mess="Eliminate all aliens"
            
    def on_key_release(self,key,modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.speedl = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.speedr = 0        
    
    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.current_state == GAME_OVER or self.current_state == GAME_WON:
            
            if x>230 and x<670 and y<230 and y>190:
                self.level = 0
                self.life = 3
                self.HP = 100
                self.score = 0
                global ALIEN_SPEED
                ALIEN_SPEED = 1
                self.current_state = GAME_RUNNING
                self.draw_game()
            
            elif x>370 and x<470 and y<155 and y>115:
                self.sound_player.pause()
                self.close()
            
        elif self.current_state == MENU:
            
            if x>290 and x<520 and y<310 and y>265:
                self.current_state = GAME_RUNNING
                self.draw_game()
                
            elif x>300 and x<490 and y<230 and y>190:
                self.Tut=0
                self.current_state = GAME_RUNNING
                self.Tutorial()
                
            elif x>350 and x<450 and y<160 and y>120:
                self.sound_player.pause()
                self.close()
                
    def on_mouse_motion(self, x, y, dx, dy):
        
        self.mouse = [x,y]
        
    def draw_game_won(self):
        
        if self.sound_player.volume < 1:
            self.sound_player.volume += 0.005
            
        high_score_file = open("best.txt","r")
        global BEST_SCORE
        BEST_SCORE=int(high_score_file.read())
        high_score_file.close()
        
        output = "You Win!"
        arcade.draw_text(output, 240, 420, arcade.color.WHITE, 54, font_name='Walk Around the Block')

        output = "Your score:"+str(self.score)
        arcade.draw_text(output, 280, 325, arcade.color.WHITE, 24, font_name='Walk Around the Block')
        
        output = "Best score:"+str(BEST_SCORE)
        arcade.draw_text(output, 280, 275, arcade.color.WHITE, 24, font_name='Walk Around the Block')
        
        output = "Play again"
        arcade.draw_text(output, 290, 200, arcade.color.WHITE, 30, font_name='Walk Around the Block')
    
        output = "Quit"
        arcade.draw_text(output, 360, 125, arcade.color.WHITE, 30, font_name='Walk Around the Block')
        
        if self.mouse[0]>290 and self.mouse[0]<530 and self.mouse[1]<230 and self.mouse[1]>190:
            output = "Play again"
            arcade.draw_text(output, 290, 200, BLUE, 30, font_name='Walk Around the Block')
            
        if self.mouse[0]>360 and self.mouse[0]<460 and self.mouse[1]<155 and self.mouse[1]>115:
            output = "Quit"
            arcade.draw_text(output, 360, 125, BLUE, 30, font_name='Walk Around the Block')

    def draw_game_over(self):
        
        if self.sound_player.volume < 1:
            self.sound_player.volume += 0.005
            
        high_score_file = open("best.txt","r")
        global BEST_SCORE
        BEST_SCORE=int(high_score_file.read())
        high_score_file.close()
        if(self.score>BEST_SCORE):
            high_score_file = open("best.txt","w")
            high_score_file.write(str(self.score))
            BEST_SCORE=self.score
            high_score_file.close()
        
        output = "Game Over"
        arcade.draw_text(output, 190, 420, arcade.color.WHITE, 54, font_name='Walk Around the Block')

        output = "Your score:"+str(self.score)
        arcade.draw_text(output, 300, 325, arcade.color.WHITE, 24, font_name='Walk Around the Block')
        
        output = "Best score:"+str(BEST_SCORE)
        arcade.draw_text(output, 300, 275, arcade.color.WHITE, 24, font_name='Walk Around the Block')
        
        output = "Click to restart"
        arcade.draw_text(output, 230, 200, arcade.color.WHITE, 30, font_name='Walk Around the Block')
    
        output = "Quit"
        arcade.draw_text(output, 370, 125, arcade.color.WHITE, 30, font_name='Walk Around the Block')
        
        if self.mouse[0]>230 and self.mouse[0]<670 and self.mouse[1]<230 and self.mouse[1]>190:
            output = "Click to restart"
            arcade.draw_text(output, 230, 200, BLUE, 30, font_name='Walk Around the Block')
            
        if self.mouse[0]>350 and self.mouse[0]<450 and self.mouse[1]<155 and self.mouse[1]>115:
            output = "Quit"
            arcade.draw_text(output, 370, 125, BLUE, 30, font_name='Walk Around the Block')
       
        
    def draw_menu(self):
        
        output = "Szczelanie"
        arcade.draw_text(output, 180, 400, arcade.color.WHITE, 54, font_name='Walk Around the Block')
        
        if self.sound_player.volume < 1:
            self.sound_player.volume += 0.005
        
        if self.mouse[0]>290 and self.mouse[0]<520 and self.mouse[1]<310 and self.mouse[1]>265:
            output = "Play Game"
            arcade.draw_text(output, 290, 275, BLUE, 30, font_name='Walk Around the Block')
        else:
            output = "Play Game"
            arcade.draw_text(output, 290, 275, arcade.color.WHITE, 30, font_name='Walk Around the Block')
        
        if self.mouse[0]>300 and self.mouse[0]<490 and self.mouse[1]<230 and self.mouse[1]>190:
            output = "Tutorial"
            arcade.draw_text(output, 300, 200, BLUE, 30, font_name='Walk Around the Block')
        else:
            output = "Tutorial"
            arcade.draw_text(output, 300, 200, arcade.color.WHITE, 30, font_name='Walk Around the Block')
        if self.mouse[0]>350 and self.mouse[0]<450 and self.mouse[1]<160 and self.mouse[1]>120:
            output = "Quit"
            arcade.draw_text(output, 350, 125, BLUE, 30, font_name='Walk Around the Block')
        else:
            output = "Quit"
            arcade.draw_text(output, 350, 125, arcade.color.WHITE, 30, font_name='Walk Around the Block')
        
        
    def animate(self, delta_time):

        self.all_sprites_list.update()

        for bullet in self.bullet_list:

            hit_list = arcade.check_for_collision_with_list(bullet, self.alien_list)

            if len(hit_list) > 0:
                bullet.kill()

            for alien in hit_list:
                alien.life -= 1
                if(alien.life==0):
                    alien.kill()
                    arcade.play_sound(self.kill_sound)
                self.score += 1

            if bullet.top > SCREEN_HEIGHT-25:
                bullet.kill()
         
        for bullet in self.alien_bullet_list:

            hit = arcade.check_for_collision(bullet, self.player_sprite)
            if hit:
                bullet.kill()
                self.HP -= 20

            if bullet.bottom < 30:
                bullet.kill()
                
                
        for bulleta in self.alien_bullet_list:
            
            for bullet in self.bullet_list:
                hit = arcade.check_for_collision(bulleta, bullet)
                if hit:
                    bullet.kill()
                    bulleta.kill()
        
        for block in self.block_list:
            for bullet in self.bullet_list:
                hit = arcade.check_for_collision(block, bullet)
                if hit:
                    bullet.kill()
                    block.kill()
            for bullet in self.alien_bullet_list:
                hit = arcade.check_for_collision(block, bullet)
                if hit:
                    bullet.kill()
                    block.kill()
            for alien in self.alien_list:
                hit = arcade.check_for_collision(block, alien)
                if hit:
                    block.kill()
                    
        if (self.alien_list and self.level!=0):
            if self.level!=5:
                for alien in self.alien_list:
                    x=random.randrange(1300-200*self.level)
                    if(x==100):
                        bullet = BulletAlien("images/laser2.png",0.6)
                        bullet.angle = 270
                        bullet.center_x = alien.center_x
                        bullet.bottom = alien.bottom
                        self.all_sprites_list.append(bullet)
                        self.alien_bullet_list.append(bullet)
                alienl=self.alien_list[0]
                alienr=self.alien_list[0]
                for alien in self.alien_list:
                    if alien.center_x<alienl.center_x:
                        alienl=alien
                    elif alien.center_x>alienr.center_x:
                        alienr=alien
            
                global ALIEN_SPEED
                if alienl.center_x<=0:
                    ALIEN_SPEED=-ALIEN_SPEED
                    for alien in self.alien_list:
                        alien.center_y-=50
                        alien.center_x+=ALIEN_SPEED
                elif alienr.center_x>=800:
                    ALIEN_SPEED=-ALIEN_SPEED
                    for alien in self.alien_list:
                        alien.center_y-=50
                        alien.center_x+=ALIEN_SPEED
                else:
                    for alien in self.alien_list:
                        alien.center_x+=ALIEN_SPEED
        
            else:
                boss=self.alien_list[0]
                speed = 0
                x=random.randrange(15)
                if(x==10):
                    bullet = BulletAlien("images/laser3.png",0.6)
                    bullet.angle = 270
                    bullet.center_x = boss.center_x
                    bullet.bottom = boss.bottom
                    self.all_sprites_list.append(bullet)
                    self.alien_bullet_list.append(bullet)
                if boss.center_x-2>self.player_sprite.center_x:
                    speed=-2
                    boss.center_x+=speed
                elif boss.center_x+2<self.player_sprite.center_x:
                    speed=2
                    boss.center_x+=speed
                else:
                    speed=0 
                        
            last=len(self.alien_list)
            if (self.alien_list[last-1].center_y<=100 or self.HP==0) and self.level!=5:
                global BEST_SCORE
                self.life -= 1
                if(self.score>BEST_SCORE):
                    BEST_SCORE=self.score
                for i in range(last):
                    self.alien_list[0].kill()
                for i in range(len(self.block_list)):
                    self.block_list[0].kill()
                if(self.life<=0):
                    self.current_state = GAME_OVER
                elif(self.level==1):
                    arcade.play_sound(self.dead_sound)
                    self.HP=100
                    self.Level1()
                elif(self.level==2):
                    arcade.play_sound(self.dead_sound)
                    self.HP=100
                    self.Level2()
                elif(self.level==3):
                    arcade.play_sound(self.dead_sound)
                    self.HP=100
                    self.Level3()
                elif(self.level==4):
                    arcade.play_sound(self.dead_sound)
                    self.HP=100
                    self.Level4()
            elif self.level == 5 and self.HP == 0:
                self.life -= 1
                if(self.score>BEST_SCORE):
                    BEST_SCORE=self.score
                if(self.life<=0):
                    self.alien_list[0].kill()
                    for i in range(len(self.block_list)):
                        self.block_list[0].kill()
                    self.current_state = GAME_OVER
                else:
                    arcade.play_sound(self.dead_sound)
                    self.HP=100
    
    def Boss(self):
        boss=arcade.Sprite("images/BOSS.png",0.5)
        boss.center_x = 400
        boss.center_y = 400
        boss.life = 50
        self.all_sprites_list.append(boss)
        self.alien_list.append(boss)
                    
    def Block(self,x):
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_11.png",0.25)
        block.center_x = x-32
        block.center_y = 150
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_05.png",0.25)
        block.center_x = x-16
        block.center_y = 150
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_05.png",0.25)
        block.center_x = x
        block.center_y = 150
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_12.png",0.25)
        block.center_x = x+16
        block.center_y = 150
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_04.png",0.25)
        block.center_x = x-32
        block.center_y = 134
        block.angle = 90
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_06.png",0.25)
        block.center_x = x+16
        block.center_y = 134
        block.angle = 270
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_03.png",0.25)
        block.center_x = x-16
        block.center_y = 134
        block.angle = 270
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
        block = arcade.Sprite("images/Blue tiles/tileBlue_03.png",0.25)
        block.center_x = x
        block.center_y = 134
        block.angle = 270
        self.all_sprites_list.append(block)
        self.block_list.append(block)
        
    def Tutorial(self):   
        posy=SCREEN_HEIGHT-50
        posx=100
    
        for i in range(12):
            
            if(i%4 == 3 and ((i+1)/4)%2==0):
                continue
            alien = arcade.Sprite("images/shipGreen.png", 0.3)
            alien.life=1
            if(i%4 == 0 and i!=0):
                posy-=100
                posx=100
            if((i/4)%2==1 and i%4 == 0):
                posx=200
            alien.center_x = posx
            alien.center_y = posy
            posx +=200
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)

        self.Block(250)
        self.Block(550)
        
    def Level1(self):
        posy=SCREEN_HEIGHT-50
        posx=200
        for i in range(36):
            
            alien = arcade.Sprite("images/shipGreen.png", 0.3)
            alien.life=1
            if(i%9 == 0 and i!=0):
                posy-=50
                posx=200
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
            
        self.Block(200)
        self.Block(400)
        self.Block(600)
    
    def Level2(self):
        posy=SCREEN_HEIGHT-50
        posx=200
        for i in range(18):
            
            alien = arcade.Sprite("images/shipBeige.png", 0.35)
            alien.life=2
            if(i%9 == 0 and i!=0):
                posy-=50
                posx=200
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
            
        for i in range(18):
            
            alien = arcade.Sprite("images/shipGreen.png", 0.3)
            alien.life=1
            if(i%9 == 0):
                posy-=50
                posx=200
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
            
        self.Block(200)
        self.Block(400)
        self.Block(600)
            
    def Level3(self):
        
        posy=SCREEN_HEIGHT-50
        posx=200
        for i in range(9):
            
            alien = arcade.Sprite("images/shipBlue.png", 0.35)
            alien.life=3
            if(i%9 == 0 and i!=0):
                posy-=50
                posx=200
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
            
        for i in range(9):
            
            alien = arcade.Sprite("images/shipBeige.png", 0.35)
            alien.life=2
            if(i%9 == 0):
                posy-=50
                posx=200
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
        
        for i in range(18):
            
            alien = arcade.Sprite("images/shipGreen.png", 0.3)
            alien.life=1
            if(i%9 == 0):
                posy-=50
                posx=200
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
        
        self.Block(200)
        self.Block(400)
        self.Block(600)
        
    def Level4(self):
        
        posy=SCREEN_HEIGHT-50
        posx=230
        
        for i in range(8):
            
            alien = arcade.Sprite("images/shipBlue.png", 0.35)
            alien.life=3
            if(i%8 == 0 and i!=0):
                posy-=50
                posx=230
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
            
        for i in range(24):
            
            alien = arcade.Sprite("images/shipBeige.png", 0.35)
            alien.life=2
            if(i%8 == 0):
                posy-=50
                posx=230
            alien.center_x = posx
            alien.center_y = posy
            posx +=60
            self.all_sprites_list.append(alien)
            self.alien_list.append(alien)
        
        self.Block(160)
        self.Block(320)
        self.Block(480)
        self.Block(640)
            
def main():
    GameWindow()
    arcade.run()
main()