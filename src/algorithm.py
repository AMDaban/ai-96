from . import resource_manager, constants
from copy import deepcopy


def get_next_state(state):
    print(get_weighted_conflict_count(state))


def get_weighted_conflict_count(state):
    classes_conflicts = 0
    professors_conflicts = 0
    free_time_conflicts = 0

    all_classes = deepcopy(resource_manager.get_classes())
    classes_count_template = {single_class: 0 for single_class in all_classes}

    all_professors = resource_manager.get_professors()
    professors_count_template = {professor: 0 for professor in all_professors}

    for day in state:
        for slot in state.get(day):

            classes_count = deepcopy(classes_count_template)
            professors_count = deepcopy(professors_count_template)

            for event in state.get(day).get(slot):
                classes_count.update({event[0]: classes_count.get(event[0]) + 1})
                professors_count.update({event[1]: professors_count.get(event[1]) + 1})

            for single_class in classes_count:
                if classes_count.get(single_class) > 1:
                    classes_conflicts += 1

            for single_professor in professors_count:
                if professors_count.get(single_professor) > 1:
                    professors_conflicts += 1

                if professors_count.get(single_professor) >= 1:
                    if resource_manager.get_professor_free_time(single_professor) \
                            .get(constants.week_days_map_reverse.get(day)) \
                            .get(slot) != 1:
                        free_time_conflicts += 1

    return professors_conflicts * 10 + classes_conflicts * 5 + free_time_conflicts * 2
