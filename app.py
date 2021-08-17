from googlesearch import search
import webbrowser
import sys
import utils
import os


def main():
    showChoices()

def showChoices():
    choices = {
        'Download by Artist + Song Title':
        'utils.downloadYouTubeVideoWithUserInput()',
        'Scrape and download from a specific chart':
        'utils.scrapeByChart()',
    }
    
    print("---------------------------")

    # Increment index by 1 to make it more user-friendly
    for index, (key, value) in enumerate(choices.items()):
        print(index + 1, ': ', key)

    choices_list = list(choices)
    user_choice = int(input('\nEnter a choice: '))
    
    # Decrement by 1 to match list index
    eval(choices[choices_list[user_choice - 1]])


if __name__ == '__main__':
    main()