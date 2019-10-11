# Random word generator

### How it works
update_index.py generates an index with :
 - The probability of each letter to be the first of a word
 - The probability of each couple of letter to be the first of a word
 - The probability of each letter to be after a set of 3 letter
 - The probability of each letter to be after a set of 2 letter and at the end

Words.py forms a word by randomly choosing a letter each step according to the probabilities in the 'index' (from update_index.py)
