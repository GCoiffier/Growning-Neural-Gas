import pygame
from . import constants as cst
from . import neurons as nr
from random import randint

class NeuralGas:

	def __init__(self,datas,parameters):
		"""
		A neural gas is given a set of data vectors (here in 2D space) and
		some parameters defined in GNG.py
		The gas is initialized with two independent neurons and no edges
		"""
		pygame.init()
		nb_iter_max = 10*1000

		self.f = pygame.font.SysFont("arial",20)
		self.datas = datas
		self.parameters = parameters

		self.neurons = set()
		# initialized with 2 independent nodes
		self.neurons.add(nr.Neuron(list(datas[0])))
		self.neurons.add(nr.Neuron(list(datas[1])))

		self.edges = set()

		self.show_data = True
		self.show_gas = True
		self.show_stats = True

		self.f = pygame.font.SysFont("arial",20)
		pygame.display.set_caption("Neural Network")
		pygame.display.set_mode((cst.WIDTH,cst.HEIGHT))


	def get_sample(self):
		return self.datas[randint(0,len(self.datas)-1)]

	def get_two_nearest_nodes(self,pt):
		m1,m2 = None, None
		p1,p2 = None, None
		for node in self.neurons:
			if m2 is None :
				if m1 is None :
					m1 = node.distance_from_point(pt)
					p1 = node
				else :
					m2 = node.distance_from_point(pt)
					p2 = node
			d = node.distance_from_point(pt)
			if d<=m1 :
				m2 = m1
				p2 = p1
				m1 = d
				p1 = node
			elif m1<d<=m2 :
				m2 = d
				p2 = node
		return p1,p2

	def update(self,current_iteration):
		"""
		runs one iteration of the GNG algorithm
		"""
		# Step 1 : get a sample and its two closest nodes
		s = self.get_sample()
		na,nb = self.get_two_nearest_nodes(s)

		# Step 2 : update na's error
		na.error += na.distance_from_point(s)

		# Step 3 : update na's position as well as its neightbours' position
		na.pos[0] += self.parameters["eps_b"]*(s[0]-na.pos[0])
		na.pos[1] += self.parameters["eps_b"]*(s[1]-na.pos[1])

		for x in na.neightbours :
			x.pos[0] += self.parameters["eps_n"]*(s[0]-x.pos[0])
			x.pos[1] += self.parameters["eps_n"]*(s[1]-x.pos[1])

		# Step 4 : increase edge's age between na and its neightbours
		for e in na.edge_neightbours :
			e.age +=1

		# Step 5 : create an edge between na and nb. If such edge already exists, reset its age
		e = na.find_edge_of_extremity(nb)
		if e is None :
			e = nr.Edge(na,nb)
			na.edge_neightbours.append(e)
			na.neightbours.append(nb)
			nb.edge_neightbours.append(e)
			nb.neightbours.append(na)
			self.edges.add(e)
		else :
			e.age = 0

		# Step 6 : for all incident edge of na, if age > age_max, delete the edge, and delete
		#          any isolated node created
		for e in na.edge_neightbours:
			if e.age > self.parameters["age_max"] :
				if na == e.extr1 :
					other_end = e.extr2
				else :
					other_end = e.extr1
				na.edge_neightbours.remove(e)
				na.neightbours.remove(other_end)
				other_end.edge_neightbours.remove(e)
				other_end.neightbours.remove(na)
				if len(other_end.neightbours) == 0 :
					self.neurons.remove(other_end)
				if len(na.neightbours) == 0 :
					self.neurons.remove(na)
				self.edges.remove(e)

		# Step 7 : eventually create a new vertice
			if current_iteration%self.parameters["lambda"] == 0 :
				# 7.1 : find the node u with the largest error
				m,u = None,None
				for x in self.neurons :
						m = x.error
						u = x

				# 7.2 : find the node v, neightbour of u, with the largest error
				m,v = None,None
				for x in u.neightbours :
					if m is None or m<x.error :
						m = x.error
						v = x

				# 7.3 :	disconnect u and v
				e = u.find_edge_of_extremity(v)
				try :
					self.edges.remove(e)
					u.edge_neightbours.remove(e)
					u.neightbours.remove(v)
					v.edge_neightbours.remove(e)
					v.neightbours.remove(u)
				except :
					print("edge.remove : no such edge")
					
				# 7.4 : create a new node r between u and v
				r = nr.Neuron([ (u.pos[0]+v.pos[0])/2 , (u.pos[1]+v.pos[1])/2])
				self.neurons.add(r)

				# 7.5 : connect u and r, and v and r
				e_ur = nr.Edge(u,r)
				e_vr = nr.Edge(v,r)
				self.edges.add(e_ur)
				self.edges.add(e_vr)
				u.neightbours.append(r)
				v.neightbours.append(r)
				r.neightbours = [u,v]

				r.edge_neightbours = [e_ur, e_vr]
				u.edge_neightbours.append(e_ur)
				v.edge_neightbours.append(e_vr)

				# 7.6 : ajust error of u and v
				u.error *= self.parameters["alpha"]
				v.error *= self.parameters["alpha"]

		# Step 8 : multiply every error by 1-beta
		for node in self.neurons :
			node.error *= (1-self.parameters["beta"])
		# Done !
		return


	def display_gas(self,bliton):
		""" Puts the neural gas on screen """
		for e in self.edges :
			e.display(bliton)

	def display_data(self,bliton):
		""" Puts original data points on screen """
		for (x,y) in self.datas :
			pygame.draw.circle(bliton, pygame.Color("red"), (x,y), 2, 0)

	def display_stats(self,bliton,i):
		x = self.f.render("Current iteration : " + str(i), True, pygame.Color("green"))
		x_rect = x.get_rect()
		x_rect.topright = (cst.WIDTH,0)
		bliton.blit(x, x_rect)

	def run(self, animated = False):
		screen = pygame.display.get_surface()
		clock = pygame.time.Clock()
		i = 0

		while True :
			clock.tick(60)

			# 1\ Handling windows events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_a :
					self.show_data = not self.show_data
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_z :
					self.show_gas = not self.show_gas
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_e :
					self.show_stats = not self.show_stats

	        # 2\ Updating network
			if i< cst.ITER_MAX :
				self.update(i)
				i+=1
			elif i == cst.ITER_MAX :
				print("Done")
				i+=1

	       	# 3\ Display
			if not animated and i%1000 == 1 :
				print(i)

			if animated or i>cst.ITER_MAX :
				screen.fill(pygame.Color("black"))
				if self.show_data :
					self.display_data(screen)
				if self.show_gas :
					self.display_gas(screen)
				if self.show_stats :
					self.display_stats(screen,i)
			pygame.display.flip()
