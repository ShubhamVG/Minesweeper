# Minesweeper
#### Video Demo: https://youtu.be/AszSmnss12w
(If I sound sick, that is because I was. Caught cold 🤧)
#### Description: A simple Minesweeper game written in Python, along with an _AI solver_ for the final project of CS50x.

## Introduction
Minesweeper, the classic game we all love, but this time with an added _AI solver_.
The game is so nostalgic for some of us and it probably was the first or second ever computer game we played.
This version has all the features (hopefully) as the classic like flagging certain tiles, 1/4th of the tiles being mines, etc. but as mentioned earlier, also have an _AI solver_ which can play the game on its own and find the best moves on its own!
If you don't know about minesweeper or unfamiliar with its rules, [click here to go to its Wikipedia](https://en.wikipedia.org/wiki/Minesweeper_(video_game)).
This project uses `pygame` to run the GUI (or graphics of the game) whereas the _AI solver_ just follows certain minesweeper tactics and probability to come up with the best move.
_Maybe technically not an AI?_ But implementing reinforcement learning for minesweeper would be like using a Bazuka to kill a house fly.
Mathematically, a perfect minesweeper solver cannot exist. There's always a 1/4 chance of losing on the first move. You do get an advantage later on but there may arise a situation where even the best player is stuck with a 50-50 chance.

## Installation

0. Install [Python](https://python.org/download), if not already installed. Optionally, install [Git](https://git-scm.com/downloads) to clone the repo easily. Git is highly recommended if you are a developer installing this.
1. Clone this repository to your computer (or just download the zip and extract it).
```
git clone https://github.com/ShubhamVG/Minesweeper.git
```
2. Open the terminal in the same directory as where you cloned the repo and install the dependencies by running this command in the terminal.
```
pip install -r requirements.txt
```

## Usage

To play the game, go to the same folder where the repo was cloned and run the following command:

- For Windows:
```
py minesweeper.py
```
- For UNIX/Linux:
```
python3 minesweeper.py
```

IT may take a couple of seconds to load for the first time users. The menu screen will open, press the button for the grid size you want and whether the AI should be the player or not.
To reveal a cell, click on it. If the cell contains a mine, you lose the game. If the cell does not contain a mine, it will reveal the number of mines in its surrounding cells. You can also right-click on a cell to flag it as a mine.

The goal of the game is to reveal all of the non-mine cells.

## Features

* Configurable grid size and number of mines
* Flag cells as mines to avoid accidentally clicking them

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any ideas for improvements.