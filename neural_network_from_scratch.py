# -*- coding: utf-8 -*-
"""Neural_Network_From_Scratch.ipynb

Automatically generated by Colaboratory.
"""

import random
import math

def activation_tanh(x):
  numerator = math.exp(2*x) - 1
  denominator = math.exp(2*x) + 1
  out = numerator/denominator
  return out

def transpose(matrix):
  rows = len(matrix)
  columns =len(matrix[0])
  transposed = [[0 for _ in range(rows)] for _ in range(columns)]
  for j in range(rows):
    for i in range(columns):
      transposed[i][j] = matrix[j][i]
  return transposed

def forward(inputs, hidden_weights, output_weights, hidden_biases, output_bias):
    hidden_outputs = []
    hidden_weights = transpose(hidden_weights)

    for sample in inputs:
        hidden_input_for_sample = []
        for neuron_weights, bias in zip(hidden_weights, hidden_biases):
            input_sum = sum(feature * weight for feature, weight in zip(sample, neuron_weights))
            input_sum += bias
            hidden_input_for_sample.append(activation_tanh(input_sum))
        hidden_outputs.append(hidden_input_for_sample)

    final_outputs = []
    for sample_hidden_outputs in hidden_outputs:
        output_sum = sum(hidden_output * weight for hidden_output, weight in zip(sample_hidden_outputs, output_weights))
        output_sum += output_bias
        final_outputs.append(activation_tanh(output_sum))

    return final_outputs, hidden_outputs



def loss(y_pred, y_target):
  sum_loss = 0
  for i in range(len(y_pred)):
    sum_loss += (y_target[i] - y_pred[i])**2
  mean_loss = sum_loss/len(y_target)
  return mean_loss


def backward(y_pred, y_true, inputs, hidden_outputs, hidden_weights, output_weights, hidden_biases, output_bias):
    grad_loss_output = [-(y_true_i - y_pred_i) for y_true_i, y_pred_i in zip(y_true, y_pred)]
    grad_tanh_output = [(1 - y_pred_i ** 2) for y_pred_i in y_pred]

    grad_output_weights = [sum(grad_loss_output[i] * grad_tanh_output[i] * hidden_output[j] for i, hidden_output in enumerate(hidden_outputs)) for j in range(len(output_weights))]
    grad_output_bias = sum(grad_loss_output[i] * grad_tanh_output[i] for i in range(len(y_pred)))

    grad_hidden_weights = [[0 for _ in range(neurons_input)] for _ in range(neurons_hidden)]
    grad_hidden_biases = [0 for _ in range(neurons_hidden)]

    for i in range(len(inputs)):
        for j in range(neurons_hidden):
            grad_tanh_hidden = 1 - hidden_outputs[i][j] ** 2
            for k in range(neurons_input):
                grad_hidden_weights[j][k] += grad_loss_output[i] * output_weights[j] * grad_tanh_hidden * inputs[i][k]
            grad_hidden_biases[j] += grad_loss_output[i] * output_weights[j] * grad_tanh_hidden

    grad_hidden_weights = [[weight / len(inputs) for weight in neuron_weights] for neuron_weights in grad_hidden_weights]
    grad_hidden_biases = [bias / len(inputs) for bias in grad_hidden_biases]
    grad_output_weights = [grad / len(inputs) for grad in grad_output_weights]
    grad_output_bias /= len(inputs)

    return grad_hidden_weights, grad_output_weights, grad_hidden_biases, grad_output_bias

def update_parameters(hidden_weights, output_weights, hidden_biases, output_bias, grad_hidden_weights, grad_output_weights, grad_hidden_biases, grad_output_bias, learning_rate):
    for i in range(neurons_hidden):
        for j in range(neurons_input):
            hidden_weights[i][j] -= learning_rate * grad_hidden_weights[i][j]
        hidden_biases[i] -= learning_rate * grad_hidden_biases[i]

    for i in range(neurons_hidden):
        output_weights[i] -= learning_rate * grad_output_weights[i]
    output_bias -= learning_rate * grad_output_bias

    return hidden_weights, output_weights, hidden_biases, output_bias

from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np

iris = datasets.load_iris()

X = iris.data[:, :3]  # Select only the first three features
y = iris.target
y = np.where(y == 0, 1.0, -1.0)

inputs,X_test,y_true,y_test = train_test_split(X,y,test_size=0.1,random_state=1)

num_features = len(inputs[0])
neurons_input = 3
neurons_hidden = 3
neurons_output = 1
# random.seed(1)
# Initialize the weights and biases randomly
hidden_weights = [[random.normalvariate(0, 0.5) for _ in range(neurons_input)] for _ in range(neurons_hidden)]
output_weights = [random.normalvariate(0, 0.5) for _ in range(neurons_hidden)]
hidden_biases = [random.normalvariate(0, 1) for _ in range(neurons_hidden)]
output_bias = random.normalvariate(0, 1)

num_epochs = 1000  # The number of iterations to train the network
learning_rate = 0.3  # The step size for updating the weights

# Training loop
for epoch in range(num_epochs):
    # Forward pass: compute predicted y by passing x to the model
    y_pred, hidden_outputs = forward(inputs, hidden_weights, output_weights, hidden_biases, output_bias)

    # Compute and print loss
    current_loss = loss(y_pred, y_true)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {current_loss}")

    # Backward pass: compute gradient of the loss with respect to model parameters
    grad_hidden_weights, grad_output_weights, grad_hidden_biases, grad_output_bias = backward(
        y_pred, y_true, inputs, hidden_outputs, hidden_weights, output_weights, hidden_biases, output_bias
    )

    # Update weights and biases
    hidden_weights, output_weights, hidden_biases, output_bias = update_parameters(
        hidden_weights, output_weights, hidden_biases, output_bias, grad_hidden_weights, grad_output_weights, grad_hidden_biases, grad_output_bias, learning_rate
    )

print(y_pred)

y_test_pred, _= forward(X_test, hidden_weights, output_weights, hidden_biases, output_bias)
print(loss(y_test_pred,y_test))

def calculate_accuracy(y_target, y_pred):
    # Assuming y_pred are the predicted class labels from your model and y_true are the actual labels
    correct_predictions = sum(y_pred_i == y_target_i for y_pred_i, y_target_i in zip(y_pred, y_target))
    accuracy = correct_predictions / len(y_target)
    return accuracy

y_pred_binary = [1.0 if pred > 0 else -1.0 for pred in y_pred]
y_test_pred_binary = [1.0 if pred > 0 else -1.0 for pred in y_test_pred]

train_accuracy = calculate_accuracy(y_true,y_pred_binary)
test_accuracy = calculate_accuracy(y_test,y_test_pred_binary)
print(f"Train Accuracy: {train_accuracy * 100}")
print(f"Test Accuracy: {test_accuracy * 100}")

# import pickle

# # Save the model parameters to a file
# with open('my_neural_network.pkl', 'wb') as file:
#     pickle.dump({
#         'hidden_weights': hidden_weights,
#         'output_weights': output_weights,
#         'hidden_biases': hidden_biases,
#         'output_bias': output_bias
#     }, file)

# print("Model saved successfully!")

# import pickle

# with open('my_neural_network.pkl', 'rb') as file:  #To Load the model
#     model_params = pickle.load(file)

# hidden_weights = model_params['hidden_weights']
# output_weights = model_params['output_weights']
# hidden_biases = model_params['hidden_biases']
# output_bias = model_params['output_bias']

# print("Model loaded successfully!")

