max_score = 5  # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import load_student_code, format_error_message, exception_message_for_students, normalize_text, prettify_dictionary
#from test_cases_classes_final import class_test_cases
from collections.abc import Iterable
import pytest, re

# Checks if the expected printed messages actually appear, but doesn't check for specific inputs or correct calculations.
def test_14_no_tie_scores(current_test_name, input_test_cases):
    try:
        # Ensure test_cases is valid and iterable
        if not isinstance(input_test_cases, list):
            input_test_case = {"id_input_test_case": None}
            exception_message_for_students(ValueError("input_test_cases should be a list of dictionaries. Contact your professor."), input_test_case, current_test_name) 
            return  # Technically not needed, as exception_message_for_students throws a pytest.fail Error, but included for clarity that this ends the test.

        for input_test_case in input_test_cases:
            
            inputs = input_test_case["inputs"]
            matching_numbers_found = False
            num_repeat_iterations = 5

            # repeat test case 50 times, should have a 99.9999% chance of finding a tie score if it exists.
            for _ in range(num_repeat_iterations):
                manager_payload = load_student_code(current_test_name, inputs, input_test_case)

                captured_output = manager_payload.get('captured_output')
                captured_lines = captured_output.splitlines()
                normalized_captured_lines = [normalize_text(line) for line in captured_lines]
                normalized_game_results = [line for line in normalized_captured_lines if 'results of game' in line]
                # first catch if they ever print out actual tie scores:
                for line in normalized_game_results:

                    number_pair = set(find_last_two_integers(line))
                    if len(number_pair) == 1:
                        matching_numbers_found = True
                        break

                if matching_numbers_found:
                    break
                    
            assert not matching_numbers_found, format_error_message(
                custom_message=(f"Your code doesn't prevent tie scores for the home and away teams.\n\n"
                                f"These scores were generated during your code:.\n\n"
                                f"{line}\n\n"
                                f"Make sure you either continue generating the scores when there is a tie until "
                                f"there is no longer a tie, or you find a way to never generate tie scores to begin with."),
                current_test_name=current_test_name,
                input_test_case=input_test_case,
                display_inputs=True,
            )

    # assert raises an AssertionError, but I don't want to actually catch it
    # this is just so I can have another Exception catch below it in case
    # anything else goes wrong.
    except AssertionError:
        raise
    
    except Exception as e:
        # Handle other exceptions
        exception_message_for_students(e, input_test_case)

def find_last_two_integers(input_string):
    # Find all integers in the string
    numbers = re.findall(r'\d+', input_string)
    
    # If there are at least two numbers, get the last two; otherwise return what we have
    if len(numbers) >= 2:
        return int(numbers[-2]), int(numbers[-1])
    elif len(numbers) == 1:
        return int(numbers[0]),
    else:
        return None  # Return None if no integers found



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