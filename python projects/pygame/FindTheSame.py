import random, pygame, sys
from pygame.locals import *

BOARDWIDTH = 6      # 长度有六个方块
BOARDHEIGHT = 6     # 宽度有六个方块
BOXSIZE = 80       # 方块的像素的大小
BOXGAP = 10        # 方块之间间隙像素的大小
WINDOWWIDTH = 730   # 界面的长度像素大小
WINDOWHEIGHT = 730  # 界面的宽度像素大小
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (100, 100, 100)
GREEN = (50, 205, 50)
RED = (255, 0, 0)

BGCOLOR = BLACK
TEXTCOLOR = WHITE
BASICFONTSIZE = 70

XMARGIN = int((WINDOWWIDTH - (BOXGAP * (BOARDWIDTH - 1) + BOXSIZE * BOARDWIDTH )) / 2)
YMARGIN = XMARGIN

CIRCLE = 'circle'
SQUARE = 'square'
DIAMOND = 'diamond' # 菱形
TRIANGLE = 'triangle'
OVAL = 'oval'       # 椭圆
RECTANGLE = 'rectangle' # 长方形

ALLCOLORS = (RED, BLUE, GREEN)
ALLSHAPES = (CIRCLE, SQUARE, DIAMOND, TRIANGLE, OVAL, RECTANGLE)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "图案多于预设的数量"



def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    mousex = 0  # 鼠标的x坐标
    mousey = 0  # 鼠标的y坐标
    pygame.display.set_caption('Slide Puzzle')      # 设置游戏名称
    BASICFONT = pygame.font.Font('freesansbold.ttf',BASICFONTSIZE)          # 字体颜色
    # 设置New Game的选项
    # NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    # 设置主界面
    mainBoard = getRandomizedBoard()
    
    emptySpace = getBoxesAway(False)  # 游戏板中存在多少已经被移走的空位

    firstSelection = None     # 表示该图案是否为第一次点击

    DISPLAYSURF.fill(BGCOLOR)
    # startGameAnimation(mainBoard)    # 开场动画
    # chosenBoxes = setChosenBoxes(mainBoard)
    # 主游戏循环

    while True:
        mouseClicked = False    # 如果玩家点击鼠标，则该值为真

        DISPLAYSURF.fill(BGCOLOR)
        drawWhiteBoard(mainBoard)
        drawBoard(mainBoard, emptySpace)


        for event in pygame.event.get():            
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:  # 鼠标光标移动
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:  # 鼠标按下
                mousex, mousey = event.pos
                mouseClicked = True


            boxx, boxy = getBoxAtPixel(mousex, mousey)  # 获取鼠标所在的方块坐标
            if boxx != None and boxy != None:
                if not emptySpace[boxx][boxy]:
                    drawHighlightBox(boxx, boxy, GRAY)
                if not emptySpace[boxx][boxy] and mouseClicked:
                    # chosenBoxes[boxx][boxy] = True  # 游戏版中所有被选中的方块
                    drawHighlightBox(boxx, boxy, GREEN)
                    
                    if firstSelection == None:
                        firstSelection = (boxx, boxy)
                    else:
                        if firstSelection[0] != boxx or firstSelection[1] != boxy:
                            icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                            icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                            if icon1shape == icon2shape and icon1color == icon2color:
                                # 图像匹配
                                coverTheBoxes(mainBoard, boxx, boxy, BGCOLOR)
                                coverTheBoxes(mainBoard, firstSelection[0], firstSelection[1], BGCOLOR)
                                emptySpace[boxx][boxy] = True
                                emptySpace[firstSelection[0]][firstSelection[1]] = True
                            if hasWon(emptySpace):
                                gameWonAnimation(mainBoard)

                                mainBoard = getRandomizedBoard()
                                emptySpace = getBoxesAway(False)

                                drawWhiteBoard(mainBoard)
                                drawBoard(mainBoard, emptySpace)
                                pygame.display.update()
                        firstSelection = None
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def getBoxesAway(val):
    emptySpace = []
    for i in range(BOARDWIDTH):
        emptySpace.append([val] * BOARDHEIGHT)
    return emptySpace

def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    random.shuffle(icons)
    numIconsUsed = int(BOARDHEIGHT * BOARDWIDTH / 2)
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)
    # 将图像放置在游戏板上
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    # 用来获得方块的左上角像素坐标
    left = boxx * (BOXSIZE + BOXGAP) + XMARGIN
    top = boxy * (BOXSIZE + BOXGAP) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    # 用来获得方块坐标
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == CIRCLE:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), quarter)
        # 圆
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
        # 正方形
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top),(left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE -1), (left, top + half)))
        # 菱形
    elif shape == TRIANGLE:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + quarter, top + BOXSIZE - quarter), (left + BOXSIZE - quarter, top + BOXSIZE - quarter)))
        # 三角形
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))
    elif shape == RECTANGLE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - quarter))
        # 長方形


def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]


def coverTheBoxes(board, boxx, boxy, color):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, color, (left, top, BOXSIZE, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    

def drawBoard(board, emptySpace):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not emptySpace[boxx][boxy]:
                shape, color = getShapeAndColor(board, boxx ,boxy)
                drawIcon(shape, color, boxx, boxy)
            else:
                pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))

def drawWhiteBoard(board):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))

def drawHighlightBox(boxx, boxy, color):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, color, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def gameWonAnimation(board):
    textWonObj = BASICFONT.render('You Win!', False, WHITE)
    textRectObj = textWonObj.get_rect()
    textRectObj.center = (300, 300)
    DISPLAYSURF.blit(textWonObj, textRectObj)
    pygame.display.update()
    pygame.time.wait(3000)

def hasWon(emptySpace):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if emptySpace[i][j] == False:
                return False
    return True

if __name__ == '__main__':
    main()