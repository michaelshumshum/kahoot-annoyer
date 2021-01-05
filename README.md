# kahoot-annoyer
there is no such thing as fun
## about
literally flood kahoot.it games with bots.
inspired by [msemple's kahoot-hack](https://github.com/msemple1111/kahoot-hack) and [theusaf's kahootPy](https://github.com/theusaf/KahootPY)

## cool features
- flood kahoot.it games with lots of bots. the beefier your computer, the more bots. from my testing on my touchbar macbook pro, i could easily get 200+ bots.
- the bots can answer every single type of question possible on a quiz, including multiselection, jumble, and open-ended. for the multiple-choice questions, the bots will choose random answers, while with open-ended, will input a random string of text.
- comes with a pretty neat terminal interface that is half working. it will potentially display data about the bots in the game such as the highest scoring bot, highest streak bot, and what answers the bots provided for each question. the interface also includes a basic and barely readable "log". as of now, the interface is still quite broken.
- i also included a brute-force kahoot-code searcher that can search the entire world for active kahoot games. though, keep in mind that not all the games are joinable due to latency. 

## prerequisites
- python 3.x
- `pip install npyscreen`
- a decent internet connection and computer

## usage
to flood bots, run the `flood.py` script. it will prompt you for the game PIN, the number of bots, and an optional custom name for the bots. alternatively, you can add arguments to when you run the script instead of answering the prompts.

(example: `python3 flood.py <PIN> <# of bots> <custom name>`).

as of now, the scripts will not close itself upon game end. for now, press ctrl+c to end it. the terminal formatting will look weird afterwards due to how npyscreen works. type `reset` into the terminal and it should go back to normal.

to search for kahoot games, run `search.py`. keep in mind that this script is quite resource heavy and doesn't ensure you can join those games, only provides you with codes for active games. press ctrl+c to end the script.

do not touch any of the scripts with an `_` at the front unless you know what you are doing.

## notes
it is still not perfect and can definetly be improved. some methods i use are quite stupid, such as the mothership class. i plan to optimize the code and increase the potential.
feel free to suggest pull requests and identify issues.
