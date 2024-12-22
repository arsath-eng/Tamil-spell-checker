# models/rule_based_model.py

from tamil_data import TAMIL_LANGUAGE_DATA

class RuleBasedChecker:
    def __init__(self):
        self.data = TAMIL_LANGUAGE_DATA
        
    def check_text(self, text):
        errors = []
        words = text.split()
        
        for i, word in enumerate(words):
            # Check spelling
            if not self._is_valid_word(word):
                correction = self._get_correction(word)
                if correction:
                    errors.append(('spelling', f'Incorrect spelling: {word}', 
                                 f'Suggestion: {correction}'))
            
            # Check grammar
            if i > 0:
                grammar_error = self._check_grammar_rules(words[i-1], word)
                if grammar_error:
                    errors.append(('grammar', grammar_error[0], grammar_error[1]))
        
        return errors
    
    def _is_valid_word(self, word):
        all_words = (self.data['pronouns'] + self.data['verbs'] + 
                    self.data['nouns'] + self.data['adjectives'] + 
                    self.data['common_words'])
        return word in all_words or word in self.data['colloquial_forms'].keys()
    
    def _get_correction(self, word):
        if word in self.data['colloquial_forms']:
            return self.data['colloquial_forms'][word]
        return None
    
    def _check_grammar_rules(self, prev_word, curr_word):
        # Subject-verb agreement check
        if prev_word in self.data['pronouns']:
            if curr_word in self.data['verbs']:
                if not self._check_subject_verb_agreement(prev_word, curr_word):
                    return ('Subject-verb agreement error', 
                           f'{prev_word} {curr_word}')
        return None
    
    def _check_subject_verb_agreement(self, subject, verb):
        # Simplified rule checking
        singular_pronouns = ['நான்', 'நீ', 'அவன்', 'அவள்', 'அது']
        plural_pronouns = ['நாங்கள்', 'நீங்கள்', 'அவர்கள்']
        
        if subject in singular_pronouns and verb.endswith('கிறார்கள்'):
            return False
        if subject in plural_pronouns and not verb.endswith('கிறார்கள்'):
            return False
        return True
