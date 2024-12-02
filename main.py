# main.py
import streamlit as st
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from Levenshtein import distance
import json
import re

class TamilChecker:
    def __init__(self):
        self.normalizer = IndicNormalizerFactory().get_normalizer("ta")
        
        # Load Tamil word dictionary
        with open('tamil_words.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tamil_words = set()
            for category in data.values():
                self.tamil_words.update(category)
            
            # Store word categories separately for grammar checking
            self.word_categories = data
        
        # Common spelling mistakes and their corrections
        self.spelling_corrections = {
            'நங்க': 'நாங்க',
            'எங்க': 'எங்கே',
            'படிச்சேன்': 'படித்தேன்',
            'போனேன்': 'போனேன்',
            'வந்தேன்': 'வந்தேன்',
            'இருக்கு': 'இருக்கிறது',
            'இல்ல': 'இல்லை',
            'வேணும்': 'வேண்டும்',
            'தெரியல': 'தெரியவில்லை',
            
        }

        # Detailed grammar rules
        self.grammar_rules = {
            # Subject-Verb Agreement
            'agreement_rules': [
                {
                    'pattern': r'(அவர்கள்|நாங்கள்|நீங்கள்)\s+(\w+கிறான்|\w+கிறாள்|\w+கிறது)',
                    'message': 'Plural subject with singular verb',
                    'correction': lambda x: x.group(1) + ' ' + x.group(2).replace('கிறான்', 'கிறார்கள்')
                                                               .replace('கிறாள்', 'கிறார்கள்')
                                                               .replace('கிறது', 'கிறார்கள்')
                },
                {
                    'pattern': r'(அவன்|அவள்)\s+(\w+கிறார்கள்)',
                    'message': 'Singular subject with plural verb',
                    'correction': lambda x: x.group(1) + ' ' + x.group(2).replace('கிறார்கள்', 'கிறார்')
                }
            ],
            
            # Tense consistency
            'tense_rules': [
                {
                    'pattern': r'(\w+கிறேன்|\w+கிறார்)\s+(\w+இருந்தது|\w+இருந்தார்)',
                    'message': 'Inconsistent tense usage',
                    'correction': None  # Complex to autocorrect, will provide suggestion only
                }
            ],
            
            # Word order
            'word_order': [
                {
                    'pattern': r'(\w+)\s+(அந்த|இந்த)',
                    'message': 'Incorrect demonstrative placement',
                    'correction': lambda x: x.group(2) + ' ' + x.group(1)
                }
            ]
        }

    def _get_phonetic_hash(self, word):
        """Create a simple phonetic hash for Tamil words"""
        # Remove vowel marks for approximate matching
        consonants = 'கஙசஞடணதநபமயரலவழளறன'
        result = ''
        for char in word:
            if char in consonants:
                result += char
        return result

    def spell_check(self, text):
        words = text.split()
        corrections = []
        
        for word in words:
            normalized_word = self.normalizer.normalize(word)
            
            # Check direct corrections first
            if word in self.spelling_corrections:
                corrections.append((word, self.spelling_corrections[word]))
                continue
            
            # If not in dictionary, find closest match
            if normalized_word not in self.tamil_words:
                # Get phonetic hash
                word_hash = self._get_phonetic_hash(normalized_word)
                
                # Find closest matches using both Levenshtein and phonetic matching
                candidates = []
                for dict_word in self.tamil_words:
                    dict_hash = self._get_phonetic_hash(dict_word)
                    if len(word_hash) > 0 and len(dict_hash) > 0:
                        if word_hash[0] == dict_hash[0]:  # First character match for speed
                            lev_dist = distance(normalized_word, dict_word)
                            if lev_dist <= 2:
                                candidates.append((dict_word, lev_dist))
                
                if candidates:
                    # Sort by Levenshtein distance
                    closest = min(candidates, key=lambda x: x[1])[0]
                    corrections.append((word, closest))
        
        return corrections[:5]

    def check_grammar(self, text):
        errors = []
        corrections = []
        
        # Check each grammar rule category
        for rule_type, rules in self.grammar_rules.items():
            for rule in rules:
                matches = re.finditer(rule['pattern'], text)
                for match in matches:
                    error = {
                        'type': rule_type,
                        'message': rule['message'],
                        'original': match.group(0)
                    }
                    
                    if rule['correction']:
                        try:
                            corrected = rule['correction'](match)
                            error['suggestion'] = corrected
                        except Exception:
                            error['suggestion'] = None
                    
                    errors.append(error)
                    
                    # If there's a correction, store it
                    if 'suggestion' in error and error['suggestion']:
                        corrections.append((error['original'], error['suggestion']))
        
        return errors, corrections

# Streamlit interface
def main():
    st.title("Tamil Spell and Grammar Checker")
    
    # Initialize checker
    try:
        checker = TamilChecker()
    except Exception as e:
        st.error(f"Error initializing checker: {str(e)}")
        return
    
    # Text input
    text = st.text_area("Enter Tamil text:", height=200)
    
    if st.button("Check Text"):
        if text:
            try:
                # Spell check
                st.subheader("Spelling Corrections")
                spell_corrections = checker.spell_check(text)
                if spell_corrections:
                    for original, suggestion in spell_corrections:
                        st.write(f"Found: {original}")
                        st.write(f"Suggestion: {suggestion}")
                        st.write("---")
                else:
                    st.write("No spelling errors found.")
                
                # Grammar check
                st.subheader("Grammar Analysis")
                grammar_errors, grammar_corrections = checker.check_grammar(text)
                if grammar_errors:
                    for error in grammar_errors:
                        st.write(f"Error Type: {error['type']}")
                        st.write(f"Issue: {error['message']}")
                        st.write(f"Found in: {error['original']}")
                        if 'suggestion' in error and error['suggestion']:
                            st.write(f"Suggestion: {error['suggestion']}")
                        st.write("---")
                else:
                    st.write("No grammar errors found.")
                
                # Show corrected text if there are any corrections
                if spell_corrections or grammar_corrections:
                    st.subheader("Corrected Text")
                    corrected_text = text
                    for original, correction in spell_corrections + grammar_corrections:
                        corrected_text = corrected_text.replace(original, correction)
                    st.write(corrected_text)
                    
            except Exception as e:
                st.error(f"Error processing text: {str(e)}")

if __name__ == "__main__":
    main()