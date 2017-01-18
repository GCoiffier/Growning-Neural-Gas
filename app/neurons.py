from random import randint
import pygame
from . import constants as cst

class Neuron:

    def __init__(self,pos):
        """
        A neuron is a node of the graph.
        - Pos is its position into the 2D space.
        - Neightbours is the list of its neightbours
        - Edge_neightbours is the list of the edges of the graph which
        has one extremity in self.
        """
        self.pos = pos
        self.neightbours = []
        self.edge_neightbours = []
        self.error = 0

    def distance_from_point(self,pt):
    	return (self.pos[0]-pt[0])*(self.pos[0]-pt[0])+(self.pos[1]-pt[1])*(self.pos[1]-pt[1])

    def find_edge_of_extremity(self,other):
        """
        Find the edge that links self to other (other should be a neightbours of self)
        """
        for e in self.edge_neightbours :
            if e.extr1 == self and e.extr2 == other :
                return e
            elif e.extr1 == other and e.extr2 == self :
                return e
        return None

class Edge:

    def __init__(self,extr1,extr2):

        self.extr1 = extr1
        self.extr2 = extr2
        self.age = 0

    def display(self,bliton):
        pygame.draw.line(bliton, pygame.Color("white"), self.extr1.pos, self.extr2.pos, 1)
