import re
import collections
import random

alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
sign = ['.','?','!',':',';','—', '\n']
alph = list(alph)

class HomeWork:

  def CountWords(self,str:str) -> None:
      rep = re.compile("[^a-zA-Zа-яА-я,\d]")
      str = (rep.sub(" ", str)).replace(",", " ")
      words = str.split()
      print(len(words))
      count = collections.Counter(words)
      print(count.most_common()[:10:1])

  def Reverse(self ,str:str) -> None:
      buf = ""
      text = list()

      i = 0
      while(i < len(str)):
          while(str[i] in alph):
              buf += str[i]
              i += 1

          if(len(buf) > 0):
              text.append(buf)

          else:
              text.append(str[i])
              i += 1
          buf = ""

      i = 0
      buft = []
      rev_text = ""

      while(i < len(text)):
          while(text[i] not in sign):
              buft.append(text[i])
              i += 1
          if (text[i] in sign):
              buft.reverse()
              for t in buft:
                  rev_text += t
              rev_text += text[i]
              i += 1
          buft = []

      print(rev_text)

  def TextAnalysis(self, str:str) -> None:
      with open(str, "r") as file:
          content = file.read()
      self.CountWords(content)
      #self.Reverse(content)

  def FindNumber(self, n: int) -> None:
      dic = list()
      for i in range(1, n + 1):
          c = 0
          t = i
          while(t != 1):
              if t % 2 == 0:
                  t /= 2
              else:
                  t = 3 * t + 1
              c += 1
          dic.append(c)
      print(dic)
      print(dic.index(max(dic)) + 1)

  def RiddleForUser(self, n:int) -> None:
      ans = False
      c = 0
      while(ans != True):
          get_ans = int(input("Enter your variant: "))
          c += 1
          if(get_ans < n):
              print("Your number is less")

          if(get_ans > n):
              print("Your number is higher")

          if(get_ans == n):
              print("You guessed it (Attempts:" + str(c) + ")")
              print("The number is " + str(n))
              print("---------------------------------")
              ans = True

  def RiddleForComp(self,n :int, t:int) -> None:
      l = 1
      r = n
      c = 0
      while(l <= r):
          m = int((l + r) / 2)
          c += 1

          if (t == m):
              print("Computer guess random number (" + str(t) + ")")
              print("The attempt - " + str(c))
              break

          if (t < m):
              r = m - 1
          else:
              l = m + 1

if __name__ == '__main__':
    user = HomeWork()
    #user.TextAnalysis("Book.txt")
    #user.FindNumber(1000)
    n = int(input("Enter the number: "))
    #user.RiddleForUser(int(random.uniform(1, n)))
    user.RiddleForComp(n, int(random.uniform(1, n)))