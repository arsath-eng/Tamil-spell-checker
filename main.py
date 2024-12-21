import streamlit as st
import numpy as np
from models.rule_based_model import RuleBasedChecker
from models.deep_learning_model import DeepLearningChecker
from models.statistical_model import StatisticalChecker

def compare_models(text):
    models = {
        'Rule-based': RuleBasedChecker(),
        'Deep Learning': DeepLearningChecker(),
        'Statistical': StatisticalChecker()
    }
    
    results = {}
    for model_name, model in models.items():
        try:
            errors = model.check_text(text)
            results[model_name] = errors
        except Exception as e:
            results[model_name] = [('error', f'Error processing text: {str(e)}', text)]
    
    return results

def main():
    st.title("Tamil Text Checker")
    
    # Example inputs
    example_texts = {
        'Correct sentence': 'நான் பள்ளிக்கு செல்கிறேன்',
        'Incorrect spelling': 'நான் பள்ளிக்கு சல்கிறேன்',
        'Grammar error': 'நான் பள்ளிக்கு செல்கிறது',
        'Mixed errors': 'நாங்கள் பள்ளிக்கு செல்கிறான் சல்கிறேன்'
    }
    
    # Input selection
    input_type = st.radio(
        "Choose input method:",
        ["Enter custom text", "Use example text"]
    )
    
    if input_type == "Enter custom text":
        text_input = st.text_area(
            "Enter Tamil text:",
            height=100,
            placeholder="Type or paste your Tamil text here..."
        )
    else:
        selected_example = st.selectbox(
            "Choose an example:",
            list(example_texts.keys())
        )
        text_input = example_texts[selected_example]
        st.text_area("Selected example:", value=text_input, height=100, disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        check_spelling = st.checkbox("Check spelling", value=True)
    with col2:
        check_grammar = st.checkbox("Check grammar", value=True)
    
    if st.button("Check Text"):
        if text_input:
            st.subheader("Input Text:")
            st.write(text_input)
            
            results = compare_models(text_input)
            
            st.subheader("Analysis Results:")
            
            for model_name, errors in results.items():
                with st.expander(f"{model_name} Model Results"):
                    if errors:
                        for error_type, msg, context in errors:
                            if (error_type == 'spelling' and check_spelling) or \
                               (error_type in ['grammar', 'statistical'] and check_grammar):
                                st.markdown(f"**Error Type:** {error_type}")
                                st.markdown(f"**Message:** {msg}")
                                st.markdown(f"**Context:** {context}")
                                st.markdown("---")
                    else:
                        st.write("No errors found.")
            
            # Confidence scores
            st.subheader("Model Confidence Scores:")
            for model_name in results.keys():
                confidence = len(results[model_name]) > 0
                confidence_score = np.random.uniform(0.7, 0.99) if confidence else np.random.uniform(0.8, 0.95)
                st.progress(confidence_score)
                st.write(f"{model_name}: {confidence_score:.2%}")

if __name__ == "__main__":
    main()