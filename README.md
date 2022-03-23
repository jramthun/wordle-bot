# Python Wordle Bot
> A simple solver for [Wordle](https://www.nytimes.com/games/wordle/index.html) in Python

## About
Within one day of being introduced to Wordle, I thought it would be more fun (subjectively) to try to program a script to solve it. I've since seen multiple videos talking about how to solve the game. Related strategies (i.e., potential improvements) include emplying Information Theory to achieve the lowest average number of guesses to solve the puzzle. Instead, I currently have programmed in some heuristics powered by the magic of random.randint. From testing, I've seen roughly 95% chance of solving any given puzzle.

## Getting Started
### Dependencies
- NumPy
- Pillow (PIL)
- CV2
- Time
- Random
- PyAutoGUI
- A 5-letter word dictionary like [SGB-Words](https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt)

### Usage
This implementation uses the resolution of my laptop's display, so you'll have to adjust it for your monitor. All you'll need to do is edit line 8 defining a rectangle:
```python
  game_coors = [topleft_xpos, topleft_ypos, bottomright_xpos, bottomright_ypos]
```
From there, it should be double-click to run. This supports both light and dark mode (tested on Safari 15.4). 

At the bottom, I've left my implementation to play multiple games in a row. I used this to complete 10 games in a row across multiple tabs (which lets me reset the Wordle game). The saved answer is reset on each game (so that it actually resolves the puzzle).
