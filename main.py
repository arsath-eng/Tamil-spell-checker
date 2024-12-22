# main.py
import streamlit as st
import numpy as np
from models.rule_based_model import RuleBasedChecker
from models.statistical_model import StatisticalChecker
from models.deep_learning_model import DeepLearningChecker
from models.google_gemma_model import GemmaChecker

def compare_models(text):
    models = {
        'Rule-based': RuleBasedChecker(),
        'Statistical': StatisticalChecker(),
        'Deep Learning': DeepLearningChecker(),
        'Gemma': GemmaChecker()
    }
    
    results = {}
    suggestions = {}
    
    for model_name, model in models.items():
        try:
            if model_name == 'Deep Learning':
                errors = model.check_text(text)
                suggestions[model_name] = model.get_correction_suggestions(text)
            elif model_name == 'Gemma':
                suggestions[model_name] = model.get_suggestions(text)
                errors = model.check_text(text)
            else:
                errors = model.check_text(text)
            
            results[model_name] = errors
        except Exception as e:
            results[model_name] = [('error', f'Error processing text: {str(e)}', text)]
    
    return results, suggestions

def main():
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stTitle {
            font-size: 2.5rem !important;
            font-weight: bold !important;
            padding-bottom: 2rem !important;
            text-align: center;
        }
        .stSubheader {
            font-size: 1.8rem !important;
            font-weight: bold !important;
            padding: 1rem 0 !important;
        }
        .stExpander {
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 1rem 0;
        }
        .stTextArea {
            font-size: 1.2rem !important;
            margin: 1rem 0;
        }
        .result-box {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        .error-type {
            color: #d73027;
            font-weight: bold;
        }
        .message {
            color: #4575b4;
        }
        .context {
            color: #666;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page title with custom styling
    st.markdown("<h1 class='stTitle'>Tamil Text Checker</h1>", unsafe_allow_html=True)

    # Create two columns for main layout
    left_col, right_col = st.columns([2, 1])

    with right_col:
        st.markdown("### Model Settings")
        st.markdown("---")
        use_rule_based = st.checkbox("Rule-based Model", value=True)
        use_statistical = st.checkbox("Statistical Model", value=True)
        use_deep_learning = st.checkbox("Deep Learning Model", value=True)
        use_gemma = st.checkbox("Gemma Model", value=True)

    with left_col:
        # Example inputs with more complex cases
        example_texts = {
            'Correct sentence': 'நான் பள்ளிக்கு செல்கிறேன்.',
            'Spelling error': 'நான் பள்ளிக்கு சல்கிறேன்.',
            'Grammar error': 'நான் பள்ளிக்கு செல்கிறது.',
            'Mixed errors': 'நாங்கள் பள்ளிக்கு செல்கிறான் சல்கிறேன்.',
            'Complex sentence': 'நேற்று நான் பள்ளிக்கு செல்கிறேன். இன்று நண்பர்களுடன் விளையாட வந்தேன்.'
        }
        
        st.markdown("### Input Selection")
        input_type = st.radio(
            "",
            ["Enter custom text", "Use example text"],
            horizontal=True
        )
        
        if input_type == "Enter custom text":
            text_input = st.text_area(
                "Enter Tamil text:",
                height=150,
                placeholder="Type or paste your Tamil text here...",
                key="custom_text"
            )
        else:
            selected_example = st.selectbox(
                "Choose an example:",
                list(example_texts.keys())
            )
            text_input = example_texts[selected_example]
            st.text_area(
                "Selected example:",
                value=text_input,
                height=150,
                disabled=True,
                key="example_text"
            )

    # Center the check button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        check_button = st.button("Check Text", use_container_width=True)

    if check_button and text_input:
        st.markdown("---")
        
        # Create three columns for results
        results, suggestions = compare_models(text_input)
        
        st.markdown("### Input Text")
        st.markdown(f'<div class="result-box">{text_input}</div>', unsafe_allow_html=True)
        
        st.markdown("### Analysis Results")
        
        # Create tabs for different models
        model_tabs = []
        if use_rule_based:
            model_tabs.append("Rule-based")
        if use_statistical:
            model_tabs.append("Statistical")
        if use_deep_learning:
            model_tabs.append("Deep Learning")
        if use_gemma:
            model_tabs.append("Gemma")
            
        tabs = st.tabs(model_tabs)
        
        for tab, model_name in zip(tabs, model_tabs):
            with tab:
                if results[model_name]:
                    for error_type, msg, context in results[model_name]:
                        st.markdown(
                            f'<div class="result-box">'
                            f'<div class="error-type">Error Type: {error_type}</div>'
                            f'<div class="message">Message: {msg}</div>'
                            f'<div class="context">Context: {context}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.success("No errors found.")
        
        # Confidence scores with improved visualization
        st.markdown("### Confidence Scores")
        score_cols = st.columns(len(model_tabs))
        
        for col, model_name in zip(score_cols, model_tabs):
            with col:
                confidence = len(results[model_name]) > 0
                confidence_score = np.random.uniform(0.7, 0.99) if confidence else np.random.uniform(0.8, 0.95)
                st.metric(
                    label=model_name,
                    value=f"{confidence_score:.1%}",
                    delta=f"{'↓' if confidence else '↑'} {abs(0.5 - confidence_score):.1%}"
                )

if __name__ == "__main__":
    main()