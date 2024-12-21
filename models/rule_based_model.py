import re
from indicnlp.tokenize import sentence_tokenize
from indicnlp.tokenize.indic_tokenize import trivial_tokenize

class RuleBasedChecker:
    def __init__(self):
        # Extended Tamil dictionary
        self.tamil_words = set([
            'வணக்கம்', 'நன்றி', 'இந்திய', 'தமிழ்', 'பயிற்சி',
            'நான்', 'நீ', 'அவன்', 'அவள்', 'அது', 'நாங்கள்', 'நீங்கள்', 'அவர்கள்',
            'பள்ளி', 'செல்', 'படி', 'எழுது', 'பேசு', 'கேள்', 'பார்'
        ])
        
        # Extended grammar rules
        self.grammar_rules = {
            'subject_verb': [
                (r'நான்.*கிறார்கள்', 'First person singular with plural verb'),
                (r'நாங்கள்.*கிறான்', 'First person plural with singular verb'),
                (r'அவன்.*கிறார்கள்', 'Third person singular with plural verb'),
                (r'அவர்கள்.*கிறான்', 'Third person plural with singular verb')
            ],
            'tense': [
                (r'\w+கிறேன்\s+\w+ந்தேன்', 'Mixed present and past tense'),
                (r'\w+வேன்\s+\w+கிறேன்', 'Mixed future and present tense'),
                (r'\w+ந்தேன்\s+\w+வேன்', 'Mixed past and future tense')
            ]
        }
    
    def check_spelling(self, text):
        errors = []
        words = trivial_tokenize(text)
        
        for word in words:
            if word not in self.tamil_words:
                errors.append(('spelling', f'Unknown word: {word}', word))
        
        return errors
    
    def check_grammar(self, text):
        errors = []
        sentences = sentence_tokenize(text, lang='ta')
        
        for sentence in sentences:
            for rule_type, rules in self.grammar_rules.items():
                for pattern, error_msg in rules:
                    if re.search(pattern, sentence):
                        errors.append(('grammar', error_msg, sentence))
        
        return errors
    
    def check_text(self, text):
        return self.check_spelling(text) + self.check_grammar(text)

# models/deep_learning_model.py
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class DeepLearningChecker:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-bert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ai4bharat/indic-bert")
        
    def check_text(self, text):
        try:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get error probability
            probabilities = torch.softmax(outputs.logits, dim=1)
            error_prob = probabilities[0][1].item()
            
            errors = []
            if error_prob > 0.5:
                errors.append(('grammar', f'Error probability: {error_prob:.2%}', text))
            
            return errors
            
        except Exception as e:
            return [('error', str(e), text)]