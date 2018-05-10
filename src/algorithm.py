from . import resource_manager, constants
from copy import deepcopy
import random


def get_next_state(state):
    current_conflicts = get_weighted_conflict_count(state)
    print("best found so far: ", current_conflicts, "conflicts")

    return_next_state = None

    all_subjects_map = {subject: 0 for subject in resource_manager.get_subjects()}
    subject_assigned_map = {subject: set({}) for subject in resource_manager.get_subjects()}

    for i in range(constants.subject_shuffle_threshold):
        target_subject = None
        current_min = constants.infinity
        for subject in all_subjects_map:
            if all_subjects_map.get(subject) < current_min:
                current_min = all_subjects_map.get(subject)
                target_subject = subject

        all_subjects_map.update({
            target_subject: all_subjects_map.get(target_subject) + 1
        })

        fprofs = resource_manager.get_masters_for(target_subject) - subject_assigned_map.get(target_subject)
        if len(fprofs) == 0:
            pass
        else:
            day_1 = None
            day_2 = None
            slot_1 = None
            slot_2 = None

            for day in state:
                for slot in state.get(day):
                    if target_subject in [cps[2] for cps in state.get(day).get(slot)]:
                        if day_1 is None:
                            day_1 = day
                            slot_1 = slot
                        else:
                            day_2 = day
                            slot_2 = slot

            target_master = fprofs.pop()
            next_state = deepcopy(state)

            index_1 = None
            for j in range(0, len(next_state.get(day_1).get(slot_1))):
                if next_state.get(day_1).get(slot_1)[j][2] == target_subject:
                    index_1 = j

            item_1_to_remove = next_state.get(day_1).get(slot_1)[index_1]
            next_state.get(day_1).get(slot_1).remove(item_1_to_remove)

            index_2 = None
            for j in range(0, len(next_state.get(day_2).get(slot_2))):
                if next_state.get(day_2).get(slot_2)[j][2] == target_subject:
                    index_2 = j

            item_2_to_remove = next_state.get(day_2).get(slot_2)[index_2]
            next_state.get(day_2).get(slot_2).remove(item_2_to_remove)

            next_state.get(day_1).get(slot_1).append((item_1_to_remove[0], target_master, item_1_to_remove[2]))
            next_state.get(day_2).get(slot_2).append((item_2_to_remove[0], target_master, item_2_to_remove[2]))

            subject_assigned_map.get(target_subject).add(target_master)

            next_state_conflicts = get_weighted_conflict_count(next_state)
            if next_state_conflicts < current_conflicts:
                return_next_state = deepcopy(next_state)
                current_conflicts = next_state_conflicts

    swaped_slots = set({})
    swapped_count = 0
    while swapped_count < constants.swapping_limit:

        random_day_1 = constants.week_days[random.randint(0, len(constants.week_days) - 1)]
        random_slot_1 = constants.day_time_slots[random.randint(0, len(constants.day_time_slots) - 1)]
        random_day_slot_1 = state.get(random_day_1).get(random_slot_1)
        random_index_1 = -1
        if len(random_day_slot_1) != 0:
            random_index_1 = random.randint(0, len(random_day_slot_1) - 1)

        random_day_2 = constants.week_days[random.randint(0, len(constants.week_days) - 1)]
        random_slot_2 = constants.day_time_slots[random.randint(0, len(constants.day_time_slots) - 1)]
        random_day_slot_2 = state.get(random_day_2).get(random_slot_2)
        random_index_2 = -1
        if len(random_day_slot_2) != 0:
            random_index_2 = random.randint(0, len(random_day_slot_2) - 1)

        is_ok = True

        if random_index_1 + random_index_2 <= -2:
            is_ok = False

        if (random_day_1, random_slot_1, random_index_1, random_day_2, random_slot_2, random_index_2) in swaped_slots:
            is_ok = False

        if (random_day_1, random_slot_1, random_index_1) == (random_day_2, random_slot_2, random_index_2):
            is_ok = False

        if is_ok:
            swapped_count += 1
            swaped_slots.add((random_day_1, random_slot_1, random_index_1, random_day_2, random_slot_2, random_index_2))

            next_state = deepcopy(state)

            item_1_to_remove = None
            if random_index_1 != -1:
                item_1_to_remove = next_state.get(random_day_1).get(random_slot_1)[random_index_1]

            item_2_to_remove = None
            if random_index_2 != -1:
                item_2_to_remove = next_state.get(random_day_2).get(random_slot_2)[random_index_2]

            if item_1_to_remove is not None:
                next_state.get(random_day_1).get(random_slot_1).remove(item_1_to_remove)

            if item_2_to_remove is not None:
                next_state.get(random_day_2).get(random_slot_2).remove(item_2_to_remove)

            if item_1_to_remove is not None:
                next_state.get(random_day_2).get(random_slot_2).append(item_1_to_remove)

            if item_2_to_remove is not None:
                next_state.get(random_day_1).get(random_slot_1).append(item_2_to_remove)

            next_state_conflicts = get_weighted_conflict_count(next_state)
            if next_state_conflicts < current_conflicts:
                return_next_state = deepcopy(next_state)
                current_conflicts = next_state_conflicts

    return return_next_state


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

    return \
        professors_conflicts * constants.p_w + classes_conflicts * constants.c_w + free_time_conflicts * constants.f_w
