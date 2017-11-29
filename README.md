# uTensor-CLI

## Introduction

  uTensor is an extremely light-weight Deep-Learning Inference framework built on mbed and Tensorflow. uTensor-cli translates your `.proto` files into models which can be imported into existing mbed projects.

  This project is under going constant development.

## Requirement
- [Python](https://www.python.org/)
- [Mbed CLI](https://github.com/ARMmbed/mbed-cli)
- [Tensorflow](https://www.tensorflow.org/install/)
- Mbed-os 5.6+ compatible [boards](https://os.mbed.com/platforms/?mbed-os=25) with at least 256kb of RAM
- SD Card (Must be LESS than 32 GB)
- SD Card reader for the board (Optional if built into the board)

## Finding your target name

`mbed detect` to see which target is connect to the board

`mbedls -l` to list all supported targets

## Using uTensor-cli

```
python utensor/utensor.py graph_out/quantized_graph.pb
```

## Example program

### Linear Regression Example
A linear regression learning algorithm example using TensorFlow library.
- Modified version of code by Aymeric Damien

```python
import tensorflow as tf
import numpy
import matplotlib.pyplot as plt
rng = numpy.random


# Parameters
learning_rate = 0.01
training_epochs = 1000
display_step = 50

# Training Data
train_X = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1])
train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
                         2.827,3.465,1.65,2.904,2.42,2.94,1.3])
n_samples = train_X.shape[0]

# tf Graph Input
X = tf.placeholder("float")
Y = tf.placeholder("float")

# Set model weights
W = tf.Variable(rng.randn(), name="weight")
b = tf.Variable(rng.randn(), name="bias")

# Construct a linear model
pred = tf.add(tf.multiply(X, W), b, name="pred")

saver = tf.train.Saver()

# Mean squared error
cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
print(cost.name)
# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training
sess = tf.Session()
sess.run(init)

# Fit all training data
for epoch in range(training_epochs):
    for (x, y) in zip(train_X, train_Y):
        sess.run(optimizer, feed_dict={X: x, Y: y})

    #Display logs per epoch step
    if (epoch+1) % display_step == 0:
        c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
        print "Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c),             "W=", sess.run(W), "b=", sess.run(b)

print "Optimization Finished!"
training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
print "Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n'


input_graph_def = sess.graph.as_graph_def()


### Decide which ouputs to dump

output_node_names = "pred,%s" % cost.op.name
print("Outputs requested:", output_node_names.split(","))
#output_node_names = "pred"


### Freeze Graph

output_graph_def = tf.graph_util.convert_variables_to_constants(
            sess, # The session
            input_graph_def, # input_graph_def is useful for retrieving the nodes
            output_node_names.split(",")
)

output_graph="lin_reg_model.pb"
with tf.gfile.GFile(output_graph, "wb") as f:
    f.write(output_graph_def.SerializeToString())


sess.close()

```

