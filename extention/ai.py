"""
network.py
~~~~~~~~~~
A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network. Gradients are calculated
using backpropagation. Note that I have focused on making the code
simple , easily readable , and easily modifiable. It is not optimized ,
and omits many desirable features.
"""
#### Libraries
# Standard library
import random
import json
# Third -party libraries
import numpy as np

class network(object):

    def __init__(self, file= None, sizes= None):
        if file : # read network from documment
            file = json.load(file)

            self.sizes = file["sizes"]
            self.num_layers = len(self.sizes)
            self.biases = [np.asarray(array) for array in file["biases"]]
            self.weights = [np.asarray(array) for array in file["weights"]]

        else: # generate new network with random values using sizes
            self.num_layers = len(sizes)
            self.sizes = sizes
            self.biases = [np.random.randn(y) for y in sizes [1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(sizes [:-1], sizes [1:])]

        # values used for backpropagation
        self.activations = []
        self.zs = []

        self.nabla_b = [np.zeros(b.shape) for b in self.biases]
        self.nabla_w = [np.zeros(w.shape) for w in self.weights]
    
    def feedforward (self , a):
        """Return the output of the network if ‘‘a‘‘ is input."""
        
        activation = a
        activations = [a] # list to store all the activations , layer by layer
        zs = [] # list to store all the z vectors , layer by layer
        
        for b, w in zip(self.biases , self.weights):
            z = np.dot(w, activation )+b
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)
            
        return activation, activations, zs

    def calculateMove(self , inputs):
        """Calaculate the move to be done using feedforward"""
        
        result_final = 0
        activations_final = 0
        zs_final = 0
        move_num = 0


        for i in range(len(inputs)):
            result, activations, zs = self.feedforward(np.asarray(inputs[i]))
            if result > result_final:
                result_final = result
                activations_final = activations
                zs_final = zs
                move_num = i

        self.activations.append(activations_final)
        self.zs.append(zs_final)

        return move_num
    
    def update_prep(self, evaluation):
        """Alters nabla_w and nabla_b"""
        delta_nabla_b = [np.zeros(b.shape) for b in self.biases]
        delta_nabla_w = [np.zeros(w.shape) for w in self.weights]

        for i in range(len(self.activations)): #note the changes for weights and biases
            delta_nabla_b , delta_nabla_w = self.mybackprop([evaluation], i)  # gradient descent

            self.nabla_b = [(nb / len(self.activations)) +dnb for nb , dnb in zip(self.nabla_b , delta_nabla_b )]
            self.nabla_w = [(nw / len(self.activations)) +dnw for nw , dnw in zip(self.nabla_w , delta_nabla_w )]
    
    def update (self, amount= 1, eta= 10):
        """Applies nabla_w and nabla_b"""
        self.weights = [w- (eta / amount) *nw
            for w, nw in zip(self.weights , self.nabla_w)]
        self.biases = [b- (eta / amount) *nb
            for b, nb in zip(self.biases , self.nabla_b)]
    
    def mybackprop(self, y, iterator):
        """Return a tuple ‘‘(nabla_b , nabla_w)‘‘ representing the
        gradient for the cost function C_x. ‘‘nabla_b ‘‘ and
        ‘‘nabla_w ‘‘ are layer -by-layer lists of numpy arrays , similar
        to ‘‘self.biases ‘‘ and ‘‘self.weights ‘‘."""
        
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        
        
        # backward pass
        delta = self. cost_derivative (self.activations[iterator] [-1], y) * self.sigmoid_prime (self.zs[iterator] [ -1])
        nabla_b [-1] = delta
        nabla_w [-1] = CoolVectorMultiply(delta, self.activations[iterator] [-2])
        
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book. Here ,
        # l = 1 means the last layer of neurons , l = 2 is the
        # second -last layer , and so on. It’s a renumbering of the
        # scheme in the book , used here to take advantage of the fact
        # that Python can use negative indices in lists.
        
        for l in range(2, self. num_layers ):
            z = self.zs[iterator] [-l]
            sp = self.sigmoid_prime (z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = CoolVectorMultiply(delta, self.activations[iterator] [-l -1])
        
        return (nabla_b , nabla_w)
    
    def cost_derivative (self , output_activations , y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        
        return ( output_activations -y)
    
    
    #### Miscellaneous functions
    
    def sigmoid(self, z):
        """The sigmoid function."""
        
        return 1.0/(1.0 + np.exp(-z))
    
    def sigmoid_prime (self, z):
        """Derivative of the sigmoid function."""
        
        return self.sigmoid(z)*(1- self.sigmoid(z))

def VectorTranspose(vector):
    vector = [[val] for val in vector]
    return vector

def CoolVectorMultiply(a, b):
    """Vector shit von numpy ist stupid, das hier nicht"""
    result = [[ax * bx for bx in b] for ax in a]
    return result