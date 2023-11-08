import numpy as np


def sigmoid(vector):
    return 1/(1+np.exp(-vector))


class Node:
    def __init__(self) -> None:
        self.weights = np.random.rand(9,3)
        self.bias = np.random.rand(9,1)
        self.activation = 0

def activationvector(nodes:list):
    return np.array([node.activation for node in nodes])

class TrainedAI:
    #9x3
    def __init__(self) -> None:
        self.nodes = [[Node() for col in range(3)] for row in range(9)]
        
    def calc(self,inputvector,layer):
        if layer == 1:

            for row in range(9):
                self.nodes[row][0].activation = sigmoid(inputvector[row])
                inputvector[row] = self.nodes[row][0].activation
            self.calc(inputvector,2)
        elif layer == 2:
            for row in range(9):
                self.nodes[row][1].activation = sigmoid(np.dot(self.nodes[row][0].weights,inputvector)+self.nodes[row][1].bias)
                inputvector[row] = self.nodes[row][1].activation
            self.calc(inputvector,3)
        elif layer == 3:
            for row in range(9):
                self.nodes[row][2].activation = sigmoid(np.dot(self.nodes[row][1].weights,inputvector)+self.nodes[row][2].bias)
                inputvector[row] = self.nodes[row][2].activation
            return inputvector


class SetAlgorithm:
    pass


class Human:
    pass
