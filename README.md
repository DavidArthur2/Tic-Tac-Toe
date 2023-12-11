# Tic-Tac-Toe
A simple implementation of the old-school Tic-Tac-Toe game made in Python, and provided graphical user interface with PySimpleGUI.
The game main features are that it's a multiplayer game, and it can be played with hand gestures.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)

## Introduction

This game is a standard Tic-Tac-Toe game where the main playground is a 3x3 board where 2 players play at the same time. One player comes after the other, and they are putting two different letters on the cells, 'O', and 'X'.
When a player has 3 of its letters in a row, column, or diagonally, wins.
A Match consist of 3 rounds, where a TIE game will be repeated until there is a winner.

## Features

- 3 type of gamemodes: PVE, PVP, and SamePC
- The PVP mode allows you to play with players across the internet
- Hand gesture recognition allows you to select cells on the board with your hands. With the closed palm you can move the 'cursor', while opening the palm marks your letter
- Personalizable gaming experience by changing background colors, selecting preferred camera, and showing the grid on camera for better navigation

## Getting Started

### Requirements

- Python 3.10 or higher
- PC or Laptop running Linux/Windows OS
-	Stable internet-connection
-	Storage space: 450 MB at least
-	Memory: 512 MB RAM at least
-	Dedicated or Integrated Webcam with a minimum resolution of 480x640 
-	Dedicated or Integrated Graphics Card


### Installation
1. Make a project folder, and navigate to it:
   
2. Clone the repository:

    ```git clone https://github.com/DavidArthur2/Tic-Tac-Toe```
3. Navigate into the project folder:
   
   ```cd Tic-Tac-Toe/src```
5. To create a virtual environment, run these commands on a terminal(Command Prompt on Windows, and Terminal on Linux):
   
   ```python -m venv <name_of_virtualenv>```
  7. To activate **Virtual Environment** on Windows, run the following command on CMD:
     
     ```source <name_of_virtualenv>/bin/activate```
     To activate **Virtual Environment** on Linux, run the following command on Terminal:

     ```<name_of_virtualenv>/Scripts/activate.bat```
  9. The python environment setup:
      
    ```pip install -r requirements.txt```


**Note: On Linux, run ```sudo apt-get install python3-tk``` to install tkinter.**



**Optional** if you want a more good-looking Font type, you can install it with the following steps(For Windows):
1. Navigate to the Fonts directory on Windows(Usually this is the location):
   
   ```cd C:\Windows\Fonts```
3. Paste the following code, where <your_project_folder> whould be replaced with the project folder location:
   
   ```copy "<your_project_folder>/Tic-Tac-Toe/src/UI/fonts/Algerian Regular.ttf"```

### Running the Game

Execute the following command in your terminal in your project folder/src:

```python main.py```

## How to Play

1. Run the game using the instructions above.
2. Register an account, or login if you already have one.
3. Select the game-mode you want to play(PVE,SamePC,PVP)
4. **(PVP mode)** Select your enemy
5. Play by the following rules!

## Game Rules

- **Players:** 2 (X and O)
- The game is played on a 3x3 grid.
- Players take turns placing their mark in an empty cell.
- The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins.
- If the grid is full and no player has achieved three in a row, the game ends in a draw, and the round restarts.
- There are total of 3 rounds, and best of 3 wins the match.

## Project Structure

- `src`: Main Python and resource files
- `README.md`: This documentation file.
- `docs`: Documentations and diagrams.

# Thank you for reading it!


