max_score = 13  # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import load_student_code, format_error_message, exception_message_for_students, normalize_text, prettify_dictionary
#from test_cases_classes_final import class_test_cases
from collections.abc import Iterable
import pytest

def test_13_game_play_game(current_test_name, input_test_cases, class_test_cases):
    try:
        # Ensure test_cases is valid and iterable
        if not isinstance(input_test_cases, list):
            input_test_case = {"id_test_case": None}
            exception_message_for_students(ValueError("test_cases should be a list of dictionaries. Contact your professor."), input_test_case=input_test_case) 
            return  # Technically not needed, as exception_message_for_students throws a pytest.fail Error, but included for clarity that this ends the test.

        # Use the appropriate test case
        input_test_case = input_test_cases[0]
        inputs = input_test_case["inputs"]

        # Name of the class being tested:
        class_name = "Game"
        method_to_test = 'play_game'
        class_test_cases_payload = {'class_name': class_name}
        class_test_cases_payload['class_test_cases'] = class_test_cases.get(class_name)
        class_test_cases_payload['test_type'] = 'method_test'
        class_test_cases_payload['method_to_test'] = method_to_test

        # Load the student's code and test classes
        manager_payload = load_student_code(current_test_name, inputs, input_test_case, class_tests=class_test_cases_payload)

        # first check if there was an error trying to run the code
        if manager_payload.get('class_results').get('CLASS ERROR') is not None:
            pytest.fail(f"{exception_message_for_students(
                exception_data=manager_payload.get('class_results').get('CLASS ERROR'), 
                input_test_case=input_test_case,
                current_test_name=current_test_name,
                )}")

        class_results_list = manager_payload.get('class_results').get('class_test_cases')

        # loop through each class test case
        for class_result in class_results_list:
            
            # get results of the methods we are looking at:
            method_results_list = [method_result for method_result in class_result.get('method_test_cases') if method_result.get('function_name') == method_to_test]
            
            if not method_results_list:
                pytest.fail(f"{exception_message_for_students(ValueError("No method test cases were found. Contact your professor."), input_test_case, current_test_name)}")

            for method_result in method_results_list:
                # first check if there were any function errors when running the method:
                if method_result.get('FUNCTION ERROR') is not None:
                    pytest.fail(f"{exception_message_for_students(
                        exception_data=method_result.get('FUNCTION ERROR'), 
                        input_test_case=input_test_case,
                        current_test_name=current_test_name,
                        )}")
                    
                # I want to go through each variable that needsto be updated and check if it was updated for each home and away team.
                initial_game = method_result.get('initial_obj_state')[0].get('instance_variables')
                final_home = method_result.get('final_obj_state')[0].get('instance_variables').get('home_team').get('instance_variables')      
                final_away = method_result.get('final_obj_state')[0].get('instance_variables').get('away_team').get('instance_variables')
                final_game = method_result.get('final_obj_state')[0].get('instance_variables')

                updated_values = {
                    "updated_game_score": False,
                    "updated_wins": False,
                    "updated_losses": False,
                    "updated_goals_scored": False,
                    "updated_goals_allowed": False
                }

                if final_game.get('home_team_score') > 0 or final_game.get('away_team_score') > 0:
                    updated_values['updated_game_score'] = True 

                if final_home.get('_SoccerTeam__wins') == 1 or final_away.get('_SoccerTeam__wins') == 1:
                    updated_values['updated_wins'] = True

                if final_home.get('_SoccerTeam__losses') == 1 or final_away.get('_SoccerTeam__losses') == 1:
                    updated_values['updated_losses'] = True

                # because of no tie scores, they can't both be zero
                if final_home.get('goals_scored') > 0 or final_away.get('goals_scored') > 0:
                    updated_values['updated_goals_scored'] = True

                if final_home.get('goals_allowed') > 0 or final_away.get('goals_allowed')  > 0:
                    updated_values['updated_goals_allowed'] = True

                updated_values_str = prettify_dictionary(updated_values)
                inital_game_str = prettify_dictionary(initial_game)
                final_game_str = prettify_dictionary(final_game)

                assert False not in list(updated_values.values()), format_error_message(
                    custom_message=(f"The method \"{method_to_test}\" is meant to update the following:\n\n"
                                    f"VALUES THAT {method_to_test.upper()} SHOULD UPDATE:\n"
                                    f"---------------------------------------------------\n"
                                    f"{updated_values_str}\n\n"
                                    f"But any \"False\" values above mean you did not properly update that value for your Game (or the team objects inside the game)."
                                    f"Below are the starting values in the Game class, followed by the values after {method_to_test} "
                                    f"is run. Make sure the after values are all being updated as they should to be according to the instructions."
                                    f"BEFORE RUNNING {method_to_test.upper()}:\n"
                                    f"{"-"*len(f"BEFORE RUNNING {method_to_test.upper()}:")}\n"
                                    f"{inital_game_str}\n\n"
                                    f"AFTER RUNNING {method_to_test.upper()}:\n"
                                    f"{"-"*len(f"AFTER RUNNING {method_to_test.upper()}:")}\n"
                                    f"{final_game_str}\n\n"
                                    f"Make sure all the necessary variables are being updated, either in the Game's score, or the nested "
                                    f"soccer team objects."),
                    current_test_name=current_test_name,
                    input_test_case=input_test_case,
                    )


                # initial_value_found = False
                # student_var_name = None
                # normalized_expected_name = normalize_text(expected_update_variable_name)
                # normalized_expected_initial_value = normalize_text(expected_update_values.get('initial_value'))
                # normalized_expected_final_value = normalize_text(expected_update_values.get('final_value'))

                # initial_obj_state_vars = method_result.get('initial_obj_state')[run_index].get('instance_variables')
                # initial_state_vars_str = '\n'.join([f"{normalize_text(name)}: {normalize_text(value)}" for name, value in initial_obj_state_vars.items()])
                # for actual_var_name, initial_var_value in initial_obj_state_vars.items():
                #     # check the var names:
                #     normalized_actual_var_name = normalize_text(actual_var_name)
                #     expected_name_match = normalized_actual_var_name == normalized_expected_name

                #     # check the var values:
                #     normalized_actual_initial_var_value = normalize_text(initial_var_value)
                #     exepcted_value_match = normalized_actual_initial_var_value == normalized_expected_initial_value

                #     if expected_name_match and exepcted_value_match:
                #         initial_value_found = True
                #         student_var_name = actual_var_name
                #         normalized_student_var_name = normalize_text(student_var_name)
                #         break
                
                # for original, replacement in [('soccerteam', '__'), ('sponsoredteam', '__')]:
                #     normalized_expected_name = normalized_expected_name.replace(original, replacement)
                #     initial_state_vars_str= initial_state_vars_str.replace(original, replacement)
                # assert initial_value_found, format_error_message(
                #     custom_message=(f"The method \"{method_to_test}\" is provided with the following argument(s) other than \"self\":\n\n"
                #                     f"METHOD ARGUMENTS:\n"
                #                     f"-----------------\n"
                #                     f"{test_inputs_str}\n\n"
                #                     f"The {class_name} object is expected to start out with the following variable and value (ignoring capitalization / punctuation):\n\n"
                #                     f"EXPECTED INITIAL VALUE:\n"
                #                     f"-----------------------\n"
                #                     f"{normalized_expected_name}: {normalized_expected_initial_value}\n\n"
                #                     f"But no variables could be found that matched that name.\n\n"
                #                     f"Make sure you are actually adding instance variables to the object by using \"self\". "
                #                     f"Double check that you are following the logic provided in the instructions.\n\n"
                #                     f"Here are all the variables the test could find in your {class_name} object (ignoring capitalization / punctuation):\n\n"
                #                     f"YOUR VARIABLES IN {class_name.upper()}:\n"
                #                     f"{"-"*len("YOUR VARIABLES IN " + class_name + ":")}\n"
                #                     f"{initial_state_vars_str}"),
                #     current_test_name=current_test_name,
                #     input_test_case=input_test_case,
                #     )
                
                # normalized_actual_final_value = normalize_text(method_result.get('final_obj_state')[run_index].get('instance_variables').get(student_var_name))
                
                # for original, replacement in [('soccerteam', '__'), ('sponsoredteam', '__')]:
                #     normalized_student_var_name = normalized_student_var_name.replace(original,replacement)

                # assert normalized_actual_final_value == normalized_expected_final_value, format_error_message(
                #     custom_message=(f"The method {method_to_test} is provided with the following argument(s) other than \"self\":\n\n"
                #                     f"METHOD ARGUMENTS:\n"
                #                     f"-----------------\n"
                #                     f"{test_inputs_str}\n\n"
                #                     f"It is expected to update the {class_name} object in the following way (ignoring capitalization / punctuation):\n\n"
                #                     f"EXPECTED INITIAL VALUE:\n"
                #                     f"-----------------------\n"
                #                     f"{normalized_expected_name}: {normalized_expected_initial_value}\n\n"
                #                     f"SHOULD BECOME EXPECTED FINAL VALUE:\n"
                #                     f"-----------------------------------\n"
                #                     f"{normalized_expected_name}: {normalized_expected_final_value}\n\n"
                #                     f"In your {class_name} object, this was your initial value:\n\n"
                #                     f"YOUR INITIAL VALUE:\n"
                #                     f"-------------------\n"
                #                     f"{normalized_student_var_name}: {normalized_actual_initial_var_value}\n\n"
                #                     f"But the final value of {normalized_student_var_name} after calling the method {method_to_test} was:\n\n"
                #                     f"YOUR FINAL VALUE:\n"
                #                     f"-----------------\n"
                #                     f"{normalized_student_var_name}: {normalized_actual_final_value}\n\n"
                #                     f"If your initial and final value are the same, make sure you are actually updating the object by changing an instance variable through \"self\". "
                #                     f"Otherwise, double check that you are following the logic provided in the instructions."),
                #     current_test_name=current_test_name,
                #     input_test_case=input_test_case,
                #     )        
    
    except AssertionError:
        raise
    except Exception as e:
        exception_message_for_students(e, input_test_case, current_test_name)

