max_score = 10  # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_student_code, format_error_message, exception_message_for_students, round_match, get_similarity_feedback
import re

# Checks if the expected printed messages actually appear, but doesn't check for specific inputs or correct calculations.
def test_02_printed_messages(current_test_name, input_test_cases):
    try:
        # Ensure test_cases is valid and iterable
        if not isinstance(input_test_cases, list):
            input_test_case = {"id_input_test_case": None}
            exception_message_for_students(ValueError("input_test_cases should be a list of dictionaries. Contact your professor."), input_test_case, current_test_name) 
            return  # Technically not needed, as exception_message_for_students throws a pytest.fail Error, but included for clarity that this ends the test.

        for input_test_case in input_test_cases:
            
            inputs = input_test_case["inputs"]
            expected_printed_messages = input_test_case["printed_messages"]
            invalid_printed_messages = input_test_case["invalid_printed_messages"]
            # Load in the student's code and capture output
            manager_payload = load_student_code(current_test_name, inputs, input_test_case)

            captured_output = manager_payload.get('captured_output')
            captured_lines = captured_output.splitlines()
            # Normalize the captured input prompts to remove spaces, punctuation, and symbols
            normalized_captured_print_statements_list = [replacing_date_and_numbers(normalize_text(captured_print)) for captured_print in captured_lines]
            normalized_captured_print_statements_str = ' '.join(normalized_captured_print_statements_list)
            normalized_captured_print_statements_list = list(dict.fromkeys(normalized_captured_print_statements_list)) # get rid of duplicates
            # create string of all print statements to search for for matches.
            
            # create a version for error messages if needed
            error_message_print_statements = [f'{index}: "{output}"' for index, output in enumerate(normalized_captured_print_statements_list, start=1)]
            # create string version for error messages if needed
            error_message_print_statements_str = '\n'.join(error_message_print_statements)
            
            # Check that each required phrase (regex pattern) is found in the normalized captured output
            for expected_phrase in expected_printed_messages:
                expected_phrase = replacing_date_and_numbers(normalize_text(expected_phrase))

                # Skip over phrases that should only sometimes print
                phrases_to_skip = ["qualified for the ncaa soccer tournament", "you had a good season", "your team needs to practice"]
                skip_iteration = False
                for skip_phrase in phrases_to_skip:
                    if skip_phrase in expected_phrase:
                        skip_iteration = True
                        break
                if skip_iteration:
                    continue

                # Check if the pattern exists in the normalized captured print statements
                match = re.search(expected_phrase, normalized_captured_print_statements_str)

                # if there isn't a match, prepare the strings for the failure message to make it less confusing.
                if not match:
                    similarity_message = get_similarity_feedback(expected_phrase, normalized_captured_print_statements_list)

                assert match, format_error_message(
                    custom_message=("The expected printed message (ignoring punctuation / capitalization):\n\n"
                                    f"\"{expected_phrase}\"\n\n"
                                    f"wasn't printed in your code.\n\n"
                                    f"HOW TO FIX IT:\n"
                                    f"--------------\n"
                                    f"There are 3 likely causes:\n"
                                    f"-   1. You made a spelling error.\n"
                                    f"-   2. You forgot to include the expected printed message.\n"
                                    f"-   3. You included the printed message and spelled it correctly, but because of some logic in your code (like an improper if statement) it doesn't appear when it should.\n\n"
                                    f"POSSIBLE SPELLING MISTAKES:\n"
                                    f"---------------------------\n"
                                    f"{similarity_message}\n\n"
                                    f"ALL YOUR PRINTED OUTPUT:\n"
                                    f"------------------------\n"
                                    f"Below are all the unique printed messages from your code (ignoring punctuation / capitalization):\n\n"
                                    f"{error_message_print_statements_str}\n\n"),
                    current_test_name=current_test_name,
                    input_test_case=input_test_case,
                    display_inputs=True,
                )

            # Ensure none of the invalid phrases are found in the normalized captured output
            for invalid_phrase in invalid_printed_messages:
                invalid_phrase = normalize_text(invalid_phrase)

                # Skip over phrases that should only sometimes print
                phrases_to_skip = ["qualified for the ncaa soccer tournament", "you had a good season", "your team needs to practice", "game info menu", "team info menu"]
                skip_iteration = False
                for skip_phrase in phrases_to_skip:
                    if skip_phrase in invalid_phrase:
                        skip_iteration = True
                        break
                if skip_iteration:
                    continue

                regex_pattern = invalid_phrase.replace("<wildcard>", r".+?")
                match = re.search(regex_pattern, normalized_captured_print_statements_str)

                assert not match, format_error_message(
                    custom_message=("You used an invalid printed message (ignoring punctuation / capitalization):\n\n"
                                    f"\"{invalid_phrase}\"\n\n"
                                    f"HOW TO FIX IT:\n"
                                    f"--------------\n"
                                    f"Most likely:\n"
                                    f"-   1. You are printing something that should be inside an if statement or while loop, but isn't.\n"
                                    f"-   2. You are printing something that IS in an if statement or while loop, but you wrote the logic incorrectly so it appears when it shouldn't.\n"
                                    f"ALL YOUR PRINTED OUTPUT:\n"
                                    f"------------------------\n"
                                    f"Below are all the unique printed messages from your code (ignoring punctuation / capitalization):\n\n"
                                    f"{error_message_print_statements_str}\n\n"),
                    current_test_name=current_test_name,
                    input_test_case=input_test_case,
                    display_inputs=True
                )
    # assert raises an AssertionError, but I don't want to actually catch it
    # this is just so I can have another Exception catch below it in case
    # anything else goes wrong.
    except AssertionError:
        raise
    
    except Exception as e:
        # Handle other exceptions
        exception_message_for_students(e, input_test_case)

def replacing_date_and_numbers(message):
    if 'results of game' in message:
        message = re.sub(r'\b(\d{4}) (\d{2}) (\d{2})\b', '<date>', message)
        # Find all digit matches after replacing the date
        digit_matches = list(re.finditer(r'\d+', message))

        # Only replace the last two occurrences of numbers if there are at least two matches
        if len(digit_matches) >= 2:
            for match in reversed(digit_matches[-2:]):
                start, end = match.span()
                message = message[:start] + "<number>" + message[end:]
    elif 'team name' in message:
        message = re.sub(r'\d+', r'\\d+', message)
    return message
            