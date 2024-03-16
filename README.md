# Optimizing Agricultural Land Arrangement Using Genetic Algorithm

This project aims to optimize agricultural land arrangement using genetic algorithm to maximize agricultural yield. The genetic algorithm is employed to find the optimal allocation of various crops on a piece of agricultural land, taking into account production costs, yield, land area, selling prices, and available budget.

## Project Description

This project is implemented using Python programming language and leverages several libraries such as NumPy, Streamlit, and Matplotlib. The genetic algorithm is used as the main optimization method. Here are the main components of this project:

- **Population Initialization**: The initial population is randomly generated with normalized proportions.
- **Fitness Calculation**: Each individual in the population is evaluated based on the income generated minus the total production costs, taking into account the budget.
- **Roulette Wheel Selection**: Individuals are chosen for reproduction based on probabilities associated with their fitness.
- **Arithmetic Crossover**: The reproduction process uses arithmetic crossover to produce offspring from parent pairs.
- **Non-Uniform Mutation**: Mutation occurs in individuals with mutation rates adjusted based on generation.
- **Streamlit Interface**: Streamlit interface is used for user input and visualization of results.
- **Land Allocation Chart**: A pie chart displays the land allocation for each type of crop.
- **Fitness Development Chart**: A line chart shows the changes in best fitness during evolution.

## How to Run the Project

1. Make sure Python and pip are installed on your system.
3. Run the application with the command `streamlit run filename.py`.
4. Set parameters such as population size, number of generations, mutation rate, and crossover rate through the Streamlit interface.
5. Enter details for each type of crop and the general input.
6. Click the "Optimize Land" button to start the optimization process.
7. View the displayed land allocation and fitness development.

## Contributors

## Contributors

## Contributors
- Baren Baruna Harahap (23/519317/NUGM/01057)
- Carica Deffa Yullinda (20/462179/PA/20151)
- Elecia Budi Syabila (23/528383/NPA/19900)
- Mahsa Rahima Yunus (23/528361/NPA/19880)
