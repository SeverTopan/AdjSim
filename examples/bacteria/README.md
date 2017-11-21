# Bacteria Simulation

This simulation illustrates the behaviour of a group of bacteria which exhibit agency, and static food.
Bacteria simply must move towards the food and consume it. Bacteria will starve if they run out of 
calories, and they have the ability to divide.

The agents are given a loss function coinciding with their calorie count. Moving, dividing, and inaction all lower calorie count, while eating raises it. Bacteria learn optimal behaviour byt choosing the set of actions which mazimize their calorie count.

Below we can see the difference that learning makes. On the left, agents choose actions randomly, while on the right they have learned to consume the food. Notice how quickly they move towards their targets.

 | ![bacteria](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/gallery/gifs/bacteria.gif) | ![bacteria_intelligent](https://raw.githubusercontent.com/SeverTopan/AdjSim/master/gallery/gifs/bacteria_intelligent.gif) |
|:-------------:|:-------------:|