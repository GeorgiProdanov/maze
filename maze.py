import wx
import msvcrt as kb
import inspect
import keyboard


class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.allAdj = set()
		self.posAdj = list()
		self.setAllAdj()
		self.left = 0
		self.right = 0
		self.up = 0
		self.down = 0
	
	def checkBound(self,x, y):
		if x < 0 or x > 17:
			return False
		if y < 0  or y > 17:
			return False
		return True
	
	def setAllAdj(self):
		if self.checkBound(self.x-1,self.y):
			self.allAdj.add(str(self.x-1)+" "+str(self.y))
		if self.checkBound(self.x, self.y-1):
			self.allAdj.add(str(self.x)+" "+str(self.y-1))
		if self.checkBound(self.x+1,self.y):
			self.allAdj.add(str(self.x+1)+" "+str(self.y))
		if self.checkBound(self.x,self.y+1):
			self.allAdj.add(str(self.x)+" "+str(self.y+1))
			
	def addPosAdj(self, node):
		self.posAdj.append(node)
		if node.x > self.x:
			self.right = node
		elif node.x < self.x:
			self.left = node
		elif node.y > self.y:
			self.down = node
		elif node.y < self.y:
			self.up = node
	
	def getPosAdj(self):
		return self.posAdj
	
	def getPosAdjList(self):
		out = list()
		for i in self.posAdj:
			out.append(i.getAsList())
		return out
	
	def getAllAdj(self):
		return self.allAdj
		
	
	def getAsList(self):
		return [self.x,self.y]
	
	def getAsString(self):
		return str(self.x)+" "+str(self.y)
	
class Grid:
	def initGrid(self):
		for i in range(0,self.x):
			self.grid.append(list())
			for ii in range(0,self.y):
				self.grid[i].append(Node(i,ii))
				
	def dic(self):
		inp = dict()
		for i in range(0,self.x):
			for ii in range(0, self.y):
				key = self.grid[i][ii].getAsString()
				inp[key] = self.grid[i][ii].getAllAdj()
				
		return self.dfs(inp,"0 0")
		
	def dfs(self, graph, start):
		visited, stack = set(), [start]
		seq = list()
		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				visited.add(vertex)
				stack.extend(graph[vertex] - visited)
				seq.append(vertex)
		
		return seq
	def setPosAdj(self,seq):

		for i in range(0,len(seq)):
			a = self.strToNum(seq[i])
			if i == len(seq)-1:
				break
			b = self.strToNum(seq[i+1])
			self.grid[a[0]][a[1]].addPosAdj(self.grid[b[0]][b[1]])
			self.grid[b[0]][b[1]].addPosAdj(self.grid[a[0]][a[1]])
		
	def strToNum(self, s):
		a,b = s.split(" ")
		a = int(a)
		b = int(b)
		return[a,b]
		
	def __init__(self):
		self.x = 18
		self.y = 18
		self.grid = list()
		self.initGrid()
		self.setPosAdj(self.dic())


class mazeDraw(wx.Panel):
	def __init__(self,w):
		super().__init__(w, size = (360,360), pos = (0,20))
		self.setup()
		
	def setup(self):
		self.grid = Grid()
		self.graph = list()
		self.cur = [0,0]
		self.form()
	def form(self):
		
		for i in range(0,18):
			self.graph.append(list())	
			for ii in range(0,18):
				tmp = nodeDraw(i,ii,self)
				self.graph[i].append(tmp)
				

		for c in range(0,len(self.grid.grid)):
			for cc in range(0,len(self.grid.grid[c])):
				if isinstance(self.grid.grid[c][cc].left, Node) == True:
					self.graph[c][cc].left.SetBackgroundColour((255,255,0))
					self.graph[c-1][cc].right.SetBackgroundColour((255,255,0))
					if self.grid.grid[c-1][cc] not in self.grid.grid[c][cc].getPosAdj():
						self.grid.grid[c-1][cc].addPosAdj(self.grid.grid[c][cc])
						self.grid.grid[c][cc].addPosAdj(self.grid.grid[c-1][cc])
						
				if isinstance(self.grid.grid[c][cc].right, Node) == True:
					self.graph[c][cc].right.SetBackgroundColour((255,255,0))
					self.graph[c+1][cc].left.SetBackgroundColour((255,255,0))
					if self.grid.grid[c+1][cc] not in self.grid.grid[c][cc].getPosAdj():
						self.grid.grid[c+1][cc].addPosAdj(self.grid.grid[c][cc])
						self.grid.grid[c][cc].addPosAdj(self.grid.grid[c+1][cc])
					
				if isinstance(self.grid.grid[c][cc].up, Node) == True:
					self.graph[c][cc].up.SetBackgroundColour((255,255,0))
					self.graph[c][cc-1].down.SetBackgroundColour((255,255,0))
					if self.grid.grid[c][cc-1] not in self.grid.grid[c][cc].getPosAdj():
						self.grid.grid[c][cc-1].addPosAdj(self.grid.grid[c][cc])
						self.grid.grid[c][cc].addPosAdj(self.grid.grid[c][cc-1])
						
				if isinstance(self.grid.grid[c][cc].down, Node) == True:
					self.graph[c][cc].down.SetBackgroundColour((255,255,0))
					self.graph[c][cc+1].up.SetBackgroundColour((255,255,0))
					if self.grid.grid[c][cc+1] not in self.grid.grid[c][cc].getPosAdj():
						self.grid.grid[c][cc+1].addPosAdj(self.grid.grid[c][cc])
						self.grid.grid[c][cc].addPosAdj(self.grid.grid[c][cc+1])
	
		self.draw(self.cur[0],self.cur[1])			
	
				
						
	def draw(self,x,y):
		self.graph[self.cur[0]][self.cur[1]].off()
		self.cur[0] = x
		self.cur[1] = y
		self.graph[self.cur[0]][self.cur[1]].on()	
		
		
class nodeDraw(wx.Panel):
	def __init__(self,x,y,pan):
		self.x = x
		self.y = y
		super().__init__(pan, size = (20,20), pos = (x*20,y*20))
		self.SetBackgroundColour((255,255,0))
		
		if self.x == 17 and self.y == 17:
			self.SetBackgroundColour((20,255,20))
		

		
		self.up = wx.Panel(self, size = (17,3), pos = (3,0))
		self.up.SetBackgroundColour((0,0,0))
		
		self.down = wx.Panel(self, size = (17,3), pos = (3,17))
		self.down.SetBackgroundColour((0,0,0))
		
		self.left = wx.Panel(self, size = (3,17), pos = (0,3))
		self.left.SetBackgroundColour((0,0,0))
		
		self.right = wx.Panel(self, size = (3,17), pos = (17,3))
		self.right.SetBackgroundColour((0,0,0))
		
		self.upRight = wx.Panel(self, size = (3,3), pos = (0,0))
		self.upRight.SetBackgroundColour((0,0,0))
		self.upLeft = wx.Panel(self, size = (3,3), pos = (0,17))
		self.upLeft.SetBackgroundColour((0,0,0))
		self.downRight = wx.Panel(self, size = (3,3), pos = (17,0))
		self.downRight.SetBackgroundColour((0,0,0))
		self.downLeft = wx.Panel(self, size = (3,3), pos = (17,17))
		self.downLeft.SetBackgroundColour((0,0,0))
		
	def on(self):
		self.SetBackgroundColour((120,0,120))
		self.Refresh()
	def off(self):
		self.SetBackgroundColour((255,255,0))
		self.Refresh()

class Game:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.md()
	def md(self):
		self.a = mazeDraw(window)
		self.a.Bind(wx.EVT_CHAR_HOOK, self.move)	
		
	def getPos(self):
		return [x,y]
	
	def checkEnd(self):
		if self.x == 17 and self.y == 17:
			return True
		else:
			 return False
		
	def move(self,key):
		if key.GetKeyCode() ==  68:
			if [self.x+1,self.y] in self.a.grid.grid[self.x][self.y].getPosAdjList():
				self.x+=1
				
				self.a.draw(self.x,self.y)
		if key.GetKeyCode() ==  65:
			if [self.x-1,self.y] in self.a.grid.grid[self.x][self.y].getPosAdjList():
				self.x-=1
				
				self.a.draw(self.x,self.y)
		if key.GetKeyCode() ==  83:
			if [self.x,self.y+1] in self.a.grid.grid[self.x][self.y].getPosAdjList():
				self.y+=1
				
				self.a.draw(self.x,self.y)
		if key.GetKeyCode() ==  87:
			if [self.x,self.y-1] in self.a.grid.grid[self.x][self.y].getPosAdjList():
				self.y-=1
			
				self.a.draw(self.x,self.y)	
		if self.checkEnd() == True:
			self.endGame()
	def endGame(self):
		self.endwin = wx.Frame(window,title = "Win", size = (225,80), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER) 
		restart = wx.Button(self.endwin, label = "New Game")
		stop = wx.Button(self.endwin,label = "Quit", pos = (120,0))
		restart.Bind(wx.EVT_BUTTON, self.restart)
		stop.Bind(wx.EVT_BUTTON, self.stopApp)
		self.endwin.Show(True)
	def stopApp(self,b):
		self.endwin.Close()
		window.Close()
	def restart(self,b):
		self.a.Destroy()
		self.md()
		self.x = 0
		self.y = 0
		self.endwin.Close()


app = wx.App() 
window = wx.Frame(None, title = "wxPython Frame", size = (380,420), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
sizer = wx.BoxSizer(wx.VERTICAL)
window.SetSizer(sizer)	
g = Game()
window.Show(True) 



app.MainLoop()
