import pygame
from pygame.locals import*
import time
import random
size=40

class Snake:
    def __init__(self,screen):
        self.screen=screen
        self.block=pygame.image.load('block.jpg')
        self.length=1
        self.x=[400]
        self.y=[300]
        self.direction='left'


    def move_left(self):
        self.direction='left'
    def move_right(self):
       self.direction='right'
    def move_up(self):
        self.direction='up'
    def  move_down(self):
        self.direction='down'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        
        if self.direction=='left':
            self.x[0]-=size
        if self.direction=='right':
            self.x[0]+=size
        if self.direction=='up':
            self.y[0]-=size
        if self.direction=='down':
            self.y[0]+=size
        self.draw()    
        
    def draw(self):
        for i in range(self.length):
            self.screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)


class Apple:
    def __init__(self,screen):
        self.screen=screen
        self.img=pygame.image.load('apple.jpg')
        self.x=120
        self.y=120
    def draw(self):
        self.screen.blit(self.img,(self.x,self.y))
        pygame.display.flip()

    def  move(self):
        self.x=random.randint(1,15)*size
        self.y=random.randint(1,15)*size
        


class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((800,700),RESIZABLE)
        pygame.display.set_caption('Snake and Apple Game')
        self.running=True
        self.snake=Snake(self.screen)
        self.apple=Apple(self.screen)
        self.snake.draw()
        self.apple.draw()
        self.pause=False
        self.play_background_music()

    def render_background(self):
        bg=pygame.image.load('background.jpg')
        self.screen.blit(bg,(0,0))

    def reset(self):
        self.snake=Snake(self.screen)
        self.apple=Apple(self.screen)

    def play_background_music(self):
        pygame.mixer.music.load('bg_music_1.mp3')
        pygame.mixer.music.play(-1,0)

    def  play_sound(self,sound_name):
        if sound_name=='crash':
            sound=pygame.mixer.Sound("crash.mp3")
        elif sound_name=='ding':
            sound=pygame.mixer.Sound('ding.mp3')
        pygame.mixer.Sound.play(sound)    
    
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
   
        pygame.display.flip()

        if self.wall_collision(self.snake.x[0],self.snake.y[0]):
            self.play_sound('crash')
            raise Exception('collision occured')

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.display_score()
            self.apple.move()
            return
        for i in range(1,self.snake.length):
            self.play_sound('crash')
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                raise Exception('collision occured')

    def  is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def wall_collision(self, x, y):
    # Check if the snake hits the boundaries of the game screen
        if x < 0 or x >= 800 or y < 0 or y >= 700:
            return True
        return False
    
    def  display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f'Score:{self.snake.length}',True,'red')
        self.screen.blit(score,(500,100))

    def show_game_over(self):
        self.render_background()
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f'Game is over!Your score is {self.snake.length}',True,('green'))
        self.screen.blit(line1,(200,300))
        line2=font.render('to play again press enter!',True,'green')
        self.screen.blit(line2,(200,500))
        pygame.mixer.music.pause()
        pygame.display.flip()

    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        self.running==False
                    if  event.key==K_RETURN:
                        pygame.mixer.music.unpause()
                        self.pause=False
                        
                
                    if not self.pause:
                        
                        if event.key==K_RIGHT:
                            self.snake.move_right()
                        if event.key==K_LEFT:
                            self.snake.move_left()
                        if event.key==K_UP:
                            self.snake.move_up()
                        if event.key==K_DOWN:
                            self.snake.move_down()

            try:
                if  not self.pause:
                    self.play()
                          
            except Exception as e:
                print(e)
                self.show_game_over()
                self.pause=True
                self.reset()
            time.sleep(0.25)


if __name__=='__main__':
    game=Game()
    game.run()
                                

            
        
