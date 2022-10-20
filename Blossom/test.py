import random
from edmonds import Solve
from max_matching import test1

def generate_graph():
  random.seed(10)
  n = random.randint(0,10)
  g = [[] * n for i in range(0,n)]
  check = [[0] * n for i in range(0,n)]
  for i in range(0,n):
    for j in range(0,n):
      x = random.randint(0,1)
      if (x % 2 == 0):
        if (not check[i][j]):
          g[i].append(j)
          check[i][j] = 1
        if (not check[j][i]):
          check[j][i] = 1
          g[j].append(i)
  return g

def main():
  for i in range(1):
    g = generate_graph()
    correct = test1(g)
    print(correct)
    # solve = Solve(g)
    # my_ans = solve.edmonds()
    # assert(correct == my_ans)

if __name__ == "__main__":
    main()