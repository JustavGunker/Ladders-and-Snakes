from turtle import Turtle

cubesize = 40 

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

posArray = []
currentNum = 1
inputPosX = 0
inputPosY = 0
size = 0
count = 0



t = Turtle()
t.hideturtle()
t.speed('fastest')
t.screen.title('Snakes and Ladders')
t.screen.bgcolor("white")

def fillGrid(size):
    startX = -(size/2)*cubesize + cubesize/2 - 2 # -2 is corellation for width of drawing
    startY = -(size/2)*cubesize + cubesize/2 - 7 # -7 is corellation for height of drawing
    t.teleport(startX,startY)
    num = 1
    for j in range(size):
        t.teleport(startX,startY+j*cubesize)
        for p in range(size):
            posX,posY = t.pos()
            corrX = 3*(len(str(num))-1) # corellation with number of integers in int
            t.teleport(startX+p*cubesize-corrX,posY) 
            t.write(str(num)) # draw number
            x,y = t.pos()
            posArray.append(Position(x+corrX,y)) # save objects with position
            num+=1

def getPos(posArray,num):
    return posArray[num-1].x, posArray[num-1].y

def drawSnake(posArray,startNum,endNum):
    startX, startY = getPos(posArray,startNum)
    endX, endY = getPos(posArray,endNum)
    t.pensize(10)
    t.color('green')
    t.teleport(startX,startY)
    t.goto(endX,endY)
    t.dot(20)
    t.pensize(1)

def drawLadder(posArray,startNum,endNum):
    startX, startY = getPos(posArray,startNum)
    endX, endY = getPos(posArray,endNum)
    t.pensize(10)
    t.color('brown')
    t.teleport(startX,startY)
    t.goto(endX,endY)
    t.pensize(1)


def drawGrid(size):
    #totalX, totalY = t.screen.screensize()
    t.home()
    startX = -(size/2)*cubesize
    startY = (size/2)*cubesize
    t.teleport(startX,startY)
    t.setheading(270) # Head south
    # Drawing left wall
    for _ in range(size): 
        t.forward(cubesize)
    # Drawing interior + top and right wall
    k = 0
    i = 0
    for k in range(size):
        for i in range(size):
            t.teleport(startX+cubesize*k,startY-cubesize*i)
            t.setheading(0) #Head east
            t.forward(cubesize)
            t.setheading(270)
            t.forward(cubesize)
     # Drawing bottom wall
    t.teleport(startX,-startY)
    t.setheading(0)
    for _ in range(size):
        t.forward(cubesize)
    fillGrid(size)

    global inputPosX
    global inputPosY
    inputPosX = startX
    inputPosY = -startY-3*cubesize
    t.teleport(inputPosX,inputPosY+cubesize)
    t.write('Choose advancement:')
    t.teleport(inputPosX,inputPosY)
    for _ in range(5):
        t.teleport(inputPosX+_*cubesize,inputPosY)
        t.write(str(_+1))


def boardInit():
    global size
    f = open('lvl2.txt','r')
    size, connections = [int(_) for _ in f.readline().split()]
    adjacency_list = [[] for _ in range(size*size)]
    
    for i in range(connections):
        s,e = [int(_) for _ in f.readline().split()]
        adjacency_list[s].append(e)
    for k in range(size*size):
        for j in range(5):
            if k+j+2 > size*size:
                adjacency_list[k].append(size*size-1) # always fill adjacency list
            else:
                adjacency_list[k].append(k+j+1)
    drawGrid(size)
    return adjacency_list

def drawCircle(x,y):
    t.color('red')
    t.teleport(x+1,y-4)
    t.circle(12)
    t.color('black')
    
def undrawCircle(x,y):
    t.color('white')
    t.teleport(x+1,y-4)
    t.circle(12)
    t.color('black')

def updatePos(nextNum):
    global posArray
    global currentNum
    currentX,currentY = getPos(posArray,currentNum)
    nextX,nextY = getPos(posArray,nextNum)
    undrawCircle(currentX,currentY)
    drawCircle(nextX,nextY)
    

def move(input):
    global currentNum
    global adjacency_list
    global posArray
    global count
    global size
    count += 1
    nextNum = adjacency_list[currentNum-1][input-1]+1 #-1 to counter the currentNum moves are from 1 to five
    updatePos(nextNum)
    currentNum = nextNum
    if adjacency_list[currentNum-1][0]+1 < currentNum:
            drawSnake(posArray,currentNum,adjacency_list[currentNum-1][0]+1)
            nextNum = adjacency_list[nextNum-1][0]+1
            updatePos(nextNum)
    if adjacency_list[currentNum-1][0]+1 >= adjacency_list[currentNum-1][1]+1 & adjacency_list[currentNum-1][1]+1 != size*size: # +1 since the next is always 1 higher
        drawLadder(posArray,currentNum,adjacency_list[currentNum-1][0]+1)
        nextNum = adjacency_list[nextNum-1][0]+1
        updatePos(nextNum)
    
    currentNum = nextNum
    advanceGame()


def getInput(x,y):
    global inputPosX
    global inputPosY
    if ((x < inputPosX+10.0) & (x >inputPosX-10.0)) & ((y < inputPosY+10.0) & (y > inputPosY-2.0)):
        input = 1
        print('input: ', input)
        t.screen.onclick(None)
        move(input)
    elif ((x < inputPosX+cubesize+10.0) & (x >inputPosX+cubesize-10.0)) & ((y < inputPosY+10.0) & (y > inputPosY-2.0)):
        input = 2
        print('input: ',input)
        t.screen.onclick(None)
        move(input)
    elif ((x < inputPosX+2*cubesize+10.0) & (x >inputPosX+2*cubesize-10.0)) & ((y < inputPosY+10.0) & (y > inputPosY-2.0)):
        input = 3
        print('input: ',input)
        t.screen.onclick(None)
        move(input)
    elif ((x < inputPosX+3*cubesize+10.0) & (x >inputPosX+3*cubesize-10.0)) & ((y < inputPosY+10.0) & (y > inputPosY-2.0)):
        input = 4
        print('input: ',input)
        t.screen.onclick(None)
        move(input)
    elif ((x < inputPosX+4*cubesize+10.0) & (x >inputPosX+4*cubesize-10.0)) & ((y < inputPosY+10.0) & (y > inputPosY-2.0)):
        input = 5
        print('input: ',input)
        t.screen.onclick(None)
        move(input)
    
def tryAgain(x,y):
    global currentNum
    global count
    if ((-5.0 < x) & (x < 50.0)) & ((-55.0 < y) & (y < -35.0)):
        t.screen.onclick(None)
        currentNum = 1
        count = 0
        main()


def victoryScreen():
    global count
    t.clear()
    t.teleport(0,0)
    t.write('Congratulations!')
    t.teleport(0,-15)
    t.write('You finished in: ')
    t.teleport(0,-30)
    t.write(str(count))
    t.teleport(5+len(str(count))*5,-30)
    t.write('steps')
    t.teleport(0,-45)
    t.write('Try again?')

def advanceGame():
    global currentNum
    global size
    if currentNum >= size*size:
        victoryScreen()
        t.screen.onclick(tryAgain)
        return
    else: 
        t.screen.onclick(getInput)


def main():
    t.screen.clear()
    global adjacency_list
    adjacency_list = boardInit()
    updatePos(1)
    advanceGame()
    t.screen.mainloop()

main()
