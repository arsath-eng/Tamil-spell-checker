# Tamil Text Checker

A comprehensive tool for checking Tamil text spelling, grammar, and overall correctness using multiple AI models.

<img src="screenshots/5-correct word/1.png" width="600" alt="Homepage Screenshot">


## Features

- Multiple model support:
  - Rule-based checking
  - Deep Learning analysis (using Indic-BERT)
  - Statistical analysis
  - Google Gemma integration
- Real-time error detection
- Spelling and grammar correction
- Confidence scores for each model
- User-friendly Streamlit interface

## Screenshots

### Main Interface
 <img src="screenshots/1-Spelling Errors (Intentional misspellings)/1.png" width="600" alt="Homepage Screenshot">

### Example Selection
<img src="screenshots/1-Spelling Errors (Intentional misspellings)/2.png" width="600" alt="Homepage Screenshot">

### Analysis Results
<img src="screenshots/1-Spelling Errors (Intentional misspellings)/3.png" width="600" alt="Homepage Screenshot">

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arsath-eng/Tamil-spell-checker.git
cd Tamil-spell-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your GROQ_API_KEY
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Access the web interface at `http://localhost:8501`

3. Choose your input method:
   - Enter custom text
   - Use example text

4. Select checking options:
   - Spelling check
   - Grammar check

5. Click "Check Text" to analyze

## Model Details

### Rule-Based Model
- Uses predefined Tamil dictionary and grammar rules
- Fast and deterministic results
- Best for basic spelling and grammar checks

### Deep Learning Model
- Powered by AI4Bharat's Indic-BERT
- Handles complex language patterns
- Suitable for nuanced grammar analysis

### Statistical Model
- Uses TF-IDF and Naive Bayes classification
- Trained on correct Tamil text samples
- Good for identifying unusual patterns

### Google Gemma Integration
- Leverages Groq's Gemma 2B model
- Provides detailed language insights
- Offers correction suggestions

## Example Use Cases

1. Basic Spelling Check:
```tamil
Input: நான் பள்ளிக்கு சல்கிறேன்
Output: Spelling error detected in "சல்கிறேன்" - Suggested: "செல்கிறேன்"
```

2. Grammar Check:
```tamil
Input: நான் பள்ளிக்கு செல்கிறார்கள்
Output: Grammar error - Subject-verb agreement mismatch
```

## Project Structure
```
tamil-text-checker/
├── main.py
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── rule_based_model.py
│   ├── deep_learning_model.py
│   ├── statistical_model.py
│   └── google_gemma_model.py
├── data/
│   └── tamil_words.txt
└── .env
```

## Dependencies

Main dependencies include:
- streamlit >= 1.24.0
- indic-nlp-library >= 0.91
- transformers >= 4.30.2
- torch >= 2.2.0
- tensorflow >= 2.13.0
- scikit-learn >= 1.2.2
- Groq API client
- python-dotenv

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## Acknowledgments

- AI4Bharat for the Indic-BERT model
- Indic NLP Library contributors
- Groq for the Gemma model API
- Tamil language experts who helped validate the rule sets


