# Hangman Game & AI
# Name: Henry Trinh
# CS5 Final Project

from dict import Dictionary
import random
import time
import webbrowser
from collections import Counter

class HangmanGame():

    def __init__(self):
        """The constructor.
           Should include count of wins for each player.
        """
        self.num_comp_wins = 0
        self.num_user_wins = 0
        # no ties are possible with this game ;p

    def __repr__(self):
        """The representation function.
           Should return a string of some sort.
        """
        s = ''
        s += "I have won" + str(self.num_comp_wins) + "games.\n"
        s += "You have won" + str(self.num_user_wins) + "games.\n"
        return s

    def status(self):
        """Prints the current status."""
        print("\n+++ \033[4mCurrent Game Scores\033[0m +++")
        print("+++   You won:", self.num_user_wins, "Times  +++")
        print("+++    AI won:", self.num_comp_wins, "Times  +++")

    def save_game(self, filename):
        """Save to a file."""
        f = open(filename, "w")  # Open file for writing
        print(self.num_comp_wins, file = f)
        print(self.num_user_wins, file = f)
        f.close()
        print(filename, "saved!")

    def load_game(self, filename):
        """Load from a file."""
        f = open(filename, "r")  # Open file for reading
        self.num_comp_wins = int(f.readline())
        self.num_user_wins = int(f.readline())
        f.close()
        print(filename, "loaded!")

    def get_word(self):
        """get random word from bigD file Dictionary variable"""
        word = random.choice(Dictionary)
        return word.upper()

    def isWord(self, word):
        """Checks if word is in Dictionary from bigD file."""
        # i think there may be an issue on my end. Only words with len(word) == 5 are considered to be words in the Dictionary list, which is not true...
        print()
        if word in Dictionary:
            print("Thanks! That is, indeed, a valid word of " + str(len(word)) + " letters.\n")
            # Will now remove word from memory (to make sure I, the computer, cannot cheat!)
            # Used this for aid: https://www.w3schools.com/python/ref_keyword_none.asp
            word = None
            print("I just removed the word from my memory. No fear! I can't cheat... How unfortunate...\n")
            return True
        else:
            print("Sorry, your word is not valid in my dictionary. I might add it someday, but I don't feel like adding it to a whitelist right now. Tough kumquats!")
            return False

    def narrow_choices(self, secret_word_letters):
        """Allows AI to remove words from Dictionary that cannot be the user's chosen word..."""
        # delete words in dictionary based on length of user's word
        for word in Dictionary:
            if len(word) != len(secret_word_letters):
                # Used this for reference: https://www.w3schools.com/python/ref_keyword_del.asp
                Dictionary.remove(word)
            
        # deletes words in dictionary based on previous AI guesses
        for word in Dictionary:
            for i, letter in enumerate(word):
                if (secret_word_letters[i] != " " and secret_word_letters[i] != word[i]) or (secret_word_letters[i] == " " and letter in guessed_letters):
                    Dictionary.remove(word)
                    break
            
    def narrow_letters(self, guessed_letters):
        """Allows AI to decide its choice letters, based on remaining words"""
        remainingLetters = []
        for word in Dictionary:
            for letter in word:
                if letter not in guessed_letters:
                    remainingLetters.append(letter)  

    def regular_game(self): 
        """gameplay for 1 player vs computer-generated word""" #HUMAN VS COMPUTER
        word = self.get_word()
        secret_word_letters = "_" * len(word)
        guessed = False
        guessed_letters = []
        guessed_words = []
        lives = 6
        print("\nWELCOME TO HANGMAN... \n")
        print("WILL YOU SAVE A MAN FROM DEATH?")
        print(self.display_hangman(lives)) #displays image from display_hangman
        print("\n" + secret_word_letters + " (" + str(len(word)) + " Letters) \n")

        while not guessed and lives > 0:
            guess = input("GUESS A LETTER, OR THE WORD... ").upper()
            if len(guess) == 1 and guess.isalpha(): #user guessed letter
                if guess in guessed_letters:
                    print("YOU ALREADY GUESSED THE LETTER", guess)
                elif guess not in word:
                    print("FOOL! " + guess + " IS NOT IN THE WORD!" + "\n")
                    print("To incentivize you, we will now put a piece of your friend on the hanger...")
                    lives -= 1
                    guessed_letters.append(guess)
                else:
                    print("Ugh, fine... " + guess + " is in the word!")
                    print("Darn, your friend lives a bit longer...") #might include insult list here
                    guessed_letters.append(guess)
                    word_as_list = list(secret_word_letters)
                    LC = [x for x, letter in enumerate(word) if letter == guess]
                    for i in LC:
                        word_as_list[i] = guess
                    secret_word_letters = "".join(word_as_list)
                    if "_" not in secret_word_letters:
                        guessed = True #when there are no hidden letters left
            elif len(guess) == len(word) and guess.isalpha(): #user guesses viable word 
                if guess in guessed_words:
                    print("YOU ALREADY GUESSED", guess)
                elif guess != word:
                    print("BAD TRY! " + guess + " IS NOT THE WORD, DUMMY")
                    lives -= 1 
                    guessed_words.append(guess)
                else:
                    guessed = True
                    secret_word_letters = word #reveals all underscores/hidden letters
            else:
                print("YOUR ANSWER BEWILDERS ME! IT AINT VALID? TRY AGAIN...")
            print(self.display_hangman(lives)) #after move, displayed image depends on number of remaining lives
            print(secret_word_letters)
            print("\n")
        
        if guessed == True:
            print("\u001b[32mFINE, YOU GUESSED THE WORD. YOUR FRIEND LIVES, I GUESS...\033[0m\n")
            self.num_user_wins += 1
        else:
            print("LOSER! WHO LOSES? BOTH YOU AND THIS PERSON, MUAHAHAHHAHA. FYI, THE WORD WAS \033[1m" + word + "\033[0m, HOW COULD YOU NOT GUESS THAT?\n")
            print("\u001b[1;31mFunny, huh. You're now a murderer...\033[0m")
            self.num_comp_wins += 1

    def guess_best_letter_using_word_length(self, length):
        """Narrows down words from Dictionary with same length as user's secret word. 
           Using this, remaining letters in new Dictionary are parsed to return the most 
           frequent letter. This will be what the AI guesses first.
        """
        #Returns new dictionary of words with same length as user's secret word
        #Based on length of user's word, we can narrow how many words fit the criterion simply based on length.
        Diction = []
        for word in Dictionary:
            if int(len(word)) == int(length):
                Diction.append(word)
        
        #following refers to this resource: https://stackoverflow.com/questions/6353049/python-count-each-letter-in-a-list-of-words
        #counts each letter in new Dictionary, Diction list.
        cnt = Counter()
        for word in Diction:
            for letter in set(word):
                cnt[letter] += 1

        #print(cnt.most_common(26)) #Example: [('e', 588), ('a', 536), ('o', 425)]
        #print([a[0] for a in cnt.most_common(1)]) #returns order of best letters to use, based on frequency.
        best_letter_list =  [a[0] for a in cnt.most_common(6)]
        best_letter_str = ''.join(best_letter_list)
        # Join technique to convert single letter to string. Reference: https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
        return best_letter_list

        # if len(word) == 3: 85 variants
        # if len(word) == 3: 513 variants
        # if len(word) == 4: 1568 variants
        # if len(word) == 5: 2152 variants
        ##[('e', 972), ('a', 828), ('r', 772), ('s', 639), ('o', 627), ('t', 611), ('l', 594), ('i', 588), ('n', 521), ('u', 416), ('c', 409), ('y', 374), ('h', 358), ('d', 358), ('p', 322), ('m', 276), ('g', 275), ('b', 238), ('k', 204), ('f', 196), ('w', 189), ('v', 138), ('x', 35), ('z', 35), ('q', 27), ('j', 26)]
        ##['e', 'a', 'r', 's', 'o', 't', 'l', 'i', 'n', 'u', 'c', 'y', 'h', 'd', 'p', 'm', 'g', 'b', 'k', 'f', 'w', 'v', 'x', 'z', 'q', 'j']
        # Best Case: User wants to use 3-letter word from Dictionary list

    def ai_game(self):
        print()
        print("So, you've decided to make me the guesser, huh?\n")
        print("Well, I'll win anyways, hehe! Now, think of any real word you want to use against me...\n")
        print("We first need to check to make sure your word is real, ok?")
        time.sleep(1.4)

        realWordTest = False
        while realWordTest is False:
            user_word = input("\nWhat was the word you chose? Don't worry, I won't remember it later, I promise! ").lower()
            word_length = len(user_word) # i only keep the number of letters, not the actual word...
            if self.isWord(user_word) == True:
                print("Ok, your word is a certified word! BRRZ! The word is no longer in my program... Let's begin the game!")
                user_word = None 
                realWordTest = True
                break
            time.sleep(1)

        secret_word_letters = "_" * int(word_length)
        guessed = False
        guessed_letters = []
        lives = 6
        guessed_words = []
        remainingLetters = []

        print("\nI recorded the number of letters you had in your word. Your job is to just remember the word you chose! DON'T FORGET THE WORD!!!")
        print("\nThis is the hanger... I will now make my guesses, and you must respond!")
        time.sleep(1)
        print(self.display_hangman(lives)) #displays image from display_hangman
        print("\n" + secret_word_letters + " (" + str(word_length) + " Letters) \n")

        while not guessed and lives > 0:
            """Allows AI to remove words from Dictionary that cannot be the user's chosen word..."""
            self.narrow_choices(secret_word_letters)
            
            i = 0
            ai_guess = self.guess_best_letter_using_word_length(word_length)[i]
            guessed_letters.append(ai_guess)

            response = input("Is the letter " + self.guess_best_letter_using_word_length(word_length)[i].upper() + " going to replace a secret letter (underscore)? (y/n) ").lower()
            if "y" in response: #yes
                print("\nI WAS RIGHT?! Haha, of course I was! Silly human, too predictable...")
                times = input("\nHow many spaces does the letter " + self.guess_best_letter_using_word_length(word_length)[i].upper() + " fill? (number) ")
                try:
                    num = int(times)
                    if num not in range(1, word_length + 1):
                        print("Please input a proper number... How many times does the letter " + ai_guess.upper() + " appear in your word? ")
                except ValueError as e:
                    print("\nI have no clue what you just said... Try again...") 
                    time.sleep(1.5)
                looper = int(times)
                while looper > 0:
                    letter_index = input("\nWhich space(s) is it in (number)? The 1st all the way to the " \
                        + str(word_length) + "th letter? \n\nIf there are multiple spaces, only put 1 value for now!\n\n") #this is gonna be fun to reduce human error...
                    try:
                        num = int(letter_index) #conversion to integer
                        if num not in range(1, word_length + 1):
                            print("Please input a proper number for the placement of the letter...")
                            time.sleep(1.5)
                    except ValueError as e: #non-integer value inputted 
                        print("\nI have no clue what you just said... Try again...") 
                        time.sleep(1.5)
                    word_as_list = list(secret_word_letters) #turns underscores into individual lists -> makes it easier to index
                    word_as_list[int(float(letter_index)) - 1] = self.guess_best_letter_using_word_length(word_length)[i] #minus 1 since arrays start at 0
                    secret_word_letters = "".join(word_as_list)
                    print(self.display_hangman(lives)) #after move, displayed image depends on number of remaining lives
                    print(secret_word_letters)
                    looper -= 1
                i += 1
            if "n" in response: #no, but there was the prescence of the letter. Hence, no lives removed from AI.
                lives -= 1 
                print(self.display_hangman(lives)) #after move, displayed image depends on number of remaining lives
                print(secret_word_letters)
                print("\nWhoops! Even AIs make mistakes ;(\n")
                i += 1
                ai_guess = self.guess_best_letter_using_word_length(word_length)[i]
                guessed_letters.append(ai_guess)
        
        answer = input("Is the word " + random.choice(Dictionary) + "? ") #dictionary should only have a few choices left based on reduction functions. Thus, this is an educated guess!
        if "y" in answer or "_" not in secret_word_letters:
            guessed = True #when there are no hidden letters left
            print("\u001b[1;31mEven with your own word, you still manage to lose...\033[0m")
            self.num_comp_wins += 1
        elif "n" in answer:
            lives = 0
            print("\u001b[32mFINE, I COULDN'T GUESS YOUR WORD! YOU WERE TOO GOOD...\033[0m\n") #may want to display the user's word
            self.num_user_wins += 1
        else:
            print("\u001b[32mFINE, I COULDN'T GUESS YOUR WORD! YOU WERE TOO GOOD...\033[0m\n") #may want to display the user's word
            self.num_user_wins += 1

    def display_hangman(self, lives):
        """displays all 7 different hangman scenarios. Placed in list; dependent on lives left."""
        hangman_imgs = [  #tiktok sound: her arms wre cut off, her legs were cut off, her ears were cut off...
                # final state: all body parts. [0] index means 0 lives.
            """
            +-------
            |      |
            |      O
            |     \\|/
            |      |
            |     / \\
           ===
            """,
            # all body parts, minus one leg.
            """
            +-------
            |      |
            |      O
            |     \\|/
            |      |
            |     / 
           ===
            """,
            # all body parts, minus both legs.
            """
            +-------
            |      |
            |      O
            |     \\|/
            |      |
            |      
           ===
            """,
            # all body parts, minus legs and one armm
            """
            +-------
            |      |
            |      O
            |     \\|
            |      |
            |     
           ===
            """,
            #  head and torso, only.
            """
            +-------
            |      |
            |      O
            |      |
            |      |
            |     
           ===
            """,
            # head, only
            """
            +-------
            |      |
            |      O
            |    
            |      
            |     
           ===
            """,
            # initial empty state: no body parts
            """
            +-------
            |      |
            |      
            |    
            |      
            |     
           ===
            """
        ]
        return hangman_imgs[lives]

    def menu(self):
        """Prints the menu of options that the user can choose."""
        print()
        print("\033[4mMenu\033[0m:\n")
        print(" (0) View Scoreboard") #self.status()
        print(" (1) Regular Hangman (You vs Computer)")
        print(" (2) AI Hangman (Computer vs You)")
        print(" (3) For Grutors Only") #Grutor version
        print(" (4) For Professors Only") #Prof Version
        print(" (5) You've Been Warned I")
        print(" (6) You've Been Warned II")
        print(" (7) Save Current Game")
        print(" (8) Load Previous Game")
        print(" (9) Exit (Quit!)")
        print()

    def play(self):
        """After the Menu Page, User Input (choice) determines subsequent action."""
        while True:

            self.menu()
            
            choice = input("Your Choice: ")
            try:
                choice = int(choice) #conversion to integer
                if choice not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    print("Please input a proper menu number...")
                    time.sleep(1.5)
                    self.menu()  
            except ValueError as e: #non-integer value inputted 
                """PLEASE CHANGE CS5 SITE TO REFLECT ValueError, NOT ParseError!!!! Took too long to fix, haha"""
                print("I have no clue what you just said... Try again...") 
                time.sleep(1.5)
                self.menu()       
            
            time.sleep(.25)

            if choice == 0:
                self.status()
            
            elif choice == 1:
                self.regular_game()

            elif choice == 2:
                self.ai_game()

            elif choice == 3:
                time.sleep(0.4)
                print("\nA grutor, eh?\n")
                time.sleep(1.5)
                print("You really thought... I'd make your life easier? How dare you! No, you must play the game like everyone else 😈")
                time.sleep(3.3)

            elif choice == 4:
                self.num_comp_wins = 0
                self.num_user_wins = 1000
                time.sleep(0.4)
                print("\nOh, hey! My Professor!\n")
                time.sleep(0.5)
                print("My brilliant, opulent, radiant, glimmering-\n")
                time.sleep(2)
                print("** PLEASE GIMME 100% ^BARK ^BARK ^BARK **\n")
                time.sleep(1.7)
                print("Oh, oops. I meant to say, CONGRATULATIONS!\n")
                time.sleep(1.5)
                print("Your score has been updated to reflect your superior intellect. Please view the Scoreboard.")

            elif choice == 5:
                time.sleep(0.5)
                print("\ni tried to think of a joke \n\nbut i couldnt so...")
                time.sleep(0.7)
                print("\ni guess this counts as something...")
                time.sleep(1.5)
                url = "https://www.youtube.com/watch?v=le5uGqHKll8"
                webbrowser.open_new_tab(url)

            elif choice == 6:
                time.sleep(0.4)
                print("\nI can't think of anything cool, so... here's some anime!")
                time.sleep(1.3)
                url = "https://www.youtube.com/watch?v=B4FQ6QaXOaA"
                webbrowser.open_new_tab(url)

            elif choice == 7:
                time.sleep(1)
                self.save_game("gamefile.txt")

            elif choice == 8:
                try:
                    self.load_game("gamefile.txt")
                    print("Welcome back!")
                except FileNotFoundError as e: #You don't have a file to load to begin with...
                    print("\nYou don't have a previous game to load, dummy!")
                    time.sleep(1.25)

            elif choice == 9:
                print("\nOk, Goodbye! Hope You Enjoyed The Game :D")
                time.sleep(1)
                break 

            else: #10
                time.sleep(.4)
                print("Here's your easter egg, O' Great Grutor:")
                time.sleep(1.2)
                url = "https://unscramblex.com/anagram/grutor/?dictionary=nwl"
                webbrowser.open_new_tab(url)
 
loadGame = HangmanGame()
loadGame.play()

"""FUNCTIONS I DEEMED USELESS BUT COULD BE USED IN THE FUTURE

def best_random_letter(self):
    #Determines best letter (randomly). Used typically for first guess
    #Dictionary Retrieved from https://gist.github.com/pozhidaevak/0dca594d6f0de367f232909fe21cdb2f
    letterFrequency = {'E' : 12.0,
        'T' : 9.10,
        'A' : 8.12,
        'O' : 7.68,
        'I' : 7.31,
        'N' : 6.95,
        'S' : 6.28,
        'R' : 6.02,
        'H' : 5.92,
        'D' : 4.32,
        'L' : 3.98,
        'U' : 2.88,
        'C' : 2.71,
        'M' : 2.61,
        'F' : 2.30,
        'Y' : 2.11,
        'W' : 2.09,
        'G' : 2.03,
        'P' : 1.82,
        'B' : 1.49,
        'V' : 1.11,
        'K' : 0.69,
        'X' : 0.17,
        'Q' : 0.11,
        'J' : 0.10,
        'Z' : 0.07 }
    #list of alphabet letters, except letters with < 3% frequency were removed...
    best_alphabet = ['a', 'd', 'e', 'h', 'i', 'l', 'n', 'o', 'r', 's', 't']
    letter = random.choice(best_alphabet)
    return letter

"""
