# kahoot-annoyer
there is no such thing as fun
## about
literally flood kahoot.it games with bots.
inspired by [msemple's kahoot-hack](https://github.com/msemple1111/kahoot-hack) and [theusaf's kahootPy](https://github.com/theusaf/KahootPY)

## cool features
- flood kahoot.it games with lots of bots. the beefier your computer, the more bots. from my testing on my touchbar macbook pro, i could easily get 200+ bots.
- the bots can answer every single type of question possible on a quiz, including multiselection, jumble, and open-ended. for the multiple-choice questions, the bots will choose random answers, while with open-ended, will input a random string of text.
- comes with a pretty neat terminal interface that shows some information about the bots.
- i also included a brute-force kahoot-code searcher that can search the entire world for active kahoot games. though, keep in mind that not all the games are joinable due to latency. 
- with this method of injecting bots, there is no character limit for the names.

**NEW:**

you can now style the names with different unicode characters. the script will randomly "style" each of the bot's names with a new unicode characters. though, this doesn't bypass the name profanity filter as this was patched a while ago. still, quite a neat feature.

i also added a new overflow "exploit". when enabling glitch names, the bots' names will be replaced b high densit unicode character strings that are very large in length. when the bots join, the host will experience lots of lag and will become quite buggy. if the bots join before the start of the game, the game becomes extremely unresponsive for a while. when going through the questions, displaying the names on screen will also lag the game a little bit and take up lots of space on the screen. the best outcome of this feature is that the host becomes unable to send requests to the players with important data such as their score, whether they got the question right, and ranking. this also means the bots themselves do not receive this information. as such, players will not be able to view their score and any other related information, which could be quite frustrating. side effects of this is that the interface/gui gets broken and the bots will not know how to leave the game themselves.

## prerequisites
- python 3.x
- `pip install npyscreen, python-pyfiglet`
- a decent internet connection and computer

## usage
download or clone this repositiory to your computer. all files, besides the `README.md` of course, are required.
to flood bots, run the `flood.py` script. it will prompt you for the game PIN, the number of bots, and an optional custom name for the bots. alternatively, you can add arguments to when you run the script instead of answering the prompts. though, you will still have to answer the name styling and glitch name prompt no matter what.

(example: `python3 flood.py <PIN> <# of bots> <custom name>`).

if you have enable glitched names, you will have to close the script manually by pressing `ctrl + c` and typing `reset` into the terminal to restore it. usually, this is done automatically, but with the glitch names, the host client is unable to send this information to the bots.

to search for kahoot games, run `search.py`. keep in mind that this script is quite resource heavy and doesn't ensure you can join those games, only provides you with codes for active games. though, due to the large amounts of codes you get, you can get lucky with a code that has a good connection.

do not touch any of the scripts with an `_` at the front unless you know what you are doing.

## notes
it is still not perfect and can definetly be improved. there are still a few things i want to add, such as providing more kinds of information in the log box.
feel free to suggest pull requests and identify issues.

i am not liable for any damage caused by the users of my scripts. these scripts most likely break kahoot's TOS (terms of service) and any consequences from misuse or severity are solely the users responsibility.
