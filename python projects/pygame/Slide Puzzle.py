import pygame, sys, random
from pygame.locals import *

# Create the constants
BOARDWIDTH = 4  # number of colums in the board
BOARDHEIGHT = 4  # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                      R    G    B
BLACK =             (  0,   0,   0)
WHITE =             (255, 255, 255)
BRIGHTBLUE =        (  0,  50, 255)
DARKTURQUOISE =     (  3,  54,  73)
GREEN =             (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDHEIGHT + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPSTIONS
    # 创建选项
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    # reset用于撤销玩家的各种操作
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    # new用于创建一个新的滑块谜题
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
    #solve用于为玩家破解谜题

    mainBoard, solutionSeq = generateNewPuzzle(80)
    # solutionSeq用于表示顺序正确的游戏板
    SOLVEDBOARD = getStartingBoard()
    allMoves = [] # 记录方块移动的步骤
    
    while True: # 主游戏循环
        slideTo = None # 记录玩家想要向哪一个方向移动贴片
        msg = ''   # 记录在窗口顶部显示什么字符串
        if mainBoard == SOLVEDBOARD:
            msg = "Solved!"

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop 
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos): # 用户点击reset选项的情况
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos): # 用户点击new选项的情况
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos): # 用户点击solve选项的情况
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                else:
                    # 如果getspotClicked没有返回(None, None)
                
                    blankx, blanky = getBlankPosition(mainBoard)
                    # 检查所点击的点周围是否挨着空白位置的一个贴片
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN
            
            elif event.type == KEYUP:
                # 用户同样可以按下键盘上的箭头和WASD键控制
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click title or press arrow keys to slide.', 8)
            # 显示滑动动画
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # 记录滑动
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    # 该函数会检查QUIT事件，然后调用terminate()函数
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        # 该循环会处理Esc按键的情况
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)   # 将其他KETYUP事件放回pygame.event队尾

def getStartingBoard():
    # 将创建并返回表示“已求解”游戏版的一个数据结构

    counter = 1
    # counter记录下一个贴片应该使用的编号
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = None
    return board


def getBlankPosition(board):
    # 遍历游戏版找到空白空格的坐标
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == None:
                return (x,y)


def makeMove(board, move):
    # 通过更新游戏板数据结构来移动
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    # 判断移动是否有效，取决于空白空格位于何处
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)

def getRandomMove(board, lastMove=None):
    # 在游戏的开始，我们从处于已求解的、有序状态的游戏数据结构开始，通过随机地移动贴片来创建谜题
    vaildMoves = [UP, DOWN, LEFT, RIGHT]

    # 防止函数选择上一次所做的移动
    if lastMove == UP or not isValidMove(board, DOWN):
        vaildMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        vaildMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        vaildMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        vaildMoves.remove(LEFT)

    # 返回列表中的随即项
    return random.choice(vaildMoves)


def getLeftTopOfTile(tileX, tileY):
    # 将贴片坐标转换为像素坐标
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top) 

def getSpotClicked(board, x, y):
    # 将像素坐标转换为游戏板坐标，功能与getLeftTopOfTile相反
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            # 如果像素坐标在该像素矩阵中
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def drawTile(tilex, tiley, number, adjx = 0, adjy = 0):
    # 绘制一个贴片
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    # 创建该方块的号码
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR) # 文本，是否抗锯齿，颜色
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect) 


def makeText(text, color, bgcolor, top, left):
    # 让文本显示在屏幕上
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
        
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])
    # 绘制游戏板的边框
    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
    # 绘制按钮
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF,SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):


    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # 创建一个图像的复制
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # 开始移动
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)            
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # 创建新的谜题

    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):  # 随机移动的次数
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', int(TILESIZE / 3))
        makeMove(board, move)   # 更新游戏板
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # 实现游戏板重置动画
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == LEFT:
            oppositeMove = RIGHT
        elif move == RIGHT:
            oppositeMove = LEFT
        slideAnimation(board, oppositeMove, '', int(TILESIZE / 2))
        makeMove(board, oppositeMove)

if __name__ == '__main__':
    main()

