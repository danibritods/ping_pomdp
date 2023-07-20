# ping_pomdp
Making a POMDP model learn to play Pong. This is my final project to obtain the degree of Bachelor in Computer Science. 
You can read my [monogaph draft][monograph] and see its [(PT-BR) presentation][presentation]. 

## Introduction 
Recently, [Kagan et al. (2022)][kagan2022] demonstrated that in vitro neurons can learn and exhibit sentience when embodied in a simulated game-world receiving only sensory, predictable, and unpredictable feedback. They used a high-density electrode grid to interface the neurons with a Pong game, where the neurons could control the paddle and receive feedback from the game. The results showed that the neurons adapted their activity to maximize the score and avoid losing. The following image shows a conceptual model of the paper.

![Kagan2022_graphical_abstract][img:kagan22_abstract]

This study inspired me to pursue a similar project, but using a computational model of active inference instead of in vitro neurons. My goal is to develop a computational structure to interface an active inference model with a Pong game, and compare its performance and behavior with the results of [Kagan et al. (2022)][kagan2022]. I also hope that this project can serve as a first step towards building computational infrastructure around this interface to compare different models and environments between themselves, and possibly map them to in vitro experiments with neuron cultures.

## Modeling

## Interface used by [Kagan et al. (2022)][kagan2022]:

![kagan22_interface][img:kagan22_electrode_layout]



## My model 
![pingPOMDP_interface][img:brito23_interface]



[monograph]: docs/PingPOMDP.pdf
[kagan2022]: https://linkinghub.elsevier.com/retrieve/pii/S0896627322008066
[img:kagan22_conceptual]: docs/kagan22_conceptual_model.jpg
[monograph]: docs/PingPOMDP.pdf
[presentation]: https://docs.google.com/presentation/d/11nIBT0JyMc6adKcwV-77EfZQtfFBNM5DIv4i2dRdgFo/edit?usp=sharing
[img:kagan22_abstract]: docs/kagan22_graphical_abstract.jpg
[img:kagan22_electrode_layout]: docs/kagan22_electrode_layout.jpg
[img:brito23_interface]: docs/brito23_interface.png

