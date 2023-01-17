# This is a change test.

from spellchecker import SpellChecker
spell = SpellChecker()
import re
from collections import Counter
import csv



def main():
    '''
    This takes files from the main.txt, and acros.txt and converts them to strings to check.
    It then runs through each program to check the given files.
    Finally, it will output suggestions from 4 categories:
        -acronyms not on list or on list but not in bullets
        -misspellings checked against dictionary and approved abbreviations
        -duplicate items
        -misc tips (double space after '!', no spacing with '--', etc.)
    '''

    print(welcome_message)
    _ = input('Press "enter" to continue...')

    # Opens our abbrevs.csv file and converts it to a list of approved abbreviations.
    abbrevList = createAbbrevList()

    # Create our initial main input, acronym list (broken down into an actual list), and the main split up into a list of individual words.
    mainText, acroList, mainSplit = get_paras()
    # Check our acronyms in text vs the acronym listing.
    notInAcros, notInText = acro(mainSplit, acroList)
    # Check for spelling errors and make sure they're not just approved abbreviations.
    misspelled = abbrevSpell(mainSplit, abbrevList)
    # Run our misc checks.
    exclaimError, doubleHyphError, startHyphError = miscChecks(mainText)
    # Check for repeats and return a list of them.
    repeats = doubleCheck(mainSplit)

    print('Acronyms in acronym listing but not in text: ', notInText)
    print('Acronyms in text but not in acronym listing: ', notInAcros)
    print('Here are words to consider changing as they are repeated in the text: ', repeats)
    print('Here is a list of potentially misspelled words: ', misspelled)
    if exclaimError:
        print('ERROR DETECTED: Ensure your exclaimation points have two spaces following them.')
    if doubleHyphError:
        print('ERROR DETECTED: Ensure there is no spacing before or after any "--".')
    if startHyphError:
        print('ERROR DETECTED: Ensure when starting a line with a hyphen that you put just one space after it.')



def get_paras():
    # This will pull input from OPR/EPR/Awards files (main.txt) as well as their acronym list file (acros.txt).

    # Creates a strings as placeholders for our "main.txt" and "acros.txt" files.
    mainText = ''
    acroList = ''

    # Open our main and acronym files to convert them into strings to use.
    with open('main.txt', 'r') as m, open('acros.txt', 'r') as a:
        mainText = m.read()
        acroList = a.read()

    # Open our acronym file and convert it to a string to use.
    with open('acros.txt', 'r') as f:
        acroList = f.read()

    # Split mainText into individual words.
    mainSplit = breakDownMain(mainText)

    # Split acros into only a list of acros.
    acroList = breakDownAcro(acroList)


    return mainText, acroList, mainSplit


    # TODO may want to reformat mainText and acroLists to make them easier to read for following functions.
        # Consider breaking down main input into lines so final output tells users where errors are.
            # Alternatively, in webapp version return imput with words highlighted, or changed colors.



def acro(mainSplit, acroList):
    # This will check our acronyms in main against our list and see if there are any in either that don't appear in the other.

    '''# Creates empty lists to store any items that don't match either list.
    itemsNotInAcros = []
    itemsNotInText = []

    # Runs through our acronym listing and if it's not in the main text, adds to our 'itemsNotInText' list.
    for item in acroList:
        if item not in mainSplit:
            itemsNotInText.append(item)

    # Runs through our main text and if item isn't in the acronym listing, adds to our 'itemsNotInacros' list.
    for item in mainSplit:
        if item.isupper() and (len(item) > 1):
            if item not in acroList:
                itemsNotInAcros.append(item)'''

    acroSet = set(acroList)
    mainSet = set(mainSplit)
    _ = []
    for item in mainSet:
        if item.isupper() and (len(item) > 1):
            continue
        _.append(item)
    for item in _:
        mainSet.remove(item)
    
    itemsNotInText = acroSet - mainSet
    itemsNotInAcros = mainSet - acroSet

    return list(itemsNotInAcros), list(itemsNotInText)

    #TODO consider checking if acronyms in list actually have definitions listed.



def abbrevSpell(mainSplit, abbrevList):
    # This will check all the spelling in the main block against a loaded dictionary and an approved abbreviation list.

    # Look for caps (acronyms).
    acros = []
    for word in mainSplit:
        if word.isupper() and (len(word) > 1):
            acros.append(word)
    # Remove acros from mainSplit copy.
    for word in acros:
        mainSplit.remove(word)


    misspelled = spell.unknown(mainSplit)
    misspelled = list(misspelled)

    # Check against abbreviation list and remove from mispellings if it's in there.
    abbrevs = []
    for word in misspelled:
        if word in abbrevList:
            abbrevs.append(word)
    # Remove abbrevs from misspelled list.
    for word in abbrevs:
        misspelled.remove(word)
            
    

    return misspelled



def doubleCheck(mainSplit):
    # This function will check the text for any words that may have been used twice.

    # Makes sure everything is lowercase for easy comparison.
    mainSplit = list(map(str.lower, mainSplit))
    for item in mainSplit:
        if len(item) == 1:
            mainSplit.remove(item)

    count = Counter(mainSplit)
    return [key for key in count if count[key] > 1]


    # TODO Probably want to ignore common repeats (e.g. "to", "be", "from", "by", etc.).



def miscChecks(mainText):
    # This will check for the following misc items:
        # Double space after any '!'.
        # No spacing between '--'.
        # One space between '-' and first word.

    # Check to ensure there are two spaces after any "!"; not 1 and not 3+.
    exclaimError = False
    if re.search("!", mainText):
        if re.search("! (?! )", mainText):
            exclaimError = True
        if re.search("!   +", mainText):
            exclaimError = True

    # Check to make sure there is no spacing between any "--".
    doubleHyphError = False
    if re.search(" --", mainText):
        doubleHyphError = True
    if re.search("-- ", mainText):
        doubleHyphError = True

    # Check to make sure any hypens at the start have one space after.
    startHyphError = False
    if re.search(r"(\n)-(?! )", mainText) or re.search(r"^-(?! )", mainText):
        startHyphError = True
    if re.search(r"(\n)-  +", mainText) or re.search(r"^-  +", mainText):
        startHyphError = True
    
    
    return exclaimError, doubleHyphError, startHyphError

    # TODO This currently only detects an error, but does not tell us where it is specifically. May want to adjust in web app.



def breakDownMain(string):
    # This will break down any string into individual words, stripping away spaces and puncuation.

    # Remove punctuation and replace with spaces as those will get deleted later.
    for char in range(len(string)):
        if string[char] in ['!', ';', ',', '?', '.', '$', '-', '/', '(', ')', ':', '"', '\n']:
            string = string.replace(string[char], ' ')

    # Split the string by spaces.
    noSpaces = string.split(' ')
    # Get rid of any leftover spaces or blank entries.
    while ' ' in noSpaces:
        noSpaces.remove(' ')
    while '' in noSpaces:
        noSpaces.remove('')
    # Strip all items in list to remove spaces as well.
    [item.strip() for item in noSpaces]

    return noSpaces


# TODO may want to add functionality to check number formatting as well.
    # This will probably require us to differentiate between the different input types (i.e. award vs. EPR vs. OPR).



def breakDownAcro(string):
    # This will break down any string into individual words, stripping away spaces and puncuation, then determine which are all caps (acros).

    # Perform all steps from breakDownMain in order to return a list of all words in the input.
    list = breakDownMain(string)

    # Now determine which words are acros (all caps) and get rid of the rest.
    badWords = []
    for item in list:
        if not item.isupper():
            badWords.append(item)
    for word in badWords:
        list.remove(word)


    return list



def createAbbrevList():
    # Opens our abbrevs.csv file and converts it to a list of approved abbreviations.
    abbrevList = []
    with open('abbrevs.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                abbrevList.append(row[0])
            except IndexError:
                pass

    return abbrevList


welcome_message =   '\n******************\nWelcome to the Python OPR/EPR/Awards Checker!' \
                    '\nThis program will convert text in the "main.txt" and "acros.txt" files to perform common checks.' \
                    '\nThe tool will then take your files and produce suggested edits to improve your product!\n\n'

if __name__ == '__main__':
    main()