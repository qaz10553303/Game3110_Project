import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json
import urllib
import urllib.parse
import urllib.request
import random
from threading import Timer

playerInQueue=[]

def connectionLoop(sock):
   while True:
      data, addr = sock.recvfrom(1024)
      res=json.loads(data.decode())
      res['WaitTime']="0"
      res['Addr']=addr
      # print("Got this: "+str(res)+" From: "+str(addr))
      playerInQueue.append(res)
      
      # print(playerInQueue)
      # print(len(playerInQueue))
      
      # if len(playerInQueue)>=3:
      #    simulateMatch(playerInQueue[0],playerInQueue[1],playerInQueue[2])
      #    playerInQueue=[]
      
      

         
def matchMakingServer(sock):
   playerInGame=[]
   while True:
      # print(playerInQueue[7]['WaitTime'])   
      for player in playerInQueue:
         player['WaitTime']=int(player['WaitTime'])+1
      if len(playerInQueue)>=2 or playerInGame:
         if not playerInGame:
            playerInGame.append(playerInQueue[0])
            p1Max=int(playerInGame[0]['MMR'])+int(playerInGame[0]['WaitTime'])*20
            p1Min=int(playerInGame[0]['MMR'])-int(playerInGame[0]['WaitTime'])*20
            del playerInQueue[0]
            # print(len(playerInQueue))
         # playerInGame.append[playerInQueue[0]]
         # del playerInQueue[0]
         else:
            print(len(playerInQueue))
            for i in range(0,len(playerInQueue)):
                  # print(playerInGame)
                  # print("len="+str(len(playerInQueue))+"i="+str(i))
                  p2Max=int(playerInQueue[i]['MMR'])+int(playerInQueue[i]['WaitTime'])*20
                  p2Min=int(playerInQueue[i]['MMR'])-int(playerInQueue[i]['WaitTime'])*20
                  # print(p1Max)
                  if p1Max>=p2Min or p1Min<=p2Max:
                     if playerInQueue[i] not in playerInGame:
                        playerInGame.append(playerInQueue[i])
                        del playerInQueue[i]
                        # print(playerInGame)
                        if len(playerInGame)==2:
                           simulateMatch(playerInGame[0],playerInGame[1],sock)
                           playerInGame=[]
                           break
      time.sleep(1)
      # for i in range(1, len(playerInQueue)):
      #    print(i)
            




def simulateMatch(player1,player2,sock):
   print("MatchFound!\n"+str(player1)+str(player2))
   
   p1k=random.randint(0,5)
   p2k=random.randint(0,5)
   p1d=random.randint(0,5)
   p2d=random.randint(0,5)
   temp_total= int(player1['MMR'])+int(player2['MMR'])
   temp_delta= abs(int(player1['MMR'])-int(player2['MMR']))
   if int(player1['MMR'])>int(player2['MMR']):
      p1Extra=-temp_delta/20
      p2Extra=temp_delta/20
      if p1Extra<=-50:
         p1Extra=-50
      if p2Extra>=50:
         p2Extra=50
   if int(player1['MMR'])<int(player2['MMR']):
      p1Extra=temp_delta/20
      p2Extra=-temp_delta/20
      if p2Extra<=-50:
         p2Extra=-50
      if p1Extra>=50:
         p1Extra=50
         

   player1['Kill']=str(int(player1['Kill'])+p1k)
   player1['Death']=str(int(player1['Death'])+p1d)
   player1['Level']=str(int(player1['Level'])+1)
   player2['Kill']=str(int(player2['Kill'])+p2k)
   player2['Death']=str(int(player2['Death'])+p2d)
   player2['Level']=str(int(player2['Level'])+1)
      
      
   temp=random.randint(1,2)
   if temp==1:
      player1['Win']=str(int(player1['Win'])+1)
      player2['Lose']=str(int(player2['Lose'])+1)
      player1['MMR']=str(int(player1['MMR'])+100+(p1k-p1d)*20)
      player2['MMR']=str(int(player1['MMR'])-50+(p2k-p2d)*20)
      winner=player1['UserName']
   elif temp==2:
      player2['Win']=str(int(player2['Win'])+1)
      player1['Lose']=str(int(player1['Lose'])+1)
      player1['MMR']=str(int(player1['MMR'])-50+(p1k-p1d)*20)
      player2['MMR']=str(int(player1['MMR'])+100+(p2k-p2d)*20)
      winner=player2['UserName']
      
   gameId=getGameEvent()+1
   print(gameId)
   GameEvent={"GameID":str(gameId),"AverageMMR":str(temp_total/2),"P1":player1['UserName'],"P2":player2['UserName'],"TimeStamp":str(time.time()),"Winner":winner}
   # print(GameEvent)
   updateGameEvent(GameEvent)
   sock.sendto(json.dumps(player1).encode(), player1['Addr'])
   sock.sendto(json.dumps(player2).encode(), player2['Addr'])

def getGameEvent():
   res = urllib.request.urlopen("https://l7y17s14ve.execute-api.us-east-2.amazonaws.com/default/F_UserManagement").read().decode("utf-8")
   # res.reverse()[0]
   res=json.loads(res)
   # res.reverse()
   if res:
      # return res[0]['GameID']
      maxGameId=int(res[0]['GameID'])
      for item in res:
         if int(item['GameID'])>maxGameId:
            maxGameId=int(item['GameID'])
      return maxGameId
      
def updateGameEvent(GameEvent):
   GameID=GameEvent['GameID']
   AverageMMR=GameEvent['AverageMMR']
   P1=GameEvent['P1']
   P2=GameEvent['P2']
   TimeStamp=GameEvent['TimeStamp']
   Winner=GameEvent['Winner']
   item={
      "GameID":GameID,
      "AverageMMR":AverageMMR,
      "P1":P1,
      "P2":P2,
      "TimeStamp":TimeStamp,
      "Winner":Winner
   }
   # data = str(item).encode('utf-8')
   data = bytes(json.dumps(item),'utf8')
   headers = {"Content-Type": "application/json"}
   req = urllib.request.Request("https://l7y17s14ve.execute-api.us-east-2.amazonaws.com/default/F_UserManagement", data=data, headers=headers)
   res = urllib.request.urlopen(req)
   print(res.read().decode("utf-8")) 


def main():
   #post
   # data = urllib.parse.urlencode({"name":"qb", "age": 12}).encode("utf-8")
   # req = urllib.request.Request("https://nxsy27mns5.execute-api.us-east-2.amazonaws.com/default/Test", data=data)
   # res = urllib.request.urlopen(req)
   # print(res.read().decode("utf-8")) 
   #post1
   # myname="123"
   # data = str({"name":myname, "age": 12}).encode('utf-8')
   # headers = {"Content-Type": "application/json"}
   # req = urllib.request.Request("https://nxsy27mns5.execute-api.us-east-2.amazonaws.com/default/Test", data=data, headers=headers)
   # res = urllib.request.urlopen(req)
   # print(res.read().decode("utf-8")) 
   
   # print(getGameEvent())
   
   #get
   # res = urllib.request.urlopen("https://nxsy27mns5.execute-api.us-east-2.amazonaws.com/default/Test")
   # print(res.read().decode("utf-8"))

   port = 12345
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.bind(('', port))

   start_new_thread(connectionLoop, (s,))
   start_new_thread(matchMakingServer, (s,))
   while True:
      time.sleep(1)

if __name__ == '__main__':
   main()
