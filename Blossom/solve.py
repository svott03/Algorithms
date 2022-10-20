from edmonds import Solve
from max_matching import test1

#Finds valid pairing
def loop(x,y):
    if (x > y):
        x,y = y,x
    vis = [[False]*(3*y) for i in range(3*y)]
    while (x != y):
        if (vis[x][y]):
            return True
        vis[x][y] = True
        y -= x
        x += x
        if (x > y):
            x,y = y,x
    return False

def solution(banana_list):
    #Your code here
    n = len(banana_list)
    g = [[] for i in range(n)]
    #form connected graph
    for i in range(0,n):
        for j in range(i+1,n):
            if (loop(banana_list[i],banana_list[j])):
                g[i].append(j)
                g[j].append(i)

    #greedy does not work
    #find the maximum matching in this non bipartite graph
    #blossom algorithm
    # Return the sum of the maximum matching on each connected component
    # solve = Solve(g)
    return test1(g)
    # return solve.edmonds()

print(solution([1, 7, 3, 21, 13, 19]))
print(solution([1,1]))
print(solution([1,1,1,2]))