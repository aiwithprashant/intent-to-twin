import json


def compute_error_reduction(error_list):
    if not error_list:
        return 0

    initial = error_list[0]
    final = error_list[-1]

    if initial == 0:
        return 1.0

    return (initial - final) / initial


def compute_validity(errors, num_objects):
    if num_objects == 0:
        return 0

    return 1 - (len(errors) / num_objects)


def compute_convergence(iterations):
    return iterations


def compute_constraint_satisfaction(errors, constraints):
    violated = len(errors)
    total = len(constraints)

    if total == 0:
        return 1.0

    return 1 - (violated / total)