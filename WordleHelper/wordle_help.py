from collections import defaultdict

def guess_word(original_word_list,word_list, guess=False):        
    print("Finding word among {}...".format(len(word_list)))
    shortest_max = 100000   # used to keep track of which guess word is the best case scenario
    chosen_word = ""
    progress_chunk_size = int(len(original_word_list) / 5) # for a progress meter in case of a slow search
    word_counter = 0
    
    if guess == False:

        for guess_word in original_word_list:   
            word_list_dict = defaultdict(list)     
            # maintain progress bar
            word_counter += 1
            if word_counter % progress_chunk_size == 0:
                print("Progress: {}%".format(20*(word_counter/progress_chunk_size)))

            # For each potential guess word, find the result tuple with the most remaining words
            # key:   (1,0,0,2,0)
            # value: list of words such that guessing the `guess_word` would yield that result
            for true_word in word_list:
                result_tuple = get_tuple(guess_word,true_word)
                word_list_dict[result_tuple].append(true_word)

            # retrieve the lengths of the word lists for each tuple
            word_list_lens = []
            for result_tuple in word_list_dict:
                word_list_lens.append(len(word_list_dict[result_tuple]))
            # give preference to words that have a chance of being guessed correctly
            if max(word_list_lens) < shortest_max or (max(word_list_lens) == shortest_max and guess_word in word_list):                
                chosen_word = guess_word
                return_word_list_dict = word_list_dict
                shortest_max = max(word_list_lens)
    else:
        # same strategy as above, find the word lists for each result tuple
        return_word_list_dict = defaultdict(list)   
        for true_word in word_list:            
            result_tuple = get_tuple(guess,true_word)
            return_word_list_dict[result_tuple].append(true_word)
            # get lengths for display
            word_list_lens = []
            for result_tuple in return_word_list_dict:
                word_list_lens.append(len(return_word_list_dict[result_tuple]))
            shortest_max = max(word_list_lens)
    if not guess:
        print("\nYour word:",chosen_word)
    print("Worst case length: {}".format(shortest_max))
    return chosen_word, return_word_list_dict

def get_tuple(guess_word,true_word):
    '''Given a guess value and a true value, find the combo of 
    grey-yellow-green squares corresponding to the accuracy
    of each letter in the guess.
    '''
    # 0 - letter not found in word (grey)
    # 1 - letter in incorrect spot (yellow)
    # 2 - letter in correct spot   (green)
    idx_list = []
    for i in range(len(guess_word)):
        if guess_word[i] == true_word[i]:
            idx_list.append(2)
        elif guess_word[i] in true_word:
            idx_list.append(1)
        else:
            idx_list.append(0)
    return tuple(idx_list)

# extract words from word list
# example line in doc: "Jul 10 2021 Day 21 DEATH"
with open("official_wordle_list.txt") as f:
    words = f.read().split('\n')
for line_idx in range(len(words)):
    words[line_idx] = words[line_idx].split(' ')[5].lower()
wordle_list = [word.lower() for word in words if len(word) == 5]

# words.txt comes from a class project to create a playable Boggle game
#     and contains ~3x as many words as official_wordle_list.txt
with open("words.txt") as f:    
    overall_words = f.read().split('\n')
    f.close()
overall_words = [word.lower() for word in overall_words if len(word) == 5]

while(True):
    print("\nNumber of existing words:",len(wordle_list))
    # let the user manually input a word if desired
    # the first automated guess takes a while, so RAISE or SERAI are recommended
    choice = input("Automate guess? (y/n): ")
    if choice == "y":
        chosen_word, word_dict = guess_word(overall_words, wordle_list)
    else:
        # get valid word from user and calculate new guess
        word_guess = input("Guess: ").lower()        
        while not word_guess.isalpha() or len(word_guess) != 5:
            word_guess = input("Please enter a five letter word:").lower()
        chosen_word, word_dict = guess_word(overall_words,wordle_list,word_guess)
    
    # get score from Wordle and narrow the remaining word list
    results = input("Results: ")
    results = tuple([int(i) for i in results])
    wordle_list = word_dict[results]
    if results == (2,2,2,2,2):
        print("Congratulations! You guessed the word!")
        quit()
    elif len(wordle_list) == 1:
        print("The word is:",wordle_list[0],"\n")
        quit()
    elif len(wordle_list) < 15:
        print("=============================")
        print("Remaining words:")
        print_lines = [[],[],[]]
        for i in range(len(wordle_list)):
            print_lines[i % 3].append(wordle_list[i])
        for line in print_lines:
            print("    ".join(line))
        print("=============================")