from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class StatisticalChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        self.model = MultinomialNB()
        
        # Extended training data
        self.train_texts = [
            "நான் பள்ளிக்கு செல்கிறேன்",
            "நாங்கள் பள்ளிக்கு செல்கிறோம்",
            "அவன் பள்ளிக்கு செல்கிறான்",
            "நான் பள்ளிக்கு செல்கிறது",
            "நாங்கள் பள்ளிக்கு செல்கிறான்",
            "அவர்கள் பள்ளிக்கு செல்கிறான்"
        ]
        self.train_labels = [1, 1, 1, 0, 0, 0]  # 1 for correct, 0 for incorrect
        
        # Train the model
        X = self.vectorizer.fit_transform(self.train_texts)
        self.model.fit(X, self.train_labels)
    
    def check_text(self, text):
        try:
            X = self.vectorizer.transform([text])
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0]
            
            errors = []
            if prediction == 0:
                conf = probability[0]
                errors.append(('statistical', f'Error confidence: {conf:.2%}', text))
            
            return errors
            
        except Exception as e:
            return [('error', str(e), text)]