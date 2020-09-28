import re
import collections
import random

alph = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
sign = ['.','?','!',':',';','—', '\n']
alph = list(alph)

class HomeWork:


  def Maxormin(self, n1, n2):
      if(n1 > n2):
          print(str(n1) + " > " + str(n2) )
      elif(n1 == n2):
          print(str(n1) + " = " + str(n2) )
      else:
          print(str(n1) + " < " + str(n2) )
      print(type(n1))

      if (type(n1) == list and type(n1) == list):
          if (len(n1) < len(n2)):
              print("Len of " + str(n1) + " > " + str(n2))
          elif (len(n1) == len(n2)):
              print("Len of " + str(n1) + " = " + str(n2))
          else:
              print("Len of " + str(n1) + " < " + str(n2))

  def MaxOrMinMany(self, mas):
        max = mas[0]
        for i in range(len(mas)):
            if mas[i] > max:
                max = mas[i]
        print(max)

  def OrderNumber(self, n):
      mas = list()
      for k in range(2, n + 1):
          order = True
          for i in range(2, k):
              if k % i == 0:
                  order = False
                  break
          if order:
              mas.append(k)
      return mas

  def Del(self, n):
      mas = list()
      for i in range(n, 0, -1):
          if (n % i == 0):
              mas.append(i)

      return mas

  def GDR(self, n1, n2):
      while n1 != 0 and n2 != 0:
          if n1 > n2:
              n1 %= n2
          else:
              n2 %= n1

      gcd = n1 + n2
      print(gcd)

  def convert(self, n, to_base, from_base):
      if isinstance(n, str):
          n = int(n, from_base)
      else:
          n = int(n)

      if n < to_base:
          return alph[n]
      else:
          print(alph[n % to_base])
          return self.convert(n // to_base, to_base, from_base) + alph[n % to_base]


if __name__ == '__main__':
    user = HomeWork()
    user.Maxormin(["x", -1], ["abc", 1])
    user.MaxOrMinMany([[1,2,3], [2,5,6]])
    ans = user.OrderNumber(1000)
    ans = user.Del(7)
    user.GDR(10, 15)
    ans = user.convert('FAA', from_base=16, to_base=10)
    print(ans)
    #user.RiddleForUser(int(random.uniform(1, n)))