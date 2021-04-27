*************************************Dot Square Project Readme File****************************************

Open the project in PyCharm IDE, then open main.py file, and configure (GridSize (line no 229) , no_of_executions (line no 230), and isGPUEnabled (line no 231)) variables. These variables are assigned with default values.

1. By default GridSize is initialized as 5 that is a 5*5 grid. If you want to try a different gridsize change this variable. 

NOTE: When you are changing the gridsize value, make sure that isGPUEnabled is False. Neural Network is trained with 5*5 grid, so if gridsize value is changed then the neural network will not work as expected.

2. If you want to execute the game multiple times, then provide according to value to no_of_executions, by default is it assigned as 1.

3. IsGPUEnabled is a boolean value, if it is set to False, then the minimax algorithm will return the best move, and if is set to True, then both minimax algorithm and neural network will run and return the best move.


Once the above variables are configured, then run the main.py file in PyCharm IDE



