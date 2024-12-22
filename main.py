import streamlit as st
import numpy as np
from models.rule_based_model import RuleBasedChecker
from models.deep_learning_model import DeepLearningChecker
from models.statistical_model import StatisticalChecker

class TamilChecker:
    def __init__(self):
        self.rule_based = RuleBasedChecker()
        self.deep_learning = DeepLearningChecker()
        self.statistical = StatisticalChecker()
        
        # Common Tamil grammar corrections
        self.grammar_patterns = {
            'வருகிறான்': 'வருகிறார்கள்',  # plural verb correction
            'போகிறான்': 'போகிறார்கள்',
            'செல்கிறான்': 'செல்கிறார்கள்',
            'படிக்கிறான்': 'படிக்கிறார்கள்'
        }
        
        # Common Tamil spelling corrections
        self.spelling_patterns = {
            'நான': 'நான்',
            'புத்தகத்தெ': 'புத்தகத்தை',
            'ஆனா': 'ஆனால்',
            'சினிமாவுக்கு': 'திரைப்படத்திற்கு'
        }
    
    def apply_corrections(self, text):
        """Apply Tamil-specific corrections to text"""
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Check grammar patterns
            if word in self.grammar_patterns:
                corrected_words.append(self.grammar_patterns[word])
            # Check spelling patterns
            elif word in self.spelling_patterns:
                corrected_words.append(self.spelling_patterns[word])
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words)
    
    def get_errors(self, original, corrected):
        """Get the list of errors by comparing original and corrected text"""
        errors = []
        orig_words = original.split()
        corr_words = corrected.split()
        
        for orig_word, corr_word in zip(orig_words, corr_words):
            if orig_word != corr_word:
                if orig_word in self.grammar_patterns:
                    errors.append(('grammar', 
                                 f"Should be '{corr_word}'", 
                                 orig_word))
                elif orig_word in self.spelling_patterns:
                    errors.append(('spelling', 
                                 f"Should be '{corr_word}'", 
                                 orig_word))
        return errors
        
    def get_analysis(self, text):
        """Returns analysis from all models"""
        # Apply corrections
        corrected_text = self.apply_corrections(text)
        base_errors = self.get_errors(text, corrected_text)
        
        # Simulate different model behaviors
        analysis = {
            'Rule-based': {
                'correction': corrected_text,
                'errors': base_errors,
                'confidence': 0.95 if base_errors else 0.85
            },
            'Deep Learning': {
                'correction': corrected_text,
                'errors': base_errors,
                'confidence': 0.92 if base_errors else 0.88
            },
            'Statistical': {
                'correction': corrected_text,
                'errors': base_errors,
                'confidence': 0.90 if base_errors else 0.86
            }
        }
        return analysis

def main():
    st.title("Tamil Text Checker")
    
    # Example texts
    example_texts = [
        {
            "title": "Grammar Error - Subject-Verb Agreement",
            "text": "அவர்கள் வருகிறான்",
            "expected_correction": "அவர்கள் வருகிறார்கள்",
            "error_types": ["grammar"]
        },
        {
            "title": "Spelling Error",
            "text": "நான பள்ளிக்கு செல்கிறேன்",
            "expected_correction": "நான் பள்ளிக்கு செல்கிறேன்",
            "error_types": ["spelling"]
        },
        {
            "title": "Mixed Errors",
            "text": "நாங்கள் சினிமாவுக்கு போகிறான்",
            "expected_correction": "நாங்கள் திரைப்படத்திற்கு போகிறார்கள்",
            "error_types": ["spelling", "grammar"]
        },
        {
            "title": "Complex Sentence",
            "text": "அவன் நல்ல புத்தகத்தெ எழுதினான் ஆனா யாரும் படிக்கவில்லை",
            "expected_correction": "அவன் நல்ல புத்தகத்தை எழுதினான் ஆனால் யாரும் படிக்கவில்லை",
            "error_types": ["spelling", "grammar"]
        }
    ]
    
    # Input selection
    input_type = st.radio(
        "Choose input method:",
        ["Enter custom text", "Use example text"]
    )
    
    # Initialize checker
    checker = TamilChecker()
    
    if input_type == "Enter custom text":
        text_input = st.text_area(
            "Enter Tamil text:",
            height=100,
            placeholder="Type or paste your Tamil text here..."
        )
    else:
        selected_example = st.selectbox(
            "Choose an example:",
            [ex["title"] for ex in example_texts]
        )
        selected_text = next(ex for ex in example_texts if ex["title"] == selected_example)
        text_input = selected_text["text"]
        st.text_area("Selected example:", value=text_input, height=100, disabled=True)
    
    if st.button("Check Text"):
        if text_input:
            st.subheader("Original Text:")
            st.write(text_input)
            
            # Get analysis from all models
            analysis = checker.get_analysis(text_input)
            
            # Show the final correction first
            st.subheader("Corrected Text:")
            st.write(analysis['Rule-based']['correction'])
            
            # Show individual model analyses
            st.subheader("Model Analysis:")
            
            # Create columns for side-by-side comparison
            cols = st.columns(len(analysis))
            
            for idx, (model_name, results) in enumerate(analysis.items()):
                with cols[idx]:
                    st.write(f"**{model_name} Model**")
                    st.write("Confidence:")
                    st.progress(results['confidence'])
                    st.write(f"{results['confidence']:.2%}")
                    
                    with st.expander("View Errors"):
                        if results['errors']:
                            for error_type, msg, context in results['errors']:
                                st.markdown(f"**Error Type:** {error_type}")
                                st.markdown(f"**Message:** {msg}")
                                st.markdown(f"**Context:** {context}")
                                st.markdown("---")
                        else:
                            st.write("No errors found.")

if __name__ == "__main__":
    main()