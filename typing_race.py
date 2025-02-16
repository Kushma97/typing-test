
import pygame
import random
import copy

pygame.init()

import nltk
nltk.download('words')
from nltk.corpus import words

wordlist = words.words()
len_indexes = []
length = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))

# Setting up the game window
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing test game")

timer = pygame.time.Clock()
fps = 60  

#Game variables
level = 1
activeString = ''
score = 0
file = open('highscore.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()

lives = 5
paused = True
word_objects = []
newLevel = True
# 2 letter, 3 letter, 4 letter, 5 letter, 6 letter, 7 and 8 
choices = [False, True, False, False, False, False, False]
letters = [] # letter a-z
for i in range(26):
  letter = chr(97 + i)  # chr converts ASCII to character
  letters.append(letter)
submit = ''


#Loading assets like fonts, sounds, music effects
footer_font= pygame.font.Font("fontsType/Square.ttf", 35) # Font("path", font_size)
pause_font = pygame.font.Font("fontsType/1up.ttf", 30)
banner_font = pygame.font.Font("fontsType/1up.ttf", 20)
font = pygame.font.Font("fontsType/AldotheApache.ttf", 40)

def generateLevel():
  word_objs = []
  include = []
  vertical_spacing = (HEIGHT-100)//level
  if True not in choices:
    choices[0] = True
  for i in range(len(choices)):
    if choices[i]:
      include.append((len_indexes[i],len_indexes[i+1]))
  for i in range(level):
    speed = random.randint(2, 3)
    y_pos = random.randint(10 + (i*vertical_spacing), (i+1)*vertical_spacing)
    x_pos = random.randint(WIDTH, WIDTH+800) #WIDTH + 800 is pizels Behind the screen
    index_select = random.choice(include)
    index = random.randint(index_select[0], index_select[1])
    text = wordlist[index].lower()
    newWord = Word(text, speed, y_pos, x_pos)
    word_objs.append(newWord)

  return word_objs

def drawPause():
  choice_commits = copy.deepcopy(choices)
  surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
  pygame.draw.rect(surface, (0,0,0,100), [80, 100, 510, 220], 0, 5) # 0 border-thickness, 5 is edge
  pygame.draw.rect(surface, (0,0,0,200), [80, 100, 510, 220], 5, 5)
  # Creating pause buttons menu from Button class
  resume_btn = Button(140, 180, surface, '>', False)
  resume_btn.drawCircles()
  quit_btn = Button(410, 180, surface, 'X', False)
  quit_btn.drawCircles()
  # defining options for pause menu
  surface.blit(footer_font.render('MENU', True, 'white'), (100, 110))
  surface.blit(footer_font.render('PLAY!', True, 'white'), (175, 160))
  surface.blit(footer_font.render('QUIT', True, 'white'), (440, 160))
  surface.blit(footer_font.render('ACTIVE LETTER LENGTH:', True, 'white'), (110, 215))
  # defining buttons for letter length selection
  for i in range(len(choices)):
    btn = Button(130+(i*70), 283, surface, str(i+2), False)
    btn.drawCircles()
    #Ensuring that the button won't osscilate going on and off when users hold there
    if btn.clicked:
      if choice_commits[i]:
        choice_commits[i] = False
      else:
        choice_commits[i] = True
    # Drwaing green radius around the active len of word
    if choices[i]:
      pygame.draw.circle(surface, 'green', (130+(i*70), 283), 25, 3)
  screen.blit(surface, (0,0))
  return resume_btn.clicked, choice_commits, quit_btn.clicked


def checkAnswer(scor):
  for wrd in word_objects:
    if wrd.text == submit:
      points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text)/3) #Just for fun our own maths for points
      scor += int(points) #removing decimals
      word_objects.remove(wrd)
     

  return scor

# Function to draw elements on the screen
def draw_screen():
  pygame.draw.rect(screen, (24, 55, 94), (0, HEIGHT - 70, WIDTH, 70), 0)  # Solid blue rectangle
  pygame.draw.rect(screen, 'white', (0, 0, WIDTH, HEIGHT), 5)  #Border around the screen
  pygame.draw.line(screen, 'white', (180, HEIGHT-70), (180, HEIGHT), 2) #Vertical line
  pygame.draw.line(screen, 'white', (550, HEIGHT-70), (550, HEIGHT), 2) # Another vertical line
  pygame.draw.line(screen, 'white', (0, HEIGHT-70), (WIDTH, HEIGHT-70), 2) #HOrizontal LiNE
  pygame.draw.rect(screen, 'black', (0, 0, WIDTH, HEIGHT), 2)  #Black rectangular Border 
# Text for showing the current level, player's current input, high scores, scores, lives, pause
  text = footer_font.render(f"Level:{level}", True, 'white')
  screen.blit(text, (10, HEIGHT-57))
  screen.blit(footer_font.render(f'"{activeString}"', True, 'white'), (200, HEIGHT-57))

  # making pause_button from Button class
  pauseBtn = Button(595, HEIGHT-37, screen, 'II', False) # these positioins are for the circle or button not II.
  pauseBtn.drawCircles()

  #We put the pause button now
  screen.blit(banner_font.render(f'Score:{score}', True, 'black'), (240, 12))
  screen.blit(banner_font.render(f'Best:{high_score}', True, 'black'), (480, 12))
  screen.blit(banner_font.render(f'Lives:{lives}', True, 'black'), (10, 12))

  return pauseBtn.clicked

def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('highscore.txt', 'w')
        file.write(str(int(high_score)))
        file.close()

class Word:
  def __init__(self, text, speed, y_pos, x_pos):
    self.text = text
    self.speed = speed
    self.y_pos = y_pos
    self.x_pos = x_pos
  def draw(self):
    color = 'black'
    screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
    active_len = len(activeString) #Length of activeString
    if activeString == self.text[:active_len]:
      screen.blit(font.render(activeString, True, 'green'),(self.x_pos, self.y_pos))
  def update(self):
    self.x_pos -= self.speed
    
class Button:
  def __init__(self, xPos, yPos, surf, text, clicked):
    self.xPos = xPos
    self.yPos = yPos
    self.surf = surf  #surface on which it is being drawn like screen, etc
    self.text = text
    self.clicked = clicked
  def drawCircles(self):
    cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.xPos, self.yPos), 24) # 35 is the radius of the circle
    if cir.collidepoint(pygame.mouse.get_pos()):
      butns =  pygame.mouse.get_pressed()
      if butns[0]: #If button is clicked not just hovered by mouse, changing the color
          pygame.draw.circle(self.surf, (190, 23, 44), (self.xPos, self.yPos), 24) 
          self.clicked = True
      else: #changing color when just hovered
        pygame.draw.circle(self.surf, (190, 89, 135), (self.xPos, self.yPos), 24) 

    pygame.draw.circle(self.surf, 'white', (self.xPos, self.yPos), 24, 3) # 3 is thickness not solid
    self.surf.blit(pause_font.render(self.text, True, 'white'), (self.xPos-12, self.yPos - 22)) #IT places II inside the circle at the right place
  
# Main loop
run = True
while run:
  # Fill the screen first before drawing anything else
  screen.fill((128, 128, 128))  # Gray background (RGB format)
  timer.tick(fps)

  # Draw background screen stuffs and status and get pause_btn status
  pauseBtn = draw_screen()
  if paused:
    resume_btn, changes, quit_btn = drawPause()
    if resume_btn:
      paused = False
    if quit_btn:
      #Checking high_score before leaving the game
      check_high_score()
      run = False
      print(f"Your highest score was {high_score}")

  if newLevel and not paused:
    word_objects = generateLevel()
    newLevel = False
  else:
    for w in word_objects:
      w.draw() #objects from Word class
      if not paused:
        w.update() #objects from Word class
      if w.x_pos < -200:
        word_objects.remove(w)
        lives -= 1
  if len(word_objects) <= 0 and not paused: #If it is empty
    level += 1
    newLevel = True
  if submit != '':
    init = score
    score = checkAnswer(score)
    submit = ''
    if init == score:
      #playing wrong entry sound
      pass

  # Handle events before drawing
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        #Checking high_score before leaving the game
        check_high_score()
        run = False
        print(f"Your highest score was {high_score}")
    if event.type == pygame.KEYDOWN: #KEYDOWN: Detects when a key is pressed
      if not paused: # Ensures the game is not paused
        if event.unicode.lower() in letters:  # Checks if the pressed key is a letter (a-z)
          activeString += event.unicode.lower() # Appends the letter to activeString

        if event.key == pygame.K_BACKSPACE and len(activeString)>0: #Checks backspace is pressed on non empty strings
          activeString = activeString[:-1] #removing the last index value
        # clicking enter button
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: # pygame.K_RETURN = Enter button
          submit = activeString
          activeString = ''
      # we can enter the ESC key to either come out of pause menu or show the pause menu
      if event.key == pygame.K_ESCAPE:
        if paused:
          paused = False
        else:
          paused = True
    #TO select other lengths after drawing the surface
    if event.type == pygame.MOUSEBUTTONUP and paused:
      if event.button == 1:
        choices = changes
  if pauseBtn:
    paused = True

  if lives < 0:
    #Restarting the game if out of lives from the surface menu
    paused = True
    level = 1
    lives = 5
    word_objects =[]
    newLevel = True
    check_high_score()
    score = 0
  # Draw the blue rectangle at the bottom
  draw_screen()

  # Update the display to show everything
  pygame.display.flip()

pygame.quit()
