# ping_pomdp
Making a POMDP model learn to play Pong. 

## Introduction 
Recently, [Kagan et al. (2022)][kagan2022] demonstrated that in vitro neurons can learn and exhibit sentience when embodied in a simulated game-world receiving only sensory, predictable, and unpredictable feedback. They used a high-density electrode grid to interface the neurons with a Pong game, where the neurons could control the paddle and receive feedback from the game. The results showed that the neurons adapted their activity to maximize the score and avoid losing. The following image shows a conceptual model of the paper.

![Kagan2022_conceptual][img:kagan22_conceptual]

This study inspired me to pursue a similar project, but using a computational model of active inference instead of in vitro neurons. My goal is to develop a computational structure to interface an active inference model with a Pong game, and compare its performance and behavior with the results of [Kagan et al. (2022)][kagan2022]. I also hope that this project can serve as a first step towards building computational infrastructure around this interface to compare different models and environments between themselves, and possibly map them to in vitro experiments with neuron cultures.

## Modeling

## Interface used by [Kagan et al. (2022)][kagan2022]:

![kagan22_interface][img:kagan22_electrode_layout]

This image shows the schematics of the experiment. A culture of neurons grown over an high density electrode grid following the layout above.

Inspired by the [DishBrain][dish_brain]'s Electrode Layout Schematic, this project will implement the following interface between a Pong implementation and a pymdp agent. 


## My model 
![pingPOMDP_interface][img:brito23_interface]



[kagan2022]: https://linkinghub.elsevier.com/retrieve/pii/S0896627322008066

[img:kagan22_conceptual]: docs/kagan22_conceptual_model.jpg
[img:kagan22_interface]: docs/kagan22_interface.jpg
[img:brito23_interface]: docs/brito23_interface.png

