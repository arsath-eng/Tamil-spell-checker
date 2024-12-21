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