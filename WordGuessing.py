# Shayling Zhao
# NetID: SXZ190015

import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem import*
import pathlib
from random import seed
from random import randint


def preprocess(tokens):

    stop_words = set(stopwords.words('english'))
    # setting up the lemmatizer
    lemmatizer = WordNetLemmatizer()
    # Creating new list
    oList = []
    # Creating list of unique lemmas
    uniqLemmas = set()
    # iterating through the tokenized list of words in raw_text
    for t in tokens:
        # if the word is composed of letters in the alphabet
        if t.isalpha() and t not in stop_words and len(t) > 5:
            # convert to lower case
            t = t.lower()
            # lemmatize the tokens
            x = lemmatizer.lemmatize(t)
            # add the word to list
            oList.append(t)
            # adding the word to list of unique lemmas
            uniqLemmas.add(x)

    # Creating new list
    nList = []
    # pos (part of speech) tagging
    tags = nltk.pos_tag(uniqLemmas)
    for tg in tags:
        # take only the words that are nouns by reading index 1 of each item
        if tg[1].startswith('N'):
            nList.append(tg)
    # Creating a new list with only  nouns
    nounList = []
    for n in nList:
        # saving only index 0 of the tuple so we only have the nouns
        nounList.append(n[0])
    print(nounList[:20])

    print("Number of tokens:", len(oList))
    print("Number of nouns:", len(set(nounList)))

    return tokens, nounList

def guessingGame(topNouns):
    score = 5
    seed(30)
    # Creating list of top words without the frequency
    topWords = []
    for t in topNouns:
        topWords.append(t[0])
    guessedLetter = 's'
    print("Let's play a word guessing game!")

    while score >= 0 and guessedLetter != '!':
        # Getting a random word of the 50
        wordIndex = randint(0, 49)
        # Saving the randomly generated word as a list into new variable
        randomWord = list(topWords[wordIndex])
        # Saving length of randomWord into a new variable
        wordLength = len(randomWord)
        # Saving the underscores in length of word as a list into a new variable
        underscores = list("_" * wordLength)
        # printing underscores as a string
        print("".join(underscores))

        # While loop with termination perameters
        while "_" in underscores and score >= 0 and guessedLetter != '!':
            guessedLetter = input("Guess a letter: ")
            # If guessed letter is already guessed
            if guessedLetter in underscores:
                print("You guessed a repeated letter")
            # If guessed letter is inside the random word and not already guessed
            if guessedLetter in randomWord and guessedLetter not in underscores:
                # add one to the score
                score = score + 1
                print("Right! Score is", score)
                # Iterate through the chars in the random word
                for r in range(wordLength):
                    # if the guessed letter is equal to the value at the index of the random word
                    if guessedLetter == randomWord[r]:
                        # set the letter at the index of the underscores
                        underscores[r] = guessedLetter
                # print the underscores and letters as a string
                print("".join(underscores))
            else:
                # if they guess the letter wrong, subtract a point
                score = score - 1
                print("Sorry, guess again. Score is", score)
        if "_" not in underscores:
            print("You solved it!")
            print("Current score:", score)
            print(" ")
            print("Guess another word")


if __name__ == '__main__':
    # if there are less than two arguments
    if len(sys.argv) < 2:
        input('File invalid. Please enter a file name as a system arg: ')
        quit()
    # setting relative path
    rel_path = sys.argv[1]
    # opening path lib and reading text
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read()

    # tokenizing raw text
    tokens = nltk.word_tokenize(text_in)
    # Calling preprocess function
    tokens, nouns = preprocess(tokens)
    # length of unique tokens divided by total length of tokens
    diversity = (len(set(tokens))) / (len(tokens))
    # printing lexical diversity formatted to 2 decimal places
    # "g" removes insignificant zeros
    print("Lexical Diversity:", '{0:.2g}'.format(diversity))

    # Creating keys for dictionary
    keys = set(nouns)
    # Creating dictionary of tokens
    nounsDict = {noun:tokens.count(noun) for noun in nouns}
    # Sorting the dictionary from greatest frequency to least
    sortedDict = dict(sorted(nounsDict.items(), key=lambda item: item[1], reverse=True))
    # Printing the 50 most common words and their counts
    # must cast to list
    topNouns = list(sortedDict.items())[:50]
    print(topNouns)
    # Calling game function
    guessingGame(topNouns)
