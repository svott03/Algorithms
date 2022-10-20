import copy

class Solve:
  def __init__(self,g):
    self.g = g

  def improve_matching(self, m,p):
    #p is guaranteed to be even (odd # of edges => even # of vertices)
    for i in range(0,len(p),2):
      m[p[i]] = 1
      m[p[i+1]] = 1

  def edmonds(self):
    # Find augmenting path
    n = len(self.g)
    # Unmarked Nodes: -1, Marked Nodes: Matched Node
    m = [-1] * n
    temp_graph = copy.deepcopy(self.g)
    match = Match(self.g,m)
    p = match.aug_path()
    while(len(p) > 0):
      self.improve_matching(m,p)
      # TODO v + e cost each iteration
      match = Match(self.g,m)
      p = match.aug_path()

    # count number of unmatched nodes
    c = 0
    for i in range(0,n):
      if (m[i] == -1):
        c += 1
    return c


class Match:

  def __init__(self,g,m):
    self.n = len(g)
    self.forest = set()
    self.g = g
    self.m = m

    # TODO marked may have to be updated after contraction or after a new aug path call in edmonds
    self.marked = [0] * self.n
    
    # Maintain set of marked edges
    self.s = [set() for i in range(0,self.n)]

    # Union find Data Structure
    self.parents = [i for i in range(0,self.n)]

    self.tree = dict()
    for v in range(0,self.n):
      self.tree[v] = [[] for i in range(0,self.n)]

    # Add each exposed vertex to forest
    for i in range(0,self.n):
      if (m[i] == -1):
        self.forest.add(i)
      else:
        self.union(i,m[i])

  def contract_graph(self, cycle):
    supernode = self.n
    g_prime = [[] for i in range(0,supernode+1)]
    for i in range(0,self.n):
      for j in range(0,len(self.g[i])):
        if (i in cycle and self.g[i][j] not in cycle):
          g_prime[supernode].append(self.g[i][j])
          g_prime[self.g[i][j]].append(supernode)
        elif (i not in cycle and self.g[i][j] in cycle):
          g_prime[supernode].append(i)
          g_prime[i].append(supernode)
        elif (i not in cycle and self.g[i][j] not in cycle):
          g_prime[i].append(self.g[i][j])
          g_prime[self.g[i][j]].append(i)
    return g_prime


  def get_path(self, cur, target, vis):
    vis[cur] = 1
    if (cur == target): return []
    for v in self.tree[cur]:
      if (not vis[v]):
        temp = self.get_path(v,target,vis)
        if (vis[target]):
          # TODO construct path faster
          temp.insert(0,cur)
          return temp
    return []

  def find(self, parents, u):
    if (parents[u] == u):
      return u
    parents[u] = self.find(parents[u])
    return parents[u]

  # merge 2 trees
  def merge(self, u,v):
    # put edges in u into v
    for i in range(0,self.n):
      for j in range(0,len(self.tree[u][i])):
        x = self.tree[u][i][j]
        self.tree[v][x].append(i)
        self.tree[v][i].append(x)

  def union(self, u, v):
    a = self.parents[u]
    b = self.parents[v]
    if (a != b):
      self.merge(a,b)
      self.parents[u] = b

  # dfs to find distance between 2 nodes
  def dfs(self, v, root, dist, vis):
    vis[v] = 1
    if (v == root): return dist
    for neighbor in self.tree[v]:
      if (not vis[neighbor]):
        temp = self.dfs(neighbor, root,dist+1,vis)
        if (vis[root]):
          return temp
    return dist

  # finds distance between 2 nodes
  def distance(self, v, root):
    dist = 0
    vis = [0] * self.n
    return self.dfs(v,root, 0, vis)

  # dfs to find even path
  def get_even_path(self, start, target, cycle):
    edges = []
    first_node = -1
    for i in range(0,len(self.tree[self.parents[start]][start])):
      if self.tree[self.parents[start]][start][i] in cycle:
        first_node = self.tree[self.parents[start]][start][i]
        break

    for i in range(0,len(self.tree[self.parents[first_node]][first_node])):
      if (self.tree[self.parents[first_node]][first_node][i] in cycle and 
      self.tree[self.parents[first_node]][first_node][i] != start):
        edges.append(self.tree[self.parents[first_node]][first_node][i])

    # assert len(edges) == 2
    vis = [0] * self.n
    vis[start] = 1
    vis[first_node] = 1
    p = self.get_path(edges[0],target,vis)
    if len(p) % 2 == 1:
      p.insert(0,first_node)
      p.insert(0,start)
      return p
    else:
      p = self.get_path(edges[0],target,vis)
      p.insert(0,first_node)
      p.insert(0,start)
      return p

  def aug_path(self):
    # While there is an unmarked vertex in F with distance(v, root(v)) even
    for v in self.forest:
      # if marked, continue
      if (self.marked[v]): continue
      d = self.distance(v, self.parents[v])
      if (d % 2 == 1): continue
      # find unmarked edge
      for j in range(0,len(self.g[v])):
        w = self.g[v][j]
        # Unmarked Edge e = (v,w)
        if (w not in self.s[v]):
          # if w is not in forest
          if (w not in self.forest):
            # w is matched, so add e and w's matched edge to F
            x = self.m[w]
            # add edges { v, w } and { w, x } to the tree of v
            # order of union arguments matters for merging trees
            self.union(v,w)
            self.tree[self.parents[v]][v].append(w)
            self.tree[self.parents[v]][w].append(v)
          elif (self.distance(w,self.parents[w]) % 2 == 0):
            if (self.parents[v] != self.parents[w]):
              # Report an augmenting path in F 
              vis = [0] * self.n
              p = self.get_path(v,self.parents[v],vis)
              p.append(v)
              x = self.get_path(w,self.parents[w],vis)
              p.extend(x)
              p.append(w)
              return p
            else:
              # Contract a blossom in G and look for the path in the contracted graph.
              # Find Cycle
              vis = [0] * self.n
              cycle = self.get_path(v,self.parents[v],vis)
              cycle.append(w)
              cycle.extend(self.get_path(w,self.parents[w],vis))
              cycle = set(cycle)
              # Contract Cycle into SuperNode S to form G'
              contracted_graph = self.contract_graph(cycle)
              # Find aug_path p in G'
              match = Match(contracted_graph,self.m)
              p = match.aug_path()
              supernode = self.n
              # p = w -> va -> vb -> ve
              p_va = []
              for i in range(0,len(p)):
                if p[i] == supernode: break
                p_va.append(p[i])
              p_vb = []
              for i in reversed(range(0,len(p))):
                if p[i] == supernode: break
                p_vb.append(p[i])
              # Find even path from vb to va in cycle, let this path be p'
              vis = [0] * self.n
              cycle.add(p_va[-1])
              cycle_path = self.get_even_path(p_vb[-1], p_va[-1],cycle)
              p_va.extend(cycle_path)
              p_va.extend(p_vb)
              return p_va

          # mark edge e
          self.s[v].add(w)
          self.s[w].add(v)
      # mark node v
      self.marked[v] = 1
    return []