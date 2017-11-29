# Design Notes

## Goals
1. Users should be able to have more than one inference model per program
1. Model interface should be consistent
1. Model should adapt to more than one input
1. Model interface should be importable as a libary and thus reusable
1. User should have control of memory, i.e. when/where model is constructed
1. Code generation should be simple and seamless but configurable

## High level generation
Currently, the generation tools take in a protobuf file and produce a header file and corresponding cpp file with the same name. For example `my_model.pb` generates `my_model.cpp` and `my_model.hpp`. 
`my_model.hpp` provides a simple `Model` interface class that makes inference as easy as constructing an object and calling `predict_proba`. Each model gets a unique namespace based on the model name, this lets users have multiple models in their programs. 

```cpp
my_model::Model model();
...
result = model.predict_proba(input1);
```
