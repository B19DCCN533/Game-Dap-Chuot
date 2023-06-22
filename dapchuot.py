import pgzrun , pygame , math , random, time
WIDTH = 993 #set độ rộng khung game
HEIGHT = 477 #set độ dài của khung game

time_left = 60 #thời gian còn lại
score = 0 # điểm số
start_game = False 
game_over = False
show_credit = False
time_pass = 0 # thời gian đã trôi qua
number1=number2=number3=0

Pos_possible = [ #vị trí xuất hiện của chuột
    (140,33),
    (455,33),
    (775,33),
    (140,188),
    (455,188),
    (775,188),
    (140,348),
    (455,348),
    (775,348)
]

# set các biến
background = Actor("background")
enemy1 = Actor('mole1')
enemy1.pos = (-100,-100)
enemy2 = Actor('mole1')
enemy2.pos = (-100,-100)
enemy3 = Actor('mole3')
enemy3.pos = (-100,-100)
player = Actor('hammer0')
background_begin = Actor('begin')
start = Actor('start1')
background_credit = Actor('credit')
credit = Actor('credit1')
back = Actor('back1')
background_finish = Actor('finish')
play_again = Actor('playagain1')

def enemy1_reset():   # set up về con chuột 1
    global start_game, enemy1, time_pass, number1, number2, number3
    if start_game:
        enemy1 = Actor('mole1')
        number1 = random.randint(0,8)
        while(number1 == number2 or number1 == number3):
            number1 = random.randint(0,8)
        enemy1.pos = Pos_possible[number1] # thay đổi vị trí của chuột 1
clock.schedule_interval(enemy1_reset,(1.0-float(time_pass/60))) # lặp lại việc xuất hiện và độ trễ của chuột 

def enemy2_reset():   # set up về con chuột 2
    global start_game, enemy2, time_pass, number3, number2, number1
    if start_game:
        enemy2 = Actor('mole1')
        number2 = random.randint(0,8)
        while(number2 == number1 or number3 == number2):
            number2 = random.randint(0,8)
        enemy2.pos = Pos_possible[number2] # thay đổi vị trí của chuột 2
clock.schedule_interval(enemy2_reset,(1.0-float(time_pass/60))) # lặp lại việc xuất hiện và độ trễ của chuột 

def enemy3_reset():   # set up về con chuột 2
    global start_game, enemy3, number1, number2, number3, time_pass
    if start_game:
        enemy3=Actor('mole3')
        number3 = random.randint(0,8)
        while(number3 == number1 or number3 == number2):
            number3 = random.randint(0,8)
        enemy3.pos = Pos_possible[number3] # thay đổi vị trí của chuột 2
clock.schedule_interval(enemy3_reset,1.25-float(time_pass/60)) # lặp lại việc xuất hiện và độ trễ của chuột 

def enemy1_del(): 
    enemy1.pos=(-100,-100)

def enemy2_del():
    enemy2.pos=(-100,-100)

def enemy3_del():
    enemy3.pos=(-100,-100)

def hang_up():  # set up về hình ảnh búa
    player.image = 'hammer0'

def on_mouse_move(pos):  # sự thay đổi của các nút khi di chuyển chuột tới
    player.pos = (pos[0],pos[1]) 
    if start.collidepoint(pos):
        start.image = 'start2'
    else:
        start.image = 'start1'

    if credit.collidepoint(pos):
        credit.image = 'credit2'
    else:
        credit.image = 'credit1'

    if back.collidepoint(pos):
        back.image = 'back2'
    else:
        back.image = 'back1'

    if play_again.collidepoint(pos):
        play_again.image = 'playagain2'
    else:
        play_again.image = 'playagain1'

def on_mouse_down(pos): # set up hành động khi click chuột máy tính
    global score, show_credit , game_over , time_left , start_game , time_pass, vol
    player.image = 'hammer1' # hình ảnh gõ búa 
    clock.schedule_unique(hang_up, 0.1) # độ trễ nhấc búa

    if enemy1.collidepoint(pos):
        enemy1.image = 'mole2' # ảnh chuột 1 bị gõ
        score = score + 10 # điểm nhận được
        # âm thanh gõ
        sounds.hammering.play()
        sounds.hammering.set_volume(0.5)
        clock.schedule_unique(enemy1_del, 0.07)

    if enemy2.collidepoint(pos):
        enemy2.image = 'mole2' # ảnh chuột 2 bị gõ
        score = score + 10 # điểm nhận được
        # âm thanh gõ
        sounds.hammering.play()
        sounds.hammering.set_volume(0.5)
        clock.schedule_unique(enemy2_del, 0.07)

    if enemy3.collidepoint(pos):
        enemy3.image = 'mole4' # ảnh chuột 3 bị gõ
        if(score>0):
            score = score - 10 # điểm bị trừ
        # âm thanh gõ
        sounds.explosion.play()
        sounds.explosion.set_volume(0.5)
        clock.schedule_unique(enemy3_del, 0.07)

    if start.collidepoint(pos): # nếu ấn nút start 
        start_game = True
        show_credit = False
        game_over = False
        time_left = 60
        time_pass = 0
    
    if credit.collidepoint(pos): #nếu nhấn nút credit
        show_credit = True
        start_game = False
        game_over = False

    if back.collidepoint(pos):
        start_game = False
        show_credit = False
        game_over = False
        enemy1.pos = (-100,-100)
        enemy2.pos = (-100,-100)
        enemy3.pos = (-100,-100)

    if play_again.collidepoint(pos): # nếu nhấn nút playagain
        show_credit = False
        start_game = True
        game_over = False
        score = 0
        time_left = 60
        time_pass = 0
    

# bật nhạc nền
music.play('bgm')
music.set_volume(0.45)

def time_up():  # set up ve thoi gian tro choi
    global time_left , game_over , start_game , time_pass
    if start_game:
        if time_left:
            time_left = time_left - 1
            time_pass = time_pass + 1
            if time_left == 10:
                sounds.count_down.play()
        else:
            game_over = True
clock.schedule_interval(time_up,1.0)

def update(): #cập nhật vị trí các nút theo sự kiện
    #global select_x , select_y
    #mouse_x , mouse_y = pygame.mouse.get_pos()
    #select_x = math.floor(mouse_x) #lấy tọa độ x vị trí chuột
    #select_y = math.floor(mouse_y) #lấy tọa độ y vị trí chuột
    if game_over:
        play_again.pos = (332,388) 
    else:
        play_again.pos = (-100,-100)
    
    if game_over or show_credit:
        back.pos = (668,388)
    else:
        back.pos = (-100,-100)

    if start_game or show_credit:  
        start.pos = (-100,-100)
        credit.pos = (-100,-100)
    else:
        start.pos = (332,388)    
        credit.pos = (668,388)

def draw(): # hàm vẽ
    if not start_game and not show_credit and not game_over:
        background_begin.draw() # in nền start
        start.draw()
        credit.draw()
    if start_game:
        background.draw() #in nền
        enemy1.draw()      #in chuột
        if time_left <= 45:
            enemy2.draw()
        #screen.draw.text('toa do x: '+str(select_x) + 'toa do y: '+str(select_y)) #in tọa độ vị trí chuột
        screen.draw.text('Time : '+ str(time_left),(850,30), fontsize=30) # in thời gian
        screen.draw.text('Score : '+ str(score),(850,400), fontsize=30, color='yellow') # in điểm
        if time_left <= 30:
            enemy3.draw()
        player.draw()     #vẽ búa
    if show_credit:
        background_credit.draw()
        screen.draw.text('Made by Nhóm 17:',(280,150),fontname='svn-times new roman bold', fontsize=30)
        screen.draw.text('Lê Thành Long - B19DCCN391',(280,190),fontname='svn-times new roman bold', fontsize=30)
        screen.draw.text('Lê Đình Duy Anh - B19DCCN017',(280,230),fontname='svn-times new roman bold', fontsize=30)
        screen.draw.text('Trần Hồng Quân - B19DCCN533',(280,270),fontname='svn-times new roman bold', fontsize=30)
        back.draw()
    if game_over:
        background_finish.draw() # in nền kết thúc
        play_again.draw()        # in nút playagain
        back.draw()
        with open("highscore.txt", 'r') as f:
            try:
                highscore = int(f.read())
            except:
                highscore = 0
        if score < highscore:
            screen.draw.text('Your score : '+ str(score),(331,207), fontsize=60)
            screen.draw.text('Highscore: '+ str(highscore),(331,277),fontsize=60)
        else:
            screen.draw.text('New Highscore : '+ str(score),(331,207), fontsize=60)
            screen.draw.text('Highscore: '+ str(highscore),(331,277),fontsize=60)
            with open("highscore.txt", 'w') as f:
                f.write(str(score))
            highscore = score
    
pgzrun.go()