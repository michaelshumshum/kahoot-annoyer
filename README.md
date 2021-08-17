# kahoot-annoyer
there is no such thing as fun

## about
literally flood kahoot.it games with bots.
inspired by [msemple's kahoot-hack](https://github.com/msemple1111/kahoot-hack) and [theusaf's kahootPy](https://github.com/theusaf/KahootPY)

## cool features
- flood kahoot.it games with lots of bots. the beefier your computer, the more bots. from my testing on my touchbar macbook pro, i could easily get 500+ bots.
- the bots can answer every single type of question possible on a quiz, including multiselection, jumble, and open-ended. for the multiple-choice questions, the bots will choose random answers, while with open-ended, will input a random string of text.
- comes with a pretty neat terminal interface that shows some information about the bots.
- i also included a brute-force kahoot-code searcher that can search the entire world for active kahoot games. though, keep in mind that not all the games are joinable due to latency.
- name styling + glitchy names.

## prerequisites
- python 3.x
- for gui:
- `pip3 install npyscreen`
- a decent internet connection and computer

## usage
download or clone this repository to your computer. all files, besides the `README.md` of course, are required.
to flood bots, run the `flood.py` script. you can use the argument system below, or enable `-i` to use an "interactive" prompt to enable certain options.

(example: `python3 flood.py -p 69420 -b 1337 -n MLG -s`).
```
usage: python3 flood.py -p <PIN> -b <# of bots> [optional arguments]

required arguments:
-b: # of bots. depending on hardware, performance may be significantly affected at higher values.
-p: code for kahoot game.

optional arguments:
-h / --help: shows a help screen with similar information.
-i: input arguments in an "interactive" fashion.
-t: disables terminal output."
-n <name>: set a custom name. by default, name is "bot".
-s: styled names.
-g: glitched names (selecting glitched names will override styled names when enabled).
```
if you have enable glitched names, you will have to close the script manually by pressing `ctrl + c` and typing `reset` into the terminal to restore it. usually, this is done automatically, but with the glitch names, the host client is unable to send this information to the bots.

to search for kahoot games, run `search.py`. keep in mind that this script is quite resource heavy and doesn't ensure you can join those games, only provides you with codes for active games. though, due to the large amounts of codes you get, you can get lucky with a code that has a good connection.

do not touch any of the scripts with an `_` at the front unless you know what you are doing.

## known problems

- occassionally, the bots will be hit with a 'too many retries' HTTPS error. unfortunately, there is no way to combat this issue.

## things I want to do
- implement a brute force 2 factor authentication method, just in case.
- bypass the profanity name filter
- potentially break [this anti-bot script](https://github.com/theusaf/kahoot-antibot)
- just optimise the code

## notes
it is still not perfect and can definitely be improved. there are still a few things i want to add, such as providing more kinds of information in the log box.
feel free to suggest pull requests and identify issues.

i am not liable for any damage caused by the users of my scripts. these scripts most likely break kahoot's TOS (terms of service) and any consequences from misuse or severity are solely the users responsibility.
