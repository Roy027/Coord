### Huge thanks to https://realpython.com/python-ai-neural-network/
# One of the tutorials, unlike others, that does not skip concepts, ...
# ...does not assume things, and explains things well.
# Other useful resources:
# https://www.samsonzhang.com/2020/11/24/understanding-the-math-behind-neural-networks-by-building-one-from-scratch-no-tf-keras-just-numpy.html
# https://scikit-learn.org/stable/modules/neural_networks_supervised.html 

# Seems that pandas module require a few other modules installed
# Such as xlrd module and openpyxl module
import pandas
import numpy
import os
import random
import math
import sys
import matplotlib.pyplot as plt
import threading

# Remove row/column display limit in order to visualise all data
# So that everything can be seen and verified for troubleshooting
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
numpy.set_printoptions(threshold=sys.maxsize)

# Converts the relative directory of training data file into an absolute directory
# An absolute directory is required as an imput in the pandas.read_excel function
directory = os.path.dirname(__file__)
datafile = os.path.join(directory, r'.\trainingdata.xlsx')

# Read excel file and assign the data to a variable
# iloc function numerically locates [rownumbers,columnnumbers], numpy.r_[] concatenates arrays of rows
# x:y , where it is inclusive of x, but exclusive of y
test_sheet = pandas.read_excel (datafile, sheet_name='CN4_table_all_cat_9767')
ideal_sheet = pandas.read_excel (datafile, sheet_name='All-model')

# Here is a commented out code to check the enumeration of columns
# col_mapping = [f"{c[0]}:{c[1]}" for c in enumerate(test_sheet.columns)]
# print(col_mapping)

################################### Set learning rate and iteration here
Lrate = 0.01    # TBC; can learning rate be different for all the different parameters?
iteration = 10000

# Depending on how the data is formatted in excel
# The column numbers listed here may be different
# Dimensions are always in no. of rows X no. of columns format
idealset = ideal_sheet.iloc[:,numpy.r_[9:21,22:39]]
idealresult = ideal_sheet.iloc[:,21]
testdata = test_sheet.iloc[:,numpy.r_[9:21,22:39]]
testlabel = test_sheet.iloc[:,1]

# Convert DataStructure into numpy array for computing purposes
# idealdata dimensions: 3780 x 29
# idealitems dimensions: 3780 rows (x 1 column)
# testset dimensions: 9767 x 29
idealdata = idealset.to_numpy()
idealitems = idealresult.to_numpy()
testset = testdata.to_numpy()
# Convert elements in idealitems into numerical labels
idealitems[idealitems == 'T-4'] = 0
idealitems[idealitems == 'SP-4'] = 1
idealitems[idealitems == 'SPY-4'] = 2
idealitems[idealitems == 'SS-4'] = 3

n_parameters = testset.shape[1]

class NeuralNetwork:
    def __init__(self, learning_rate):
        # Difference between numpy.random.rand(n_parameters) and numpy.random.rand(n_parameters, 1)
        # is that the former creates a n_parameters x 1 array containing floats
        # and the latter creates a n_parameters x 1 array containing ARRAYS CONTAINING FLOATS
        # WHICH WILL CAUSE ERRORS in the long run.
        self.weights_1 = numpy.random.rand(n_parameters)
        self.bias = numpy.random.randn()
        self.learning_rate = learning_rate

    def _sigmoid(self, x):
        return 1 / (1 + numpy.exp(-1 * x))

    def _sigmoid_deriv(self, x):
        return self._sigmoid(x) * (1 - self._sigmoid(x))

    # main function that you want to call
    # i.e. NeuralNetwork.predict(input_vector)
    # Check that the predict function is the same as...
    # ...the first part of compute gradients function
    def predict(self, input_vector):
        layer_1 = numpy.dot(input_vector, self.weights_1) + self.bias
        layer_2 = self._sigmoid(layer_1)
        prediction = layer_2
        return prediction

    # Compute the gradients to be subtracted from the weights and biases values respectively
    # Chain rule (from algebra differentiation things) is required.
    def _compute_gradients(self, input_vector, target, index):
        # [LAYER1] parameters * weights1 + bias = <layer 1 output>
        # [LAYER2] weights2*sigmoid(layer1) = <layer 2 output>
        # [LAYER3] weights3*sigmoid(layer2) = <layer 3 output>
        # [LAYER4] weights4*sigmoid(layer3) = <layer 4 output>
        # [LAYER5] weights5*sigmoid(layer4) = <layer 5 output>
        layer_1 = numpy.dot(input_vector, self.weights_1[index]) + self.bias
        layer_2 = self._sigmoid(layer_1)
        prediction = layer_2

        # [Error function] = sumof ((prediction - target)^2)
        # Target derivative: derivative of 
        derror_dprediction = 2 * (prediction - target)
        dprediction_dlayer1 = self._sigmoid_deriv(layer_1)
        dlayer1_dbias = 1
        dlayer1_dweights_1 = (0 * self.weights_1[index]) + (1 * input_vector)

        derror_dbias = (
            derror_dprediction * dprediction_dlayer1 * dlayer1_dbias
        )
        derror_dweights_1 = (
            derror_dprediction * dprediction_dlayer1 * dlayer1_dweights_1
        )
        return derror_dbias, derror_dweights_1

    # Update the bias and weights for each parameter
    # Since there exists 29(+-) parameters
    # It's important to update them one by one...
    # ...and not use the same number to update every element in the...
    # ...bias and weights arrays.
    # Edit: bias is a float value!
    def _update_parameters(self, derror_dbias, derror_dweights_1):
        self.bias = self.bias - (derror_dbias * self.learning_rate)
        self.weights_1 = self.weights_1 - (derror_dweights_1 * self.learning_rate)
        print("Bias is now " + str(self.bias))
        print("Weights is now " + str(self.weights_1))
    
    def train(self, input_vectors, targets, iterations):
        cumulative_errors = []
        for current_iteration in range(iteration):
            print("Training iteration number #" + str(current_iteration) + " of " + str(iteration))
            # Pick a data instance at random.
            # I.e. pick a .cif file containing all the stats details in an array
            random_data_index = numpy.random.randint(len(input_vectors))
            input_vector = input_vectors[random_data_index]
            target = targets[random_data_index]

            # Compute the gradients and update the weights, for each parameter in a .cif file
            # Creates array that stores the weights derivatives
            dweights_1_array = numpy.zeros(len(input_vector))
            for ind, element in enumerate(input_vector):
                derror_dbias, derror_dweights_1 = self._compute_gradients(
                    input_vector[ind], target, ind
                )
                dweights_1_array[ind] = derror_dweights_1

            self._update_parameters(derror_dbias, dweights_1_array)

            # Measure the cumulative error for all the instances
            if current_iteration % 100 == 0:
                cumulative_error = 0
                # Loop through all the instances to measure the error
                for data_instance_index in range(len(input_vectors)):
                    data_point = input_vectors[data_instance_index]
                    target = targets[data_instance_index]

                    prediction = self.predict(data_point)
                    error = numpy.square(prediction - target)

                    cumulative_error = cumulative_error + error
                cumulative_errors.append(cumulative_error)
        return cumulative_errors

neural_network = NeuralNetwork(Lrate)
trainingerror = neural_network.train(idealdata, idealitems, iteration)
print(trainingerror)
plt.plot(trainingerror)
plt.savefig("trainingerror.png")
predicted = neural_network.predict(testset)
results = numpy.array([testlabel, predicted])
# Convert elements in predicted back into string results
# To be implemented only after neuralnetwork test is successful
# predicted[predicted == 0] = 'T-4'
# predicted[predicted == 1] = 'SP-4'
# predicted[predicted == 2] = 'SPY-4'
# predicted[predicted == 3] = 'SS-4'
print(numpy.transpose(results))
#print(predicted)
#print(len(predicted))