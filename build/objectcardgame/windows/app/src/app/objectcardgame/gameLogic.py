import random

class NormalCard:
    triangleCount = 0
    squareCount = 0
    circleCount = 0
    def __init__(self, triangleCount, squareCount, circleCount):
        self.triangleCount = triangleCount
        self.squareCount = squareCount
        self.circleCount = circleCount
    def score(self):
        return min(self.triangleCount, self.squareCount, self.circleCount)
    def __repr__(self):
        return f"▲ {self.triangleCount}  ■ {self.squareCount}  ● {self.circleCount}"
    def __str__(self):  
        return f"▲ {self.triangleCount}  ■ {self.squareCount}  ● {self.circleCount}"
    def randomCard():
        triangleCount = random.randint(0, 2)
        squareCount = random.randint(0, 2)
        circleCount = random.randint(0, 2)
        return NormalCard(triangleCount, squareCount, circleCount)
    def __add__(self, other):
        if isinstance(other, NormalCard):
            return NormalCard(self.triangleCount+other.triangleCount, self.squareCount+other.squareCount, self.circleCount+other.circleCount)
        else:
            return NotImplementedError
    def __sub__(self, other):
        if isinstance(other, NormalCard):
            return NormalCard(self.triangleCount-other.triangleCount, self.squareCount-other.squareCount, self.circleCount-other.circleCount)
        else:
            return NotImplementedError
class SpecialCard:
    triangleCount = 0
    squareCount = 0
    circleCount = 0
    
    bonus=0
    def getObjectName(self):
        if self.triangleCount:
            return "▲"
        elif self.squareCount:
            return "■"
        elif self.circleCount:
            return "●"
        else:
            return None
    def __init__(self, triangleCount, squareCount, circleCount, bonus):
        self.triangleCount = triangleCount
        self.squareCount = squareCount
        self.circleCount = circleCount
        self.bonus = bonus
        if bonus ==0:
            raise ValueError("SpecialCard bonus cannot be 0")
    def __repr__(self):
        s=''
        if self.triangleCount:
            s+=f"▲ "
        if self.squareCount:
            s+=f"■ "
        if self.circleCount:
            s+=f"● "
        if self.bonus>0:
            s+=f"+{self.bonus}"
        else:
            s+=f"{self.bonus}"
        return s
    def __str__(self):  
        s=''
        if self.triangleCount:
            s+=f"▲ "
        if self.squareCount:
            s+=f"■ "
        if self.circleCount:
            s+=f"● "
        if self.bonus>0:
            s+=f"+{self.bonus}"
        else:
            s+=f"{self.bonus}"
        return s
    def randomCard():
        bonus = random.randint(-3, 3)
        if bonus == 0:
            return NormalCard.randomCard()
        match random.randint(0, 2):
            case 0:
                triangleCount = 1
                squareCount = 0
                circleCount = 0
                
                return SpecialCard(triangleCount, squareCount, circleCount, bonus)
            case 1:
                triangleCount = 0
                squareCount = 1
                circleCount = 0
                
                return SpecialCard(triangleCount, squareCount, circleCount, bonus)
            case 2:
                triangleCount = 0
                squareCount = 0
                circleCount = 1
                
                return SpecialCard(triangleCount, squareCount, circleCount, bonus)
            case _:
                raise ValueError("Invalid random number")


def shuffleforplayer(normalCardforEachPlayer=10, specialCardforEachPlayer=5):
    x=[NormalCard.randomCard() for i in range(normalCardforEachPlayer)]+[SpecialCard.randomCard() for i in range(specialCardforEachPlayer)]
    random.shuffle(x)
    return x

class Player:
    hand = []
    score = 0
    deckPtr=[]
    maxTries=64
    def getCardFromDeck(self,count=1    ):
        for i in range(count):
            try:
                self.hand.append(self.deckPtr.pop())
            except IndexError:
                print("Deck is empty")
                break
    def __init__(self,deckPointer,maxTries=64):
        self.hand = shuffleforplayer()
        self.score = 0
        self.maxTries=maxTries
        self.deckPtr=deckPointer
    def drawCard(self):
        return self.hand.pop()
    def draw3Cards(self):
        try:
            return [self.hand.pop() for i in range(3)]
        except IndexError:
            match len(self.hand):               
                case 2:
                    return [self.hand.pop() for i in range(2)]
                case 1:
                    return [self.hand.pop()]
                case _:
                    return []
    def draw3CardsAI(self):
        if self.maxTries==0:
            return self.draw3Cards()
        elif len(self.hand)<3:
            return self.draw3Cards()
        else:
            maxScore=0
            bestCards=[]
            for i in range(self.maxTries):
                random.shuffle(self.hand)
                cards=self.draw3Cards()
                a=NormalCard(0,0,0)
                for c in cards:
                    self.hand.append(c)
                    if isinstance(c, NormalCard):
                        a+=c
                score=a.score()
                if score>maxScore:
                    maxScore=score
                    bestCards=cards
                    self.maxTries-=1

            for i in bestCards:
                self.hand.remove(i)
            return bestCards


    
    def getScore(self,cards=None):
        if cards is None:

            x=self.draw3CardsAI()
        else:
            x=cards
        #print(x)
        nc=NormalCard(0,0,0)
        score=0
        drawnCards=[]
        for i in x:
            if isinstance(i, NormalCard):
                nc+=i
                
            else: #SpecialCard
                for j in range(abs(i.bonus)):
                    try:
                        a=self.deckPtr.pop()
                        drawnCards.append(a)
                    except IndexError:
                        print("Deck is empty")
                        a=[]
                    
                    if isinstance(a, NormalCard):
                        a2=NormalCard(a.triangleCount*i.triangleCount,a.squareCount*i.squareCount,a.circleCount*i.circleCount)
                        drawnCards.append(a2)
                        #print(f'S:{a2}',end='')
                        
                        if i.bonus>0:
                            nc+=a2
                            #print('|+')
                        else:
                            nc-=a2
                            #print('|-')
        #print(nc)                
        score+=nc.score()
        return [score,x,drawnCards,nc]
    def isempty(self):
        return len(self.hand)==0
PLAYER_COUNT=4
# winList=[0 for i in range(PLAYER_COUNT)]
# for Z in range(1000):
#     print(f"Game {Z+1}",end=' ')
#     deck=shuffleforplayer()*PLAYER_COUNT      
#     players=[Player() for i in range(PLAYER_COUNT)]
#     while not all(i.isempty() for i in players):
#         try:
#             v=0
#             sessionScoreList=[]
#             for i in players:

#                 sessionScore,cards=i.getScore()
                
#                 v+=1
#                 sessionScoreList.append(sessionScore)
#                 deck+=cards

#             highest=max(sessionScoreList)
#             highestPlayerindex=sessionScoreList.index(highest)
#             #print(f"Player {highestPlayerindex+1} wins with score {highest}")
#             players[highestPlayerindex].score+=1
#             for idx in range(len(players)):
#                 if idx!=highestPlayerindex:
#                     if len(deck)<3:
#                         raise ValueError("game over")
#                     try:
#                         players[idx].hand+=[deck.pop() for i in range(2)]
#                     except IndexError:
#                         raise ValueError("game over")
                        
#                 else:   
#                     try:
#                         players[idx].hand+=[deck.pop() for i in range(3)]
#                     except IndexError:
#                         raise ValueError("game over")
#         except ValueError:
#             break

#     for i in players:
#         pass
#         #print(f"Player {players.index(i)+1} score: {i.score}, hand: {i.hand}")
#     winner=max(players, key=lambda x: x.score)
#     winneridx=players.index(winner)+1
#     print(f"Player {winneridx} wins the game with score {winner.score}")
#     winList[winneridx-1]+=1
# print(winList)
    
def getallDeck(playerCount=PLAYER_COUNT):
    return shuffleforplayer()*(playerCount*2)

normalcardList=[]
specialcardList=[]

# for i in getallDeck(2):
#     if isinstance(i, NormalCard):
#         normalcardList.append(i)
#     else:
#         specialcardList.append(i)
# print(f"Normal card count: {len(normalcardList)}")
# c=0
# for i in normalcardList+specialcardList:
#     print(i,end='\t|')
#     c+=1
#     if c%4==0:
#         print()



    
    