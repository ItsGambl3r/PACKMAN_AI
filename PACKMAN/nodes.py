import pygame
from vector import Vector2
from constants import *
from hashMap import HashMap
class Node(object):
    # Constructor
    def __init__(self, x, y):
        self.__position = Vector2(x, y)
        self.__neighbors = HashMap(5)
        self.__neighbors.add_all([(UP, None), (DOWN, None), (LEFT, None), (RIGHT, None)])

    def get_position(self):
        return self.__position
    
    def get_neighbors(self):
        return self.__neighbors
    
    def set_position(self, position):
        self.__position = position

    def set_neighbors(self, neighbors):
        self.__neighbors = neighbors

    def render(self, screen):
        for neighbor in self.__neighbors.get_keys():
            if self.__neighbors.get(neighbor) != None:
                line_start = self.__position.asTuple()
                line_end = self.__neighbors.get(neighbor).get_position().asTuple()  
                pygame.draw.line(screen, Colors.WHITE, line_start, line_end, 1)
                pygame.draw.circle(screen, Colors.WHITE, line_end, 5)

class NodeGroup():
    def __init__(self):
        self.__node_list = []

    def setup_test_nodes(self):
        nodeA = Node(80 ,80)
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)
        nodeA.get_neighbors()[RIGHT] = nodeB
        nodeA.get_neighbors()[DOWN] = nodeC
        nodeB.get_neighbors()[LEFT] = nodeA
        nodeB.get_neighbors()[DOWN] = nodeD
        nodeC.get_neighbors()[UP] = nodeA
        nodeC.get_neighbors()[RIGHT] = nodeD
        nodeC.get_neighbors()[DOWN] = nodeF
        nodeD.get_neighbors()[UP] = nodeB
        nodeD.get_neighbors()[LEFT] = nodeC
        nodeD.get_neighbors()[RIGHT] = nodeE
        nodeE.get_neighbors()[LEFT] = nodeD
        nodeE.get_neighbors()[DOWN] = nodeG
        nodeF.get_neighbors()[UP] = nodeC
        nodeF.get_neighbors()[RIGHT] = nodeG
        nodeG.get_neighbors()[UP] = nodeE
        nodeG.get_neighbors()[LEFT] = nodeF
        self.nodeList = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    def render(self, screen):
        for node in self.__node_list:
            node.render(screen)