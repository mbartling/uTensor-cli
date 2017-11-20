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
