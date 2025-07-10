import objectcardgame.gameLogic as gameLogic
from objectcardgame.gameLogic import PLAYER_COUNT 
import random
from objectcardgame.cardASCII import *
from colorama import init, Fore, Back, Style
init()

SEPARATE_LENGTH=6
PlayerCount=PLAYER_COUNT
STEP=64


cmdList={'help':HELP,'quit':'离开游戏','sp':'sp <length>\n每一列显示的牌数','pc':'pc <number>\n设置玩家数量','step':'step <number>\n设置玩家思考步数\n步数越大，时间越久'}
def interpretCommand(string):
    keys=cmdList.keys()
    values=cmdList.values()
    if isCommand(string):
        if string.startswith('sp'):
            global SEPARATE_LENGTH
            try:
                SEPARATE_LENGTH=int(string.split()[1])
                print(f"分隔长度已设置为{SEPARATE_LENGTH}")
            except:
                print("输入格式不正确")
        elif string.startswith('help'):
            if len(string.split())==1:
                print(HELP)
                print("命令列表:")
                for i in keys:
                    print(i)
            else:

                print(cmdList[string.split()[1]])
                
        elif string.startswith('quit'):
            print("退出游戏")
            raise SystemExit
        elif string.startswith('pc'):
            try:
                global PlayerCount
                PlayerCount=int(string.split()[1])
                print(f"玩家数量已设置为{PlayerCount}")
            except:
                print("输入格式不正确")

        elif string.startswith('step'):
            try:
                global STEP
                STEP=int(string.split()[1])
                print(f"玩家思考步数已设置为{STEP}")
            except:
                print("输入格式不正确")
    else:
        print("输入指令不正确")
def isCommand(string):
    for i in cmdList:
        if string.startswith(i):
            print(cmdList[i])
            return True
    return False

def printHand(player:gameLogic.Player):
    l=[]
    for index,card in enumerate(player.hand):  
    
        l.append(getCardClass(index+1,card))
    printListofCards(l,SEPARATE_LENGTH)
def printListofCards2(lst,separateLength=6):
    tmp=[]
    for index,card in enumerate(lst):
        tmp.append(getCardClass(index+1,card))
    printListofCards(tmp,SEPARATE_LENGTH)

print(Fore.CYAN,HEADING)

print(f'{Fore.GREEN}欢迎来到图形记分牌！{Fore.RESET}')
print()
for key,value in cmdList.items():
    if key=='help':
        print(f"{Fore.YELLOW}{key}\n{Fore.RESET}\n显示帮助")
        print()
        continue
    print(f"{Fore.YELLOW}{key}\n{Fore.RESET}\n{value}")
    print()
inputStr=input("按下回车开始游戏,或者输入指令：\n>")

while inputStr!='':
    interpretCommand(inputStr)
    inputStr=input('>')

print("游戏开始。")


PlayerCount-=1
while True:
    print('正在洗牌')
    deck=gameLogic.shuffleforplayer()*PlayerCount
    players=[gameLogic.Player(deck,STEP) for i in range(PlayerCount)]
    you=gameLogic.Player(deck,0) # only AI needs STEP


    isAnyoneEmpty=False
    while not isAnyoneEmpty:
        
        flag=True
        while flag:
            printHand(you)
            print('出牌\n请输入你想出的牌的序号，以(,)分隔。')
            inputStr=input(">draw ")
            if isCommand(inputStr):
                interpretCommand(inputStr)
                continue
            if inputStr=='':
                print("输入为空")
                inputStr='1,2,3'
            inputList=inputStr.split(',')
            if len(inputList)>3:
                print("输入的牌不能大于3")
                continue
            for i in range(3-len(inputList)):
                inputList.append(0)
            flag=False
            drawCards=[]
            
            for i in inputList:
                try:
                    if i==0:
                        continue    
                    num=int(i)
                    drawCards.append(you.hand[num-1])
                except:
                    pass
            if inputList[0]==inputList[1] or inputList[0]==inputList[2] or inputList[1]==inputList[2]:
                print("输入的牌不能重复")
                flag=True
            
            for index,card in enumerate(drawCards):

                try:
                    you.hand.remove(card)
                except:
                    pass


            if flag:
                continue
        print(f"{Fore.CYAN}出牌:{Fore.RESET}")
        printListofCards2(drawCards)
        thisSessionScore=[]
        score,_,drawnCards,result=you.getScore(drawCards)
        thisSessionScore.append(score)
        printListofCards2(drawnCards)
        print(f"{Fore.CYAN}得分: {score}({result}){Fore.RESET}")
        print('等待其他玩家出牌...')


        for i in players:
            if not i.isempty():
                print(f"{Fore.YELLOW}玩家",players.index(i)+1,f"的回合:")
                score,x,drawnCards,nc=i.getScore()
                thisSessionScore.append(score)
                printListofCards2(x)
                printListofCards2(drawnCards)
                print(Fore.RESET)

        print(f"{Fore.CYAN}本局得分:")
        print(f"得分: {thisSessionScore[0]}")
        for index,score in enumerate(thisSessionScore[1:]):

            print(f"玩家 {index+1}: {score}")
        print(Fore.RESET)

        maxScore=max(thisSessionScore)
        maxIndex=thisSessionScore.index(maxScore)
        if maxIndex==0:
            print(f"{Fore.GREEN}你赢了本局。{Fore.RESET}")
        else:
            print(f"{Fore.GREEN}玩家{maxIndex}赢了本局。{Fore.RESET}")
            # print("玩家",maxIndex,"赢了本局。")
        
        allPlayer=[you]+players
        for i in allPlayer:
            i.getCardFromDeck(3)
        allPlayer[maxIndex].score+=1
        try:
            l=allPlayer[maxIndex].hand[-1]
            allPlayer[maxIndex].hand.remove(l)
            deck.append( l ) # winner only gets 2 cards from the deck.
        except:
            pass
        print("当前分数:")
        print(f"你: \t\t{you.score}")
        for i in allPlayer[1:]: 
            print(f"玩家 {players.index(i)+1}:\t\t {i.score}")
        
        for i in allPlayer:
            if i.isempty():
                isAnyoneEmpty=True
                break
        if len(deck)==0:
            print("牌库已空！")
            isAnyoneEmpty=True

        print("下一轮开始。")
        print()
        input('按下回车继续')

    print("游戏结束。")
    print()
    print(f"{Fore.MAGENTA}最终分数:")
    print(f"你: \t\t{you.score}")
    for i in players:
        print(f"玩家 {players.index(i)+1}:\t\t {i.score}")
    allScores=[you.score]+[i.score for i in players]
    maxScore=max(allScores)
    maxIndex=allScores.index(maxScore)
    if maxIndex==0:
        print(f"{Fore.GREEN}你赢了游戏！{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}玩家{maxIndex}赢了游戏！{Fore.RESET}")

    inputStr=input("按下回车开始下一局,或者输入指令：\n>")

    while inputStr!='':
        interpretCommand(inputStr)
        inputStr=input('>')

    
        




# for i in range(PlayerCount):
#     print("Player",i+1,"'s hand:")
#     Ls=[]
    
#     for index,card in enumerate(players[i].hand):   
#         getCardClass(index+1,card)
#         Ls.append(getCardClass(index+1,card))
#     printListofCards(Ls,SEPARATE_LENGTH)
