from main import TamilChecker
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

test_cases = [
    {
        "title": "Spelling Errors Sample",
        "text": "நான பள்ளிக்கு சென்றேன்",  # நான் is correct
        "expected_correction": "நான் பள்ளிக்கு சென்றேன்",
        "error_types": ["spelling"]
    },
    {
        "title": "Vowel Mark Error",
        "text": "புத்தகத்தெ படித்தேன்",  # புத்தகத்தை is correct
        "expected_correction": "புத்தகத்தை படித்தேன்",
        "error_types": ["spelling"]
    },
    {
        "title": "Grammar Error - Subject-Verb Agreement",
        "text": "அவர்கள் வருகிறான்",  # வருகிறார்கள் is correct
        "expected_correction": "அவர்கள் வருகிறார்கள்",
        "error_types": ["grammar"]
    },
    {
        "title": "Mixed Errors",
        "text": "நாங்கள் சினிமாவுக்கு போனோம்",  # திரைப்படத்திற்கு is more formal
        "expected_correction": "நாங்கள் திரைப்படத்திற்கு போனோம்",
        "error_types": ["spelling", "grammar"]
    },
    {
        "title": "Complex Sentence",
        "text": "அவன் நல்ல புத்தகத்தெ எழுதினான் ஆனா யாரும் படிக்கவில்லை",
        "expected_correction": "அவன் நல்ல புத்தகத்தை எழுதினான் ஆனால் யாரும் படிக்கவில்லை",
        "error_types": ["spelling", "grammar"]
    }
]

class TestResults:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

def format_error(error):
    """Format error tuple into readable string"""
    error_type, message, context = error
    return f"{error_type}: {message} (Context: {context})"

def compare_text(original, corrected, expected):
    """Compare corrected text with expected correction"""
    return corrected.strip() == expected.strip()

def run_tests(checker):
    results = TestResults()
    print(f"{Fore.CYAN}Running Tamil Text Checker Tests{Style.RESET_ALL}\n")

    for i, test in enumerate(test_cases, 1):
        results.total_tests += 1
        print(f"{Fore.YELLOW}Test Case {i}: {test['title']}{Style.RESET_ALL}")
        print(f"Input Text: {test['text']}")
        
        # Collect all errors
        all_errors = []
        
        # Get spelling corrections
        spell_corrections = checker.spell_check(test['text'])
        if spell_corrections:
            all_errors.extend(spell_corrections)
            print(f"\n{Fore.BLUE}Spelling Corrections:{Style.RESET_ALL}")
            for error in spell_corrections:
                print(f"- {format_error(error)}")
        else:
            print(f"\n{Fore.GREEN}No spelling errors found{Style.RESET_ALL}")
            
        # Get grammar errors
        grammar_errors = checker.check_grammar(test['text'])
        if grammar_errors:
            all_errors.extend(grammar_errors)
            print(f"\n{Fore.BLUE}Grammar Suggestions:{Style.RESET_ALL}")
            for error in grammar_errors:
                print(f"- {format_error(error)}")
        else:
            print(f"\n{Fore.GREEN}No grammar errors found{Style.RESET_ALL}")

        # Apply corrections
        corrected_text = test['text']
        for error in all_errors:
            if isinstance(error[1], str) and isinstance(error[2], str):
                corrected_text = corrected_text.replace(error[2], error[1])

        print(f"\nCorrected Output: {corrected_text}")
        print(f"Expected Output: {test['expected_correction']}")

        # Check if correction matches expected output
        if compare_text(test['text'], corrected_text, test['expected_correction']):
            results.passed_tests += 1
            print(f"{Fore.GREEN}✓ Test Passed{Style.RESET_ALL}")
        else:
            results.failed_tests += 1
            print(f"{Fore.RED}✗ Test Failed{Style.RESET_ALL}")
            
        # Check if all expected error types were found
        found_error_types = set(error[0] for error in all_errors)
        expected_error_types = set(test['error_types'])
        if not expected_error_types.issubset(found_error_types):
            missed_types = expected_error_types - found_error_types
            print(f"{Fore.RED}Missing error types: {missed_types}{Style.RESET_ALL}")
            
        print(f"{Fore.YELLOW}{'-' * 50}{Style.RESET_ALL}\n")

    # Print summary
    print(f"\n{Fore.CYAN}Test Summary:{Style.RESET_ALL}")
    print(f"Total Tests: {results.total_tests}")
    print(f"Passed: {Fore.GREEN}{results.passed_tests}{Style.RESET_ALL}")
    print(f"Failed: {Fore.RED}{results.failed_tests}{Style.RESET_ALL}")
    print(f"Success Rate: {Fore.YELLOW}{(results.passed_tests/results.total_tests)*100:.2f}%{Style.RESET_ALL}")

def main():
    try:
        checker = TamilChecker()
        run_tests(checker)
    except Exception as e:
        print(f"{Fore.RED}Error running tests: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()