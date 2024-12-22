# models/statistical_model.py

from collections import Counter
import numpy as np
from tamil_data import TAMIL_LANGUAGE_DATA

class StatisticalChecker:
    def __init__(self):
        self.data = TAMIL_LANGUAGE_DATA
        self.build_ngram_model()
        
    def build_ngram_model(self):
        # Build bigram frequencies from valid word combinations
        self.bigrams = Counter()
        all_words = (self.data['pronouns'] + self.data['verbs'] + 
                    self.data['nouns'] + self.data['adjectives'])
        
        # Create valid bigrams from known patterns
        for i in range(len(all_words)-1):
            self.bigrams[(all_words[i], all_words[i+1])] += 1
            
    def check_text(self, text):
        errors = []
        words = text.split()
        
        for i in range(len(words)-1):
            bigram = (words[i], words[i+1])
            if self.bigrams[bigram] == 0:  # Unknown combination
                probability = self._calculate_probability(bigram)
                if probability < 0.1:  # Threshold for unlikely combinations
                    errors.append(
                        ('statistical', 
                         f'Unusual word combination: {" ".join(bigram)}',
                         f'Context: {" ".join(words[max(0,i-1):min(len(words),i+3)])}')
                    )
        
        return errors
    
    def _calculate_probability(self, bigram):
        # Simplified probability calculation
        word1, word2 = bigram
        word1_count = sum(1 for w in self.data['pronouns'] + self.data['verbs'] 
                         if w == word1)
        word2_count = sum(1 for w in self.data['pronouns'] + self.data['verbs'] 
                         if w == word2)
        
        if word1_count == 0 or word2_count == 0:
            return 0
        
        return np.sqrt((word1_count * word2_count) / 
                      (len(self.data['pronouns']) + len(self.data['verbs'])))
