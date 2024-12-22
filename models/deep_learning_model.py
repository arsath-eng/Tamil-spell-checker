# models/deep_learning_model.py

from transformers import pipeline
import torch

class DeepLearningChecker:
    def __init__(self):
        try:
            self.model = pipeline(
                "text-classification",
                model="ai4bharat/indic-bert",
                tokenizer="ai4bharat/indic-bert"
            )
        except Exception:
            self.model = None
            
    def check_text(self, text):
        if not self.model:
            return [('error', 'Model not loaded properly', text)]
            
        errors = []
        sentences = text.split('।')
        
        for sentence in sentences:
            try:
                prediction = self.model(sentence)
                if prediction[0]['score'] < 0.8:  # Confidence threshold
                    errors.append(
                        ('grammar', 'Low confidence in sentence structure',
                         f'Sentence: {sentence}')
                    )
            except Exception as e:
                errors.append(('error', str(e), sentence))
                
        return errors
