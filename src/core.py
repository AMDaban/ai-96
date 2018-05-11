from . import resource_manager, constants, excel_generator, algorithm
from copy import deepcopy

initial_state = None


def start_processing():
    global initial_state

    create_initial_state()

    depth = 0
    while depth < constants.max_algorithm_depth:
        next_state = algorithm.get_next_state(initial_state)

        if next_state is None:
            break
        else:
            initial_state = deepcopy(next_state)

        depth += 1


def create_initial_state():
    create_data_structure()
    fill_initial_state()


def create_result_excel_file():
    excel_generator.create_result(initial_state, "resources/result.xlsx")
    print("best result so far generated")


def create_data_structure():
    global initial_state

    initial_state = {
        day: {
            slot: [] for slot in constants.day_time_slots
        } for day in constants.week_days
    }


def fill_initial_state():
    global initial_state

    professors_free_time_count_map = resource_manager.get_professors_free_time_count()
    temp_professors_free_time_map = deepcopy(resource_manager.free_times_map)
    temp_subject_list = deepcopy(resource_manager.get_subjects())

    assigned_subjects = set([])

    for subject in temp_subject_list:
        subject_masters = resource_manager.get_masters_for(subject)
        is_subject_assigned = False
        for master in subject_masters:
            if not is_subject_assigned:
                if professors_free_time_count_map.get(master) >= 2:
                    is_subject_assigned = True
                    assigned_subjects.add(subject)

                    assigned_slots = 0
                    for day in temp_professors_free_time_map.get(master):
                        for slot in temp_professors_free_time_map.get(master).get(day):
                            if assigned_slots < 2:
                                if temp_professors_free_time_map.get(master).get(day).get(slot) != 0:
                                    free_classes = get_free_classes(
                                        initial_state,
                                        constants.week_days_map.get(day),
                                        slot
                                    )
                                    if free_classes != set([]):
                                        temp_tuple = (free_classes.pop(), master, subject)
                                        initial_state.get(constants.week_days_map.get(day)).get(slot).append(temp_tuple)
                                        assigned_slots = assigned_slots + 1
                                        professors_free_time_count_map.update({
                                            master: professors_free_time_count_map.get(master) - 1
                                        })
                                        temp_professors_free_time_map.get(master).get(day).update({
                                            slot: 0
                                        })

                    if assigned_slots < 2:
                        for day in temp_professors_free_time_map.get(master):
                            for slot in temp_professors_free_time_map.get(master).get(day):
                                if assigned_slots < 2:
                                    if temp_professors_free_time_map.get(master).get(day).get(slot) != 0:
                                        temp_tuple = ((deepcopy(resource_manager.classes_set)).pop(), master, subject)
                                        initial_state.get(constants.week_days_map.get(day)).get(slot).append(temp_tuple)
                                        assigned_slots = assigned_slots + 1
                                        professors_free_time_count_map.update({
                                            master: professors_free_time_count_map.get(master) - 1
                                        })
                                        temp_professors_free_time_map.get(master).get(day).update({
                                            slot: 0
                                        })

    remaining_subjects = set(temp_subject_list) - assigned_subjects
    for subject in remaining_subjects:
        subject_masters = resource_manager.get_masters_for(subject)
        is_subject_assigned = False
        for master in subject_masters:
            if not is_subject_assigned:
                is_subject_assigned = True

                assigned_slots = 0
                for day in temp_professors_free_time_map.get(master):
                    for slot in temp_professors_free_time_map.get(master).get(day):
                        if assigned_slots < 2:
                            temp_tuple = ((deepcopy(resource_manager.classes_set)).pop(), master, subject)
                            initial_state.get(constants.week_days_map.get(day)).get(slot).append(temp_tuple)
                            assigned_slots = assigned_slots + 1


def get_free_classes(state, day, slot):
    filled_classes = set([class_professor_subject[0] for class_professor_subject in state.get(day).get(slot)])
    all_classes = deepcopy(resource_manager.classes_set)
    return all_classes - filled_classes
