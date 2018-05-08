from . import resource_manager, constants
from copy import deepcopy

initial_state = None


def start_processing():
    create_initial_state()


def create_initial_state():
    create_data_structure()
    fill_initial_state()

    print(initial_state)


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
    for subject in temp_subject_list:
        subject_masters = resource_manager.get_masters_for(subject)
        for master in subject_masters:
            if professors_free_time_count_map.get(master) >= 2:
                assigned_slots = 0

                for day in temp_professors_free_time_map.get(master):
                    for slot in temp_professors_free_time_map.get(master).get(day):
                        if assigned_slots < 2:
                            if temp_professors_free_time_map.get(master).get(day).get(slot) != 0:
                                free_classes = get_free_classes(initial_state, constants.week_days_map.get(day), slot)
                                if free_classes != set([]):
                                    temp_tuple = (free_classes.pop(), master, subject)
                                    initial_state.get(constants.week_days_map.get(day)).get(slot).append(temp_tuple)
                                    assigned_slots = assigned_slots + 1
                                    professors_free_time_count_map.update({
                                        master: professors_free_time_count_map.get(master) - 1
                                    })

                for day in temp_professors_free_time_map.get(master):
                    for slot in temp_professors_free_time_map.get(master).get(day):
                        if assigned_slots < 2:
                            if temp_professors_free_time_map.get(master).get(day).get(slot) != 0:
                                free_classes = get_free_classes(initial_state, constants.week_days_map.get(day), slot)
                                temp_tuple = (free_classes.pop(), master, subject)
                                initial_state.get(constants.week_days_map.get(day)).get(slot).append(temp_tuple)
                                assigned_slots = assigned_slots + 1
                                professors_free_time_count_map.update({
                                    master: professors_free_time_count_map.get(master) - 1
                                })


def get_free_classes(state, day, slot):
    filled_classes = set([class_professor_subject[0] for class_professor_subject in state.get(day).get(slot)])
    all_classes = deepcopy(resource_manager.classes_set)
    return all_classes - filled_classes



