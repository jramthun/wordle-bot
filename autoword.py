# Beat wordle without human intervention
# https://www.nytimes.com/games/wordle/index.html

import numpy as np
from PIL import ImageGrab, Image
import cv2, time, random, pyautogui

game_coors = [2260, 571, 2920, 1370]

letter_table = [[' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ']]

wordlist = []
with open('sgb-words.txt', 'r') as f:
    for line in f:
        wordlist.append(line.strip())
# print("Potential words: " + str(len(wordlist)))

def checkTableGuesses(wordle_rgb, darkMode):
    for row in range(6):
        for col in range(5):
            # if 'greenLetter pixel' > 175, color == yellowLetter
            # if 'greenLetter' < 175 and > 160, color == greenLetter
            # if 'greenLetter' < 150, color == greyLetter
            pixel = wordle_rgb.getpixel((10 + (134 * col), 35 + (134 * row)))
            # print(darkMode)

            if darkMode == True:
                if (150 < pixel[1] < 170):
                    letter_table[row][col] = 'y'
                elif (50 < pixel[1] <= 70):
                    letter_table[row][col] = 'g'
                elif (130 < pixel[1] < 150):
                    letter_table[row][col] = 'n'
                else:
                    letter_table[row][col] = 'x'
            else:
                if (pixel[1] > 175 and pixel[1] < 190):
                    letter_table[row][col] = 'y'
                elif (pixel[1] < 150 and pixel[1] > 100):
                    letter_table[row][col] = 'g'
                elif (pixel[1] > 160 and pixel[1] < 175):
                    letter_table[row][col] = 'n'
                else:
                    letter_table[row][col] = 'x'
    return letter_table

# make guess at random
def makeGuess():
    guess = []
    firstIdx = random.randint(0, len(wordlist) - 1)
    first = wordlist[firstIdx]
    for letter in first:
        guess.append(letter)
    print(guess)
    return guess

# handle duplicates
def checkIfDuplicates(listOfElems):
    # ''' Check if given list contains any duplicates '''
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            return True
    return False

def compareWords(guess, wordlist, checks):
    # handle input
    # checks = [' ', ' ', ' ', ' ', ' ']
    # checks[0] = input("Letter color: ")
    # quit if word is correct
    if checks[0] == soln:
        for i in range(len(correct)):
            correct[i] = guess[i]
        return wordlist
    # quit if word is not in the Wordle list
    if checks[0] == notInList:
        return wordlist

    # handle rest of input    
    # for idx in range(1,len(guess)):
        # checks[idx] = input("Letter color: ")

    # handle words with no duplicate letters
    for letter in guess:
        if guess.count(letter) > 1:
                indices = [i for i,x in enumerate(guess) if x == letter]
                # print(indices)
                # word contains duplicates of that letter
                if checks[indices[0]] != greyLetter and checks[indices[1]] != greyLetter:
                    wordlist = [word for word in wordlist if ((letter in word) and (word.count(letter) > 1))]
                    if (letter not in contains):
                        contains.append(letter)
                    # if both greenLetter, keep only words that match
                    if checks[indices[0]] == greenLetter and checks[indices[1]] == greenLetter:
                        wordlist = [word for word in wordlist if (word[indices[0]] == letter) and (word[indices[1]] == letter)]
                        correct[indices[0]] = correct[indices[1]] = letter
                    # if both yellowLetter, keep words that don't have the letters in that location
                    if checks[indices[0]] == yellowLetter and checks[indices[1]] == yellowLetter:
                        wordlist = [word for word in wordlist if (word[indices[0]] != letter) and (word[indices[1]] != letter)]
                    # if one greenLetter & 1 ylw, keep words that have the greenLetter letter in that location and that don't have the yellowLetter letter in that location
                    if checks[indices[0]] == greenLetter and checks[indices[1]] == yellowLetter:
                        wordlist = [word for word in wordlist if (letter in word) and (word[indices[0]] == letter) and (word[indices[1]] != letter)]
                        correct[indices[0]] = letter
                    if checks[indices[0]] == yellowLetter and checks[indices[1]] == greenLetter:
                        wordlist = [word for word in wordlist if (letter in word) and (word[indices[0]] != letter) and (word[indices[1]] == letter)]
                        correct[indices[1]] = letter
                
                # word only has one of that letter
                if checks[indices[0]] == yellowLetter and checks[indices[1]] == greyLetter:
                    # keep if the letter is in the word AND the letter is in the wrong place AND there is only one
                    wordlist = [word for word in wordlist if ((letter in word) and (word.index(letter) != guess.index(letter)) and (word.count(letter) == 1))]
                    if (letter not in contains):
                            contains.append(letter)
                if checks[indices[0]] == greyLetter and checks[indices[1]] == greyLetter:
                    wordlist = [word for word in wordlist if letter not in word]
                if checks[indices[0]] == greyLetter and checks[indices[1]] != greyLetter:
                    check = checks[indices[1]]
                    if (check == yellowLetter):
                        if (letter not in contains):
                            contains.append(letter)
                        wordlist = [word for word in wordlist if (letter in word) and (word.index(letter) != guess.index(letter))]
                    # if greenLetter, keep words that DO contain that letter in that index
                    # works for duplicates
                    if (check == greenLetter):
                        correct[checks.index(greenLetter)] = letter
                        wordlist = [word for word in wordlist if (letter in word) and (word.index(letter) == guess.index(letter))]
        else:
            # print(letter)
            check = checks[guess.index(letter)]
            # if greyLetter, keep words that don't contain that letter at all
            if (check == greyLetter):
                wordlist = [word for word in wordlist if letter not in word]
            # if yellowLetter, keep words that DON'T contain that letter in that index
            if (check == yellowLetter):
                if (letter not in contains):
                    contains.append(letter)
                wordlist = [word for word in wordlist if (letter in word) and (word.index(letter) != guess.index(letter))]
            # if greenLetter, keep words that DO contain that letter in that index
            # works for duplicates
            if (check == greenLetter):
                correct[guess.index(letter)] = letter
                wordlist = [word for word in wordlist if (letter in word) and (word.index(letter) == guess.index(letter))]
        print("Potential words: " + str(len(wordlist)))

        # improvements to handle words with duplicate letters
        # checks = [' ', ' ', ' ', ' ', ' ']
        # for idx in range(0,len(guess)):
        #     checks[idx] = input("Letter color: ")
        # for letter in guess:
        #     if guess.count(letter) > 1:
        #         indices = [i for i,x in enumerate(guess) if x == letter]
        #         # print(indices)
        #         # word only has one of that letter
        #         if checks[indices[0]] == yellowLetter and checks[indices[1]] == greyLetter:
        #             wordlist = [word for word in wordlist if (letter in word) and (word.index(letter) != guess.index(letter)) and (word.count(letter) == 1)]

    print('Known correct letters: ' + str(correct))
    print('Contains: ' + str(contains))
    return wordlist

# Global Variables
# check accuracy
correct = [' ', ' ', ' ', ' ', ' ']
contains = []
# response options:
greyLetter = 'g'
yellowLetter = 'y'
greenLetter = 'n'
notInList = 'x'
soln = 's'

# capture screen for processing
def playWordle():
    global wordlist

    print("Playing wordle...")
    # for i in list(range(3))[::-1]:
    #     print(i+1)
    #     time.sleep(1)

    solved = False
    row = 0
    last_time = time.time()
    while (not solved and row < 6):
        newGuess = makeGuess()
        pyautogui.click(x=950, y=500)
        dispMode =  Image.fromarray(cv2.cvtColor(np.array(ImageGrab.grab(bbox=[940, 500, 945, 505])), cv2.COLOR_BGR2RGB)).convert("RGB").getpixel((1, 1))
        if dispMode[2] < 128:
            darkMode = True
        else:
            darkMode = False
        
        pyautogui.write(newGuess)
        pyautogui.press('enter')
        time.sleep(3)

        screen =  cv2.cvtColor(np.array(ImageGrab.grab(bbox=game_coors)), cv2.COLOR_BGR2RGB)
        # cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        wordle_game = Image.fromarray(screen)
        wordle_rgb = wordle_game.convert("RGB")
        letter_table = checkTableGuesses(wordle_rgb, darkMode)
        print("Row " + str(row) + " results: " + str(letter_table[row]))
        wordlist = compareWords(newGuess, wordlist, letter_table[row])

        if (' ' not in correct):
            solved = True
        if (letter_table[row][0] != 'x'):
            row += 1
        else:
            pyautogui.press("backspace", 5)

    finTime = time.time() - last_time
    if (solved):
        print('Solved in ' + str(row) + ' rows!')
        # print('Solved in ' + str(finTime) + ' seconds')
    else:
        print('Failed to guess :(')

playWordle()

# for __ in range(10):
#     playWordle()
#     with pyautogui.hold('ctrl'):
#         pyautogui.press('tab')
#     with open('sgb-words.txt', 'r') as f:
#         for line in f:
#             wordlist.append(line.strip())
#     correct = [' ', ' ', ' ', ' ', ' ']
#     contains = []