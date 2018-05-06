from openpyxl import load_workbook
from functools import reduce

professor_skills_map = None
lessons_list = None
classes_list = None
subject_list = None
free_times_map = None


def load_resources(professor_skills, classes, subjects, free_times):
    load_professor_skills(professor_skills_file_name=professor_skills)
    load_classes(classes_file_name=classes)
    load_subjects(subject_file_name=subjects)
    load_free_times(free_times_file_name=free_times)


def load_professor_skills(professor_skills_file_name):
    global professor_skills_map, lessons_list

    prof_skills = load_workbook(professor_skills_file_name)
    prof_skills_sheet = prof_skills.active

    professors = prof_skills_sheet.iter_rows(
        min_row=2,
        min_col=1,
        max_row=prof_skills_sheet.max_row,
        max_col=prof_skills_sheet.max_column
    )

    professor_skills_map = {
        professor[0].value: [skill.value for skill in professor[1:]] for professor in professors
    }

    lessons = prof_skills_sheet.iter_rows(
        min_row=1,
        min_col=2,
        max_row=1,
        max_col=prof_skills_sheet.max_column
    )

    lessons_list = list(
        map(
            lambda x: x.value,
            reduce(
                lambda x, y: x.append(y),
                [row for row in lessons]
            )
        )
    )


def get_professor_skills(professor):
    global professor_skills_map

    if professor_skills_map is not None:
        return professor_skills_map.get(professor, None)
    else:
        return None


def load_classes(classes_file_name):
    global classes_list

    classes_work_book = load_workbook(classes_file_name)
    classes_sheet = classes_work_book.active

    classes = classes_sheet.iter_rows(
        min_row=1,
        min_col=1,
        max_row=classes_sheet.max_row,
        max_col=classes_sheet.max_column
    )

    classes_list = list(
        map(
            lambda x: x.value,
            reduce(
                (lambda x, y: x.append(y)),
                [row for row in classes]
            )
        )
    )


def get_classes():
    global classes_list

    return classes_list


def load_subjects(subject_file_name):
    global subject_list

    subjects_work_book = load_workbook(subject_file_name)
    subject_sheet = subjects_work_book.active

    subjects = subject_sheet.iter_rows(
        min_row=1,
        min_col=1,
        max_row=subject_sheet.max_row,
        max_col=subject_sheet.max_column
    )

    subject_list = list(
        map(
            lambda x: x.value,
            reduce(
                lambda x, y: x.append(y),
                [row for row in subjects]
            )
        )
    )


def get_subjects():
    global subject_list

    return subject_list


def load_free_times(free_times_file_name):
    global free_times_map

    free_times_work_book = load_workbook(free_times_file_name)

    free_times_map = {}

    for professor_free_time_sheet in free_times_work_book:
        sheet_rows = professor_free_time_sheet.iter_rows(
            min_row=2,
            min_col=2,
            max_row=professor_free_time_sheet.max_row,
            max_col=professor_free_time_sheet.max_column
        )

        professor_week_free_time = [
            tuple(
                [time_slot.value for time_slot in row]
            ) for row in sheet_rows
        ]

        free_times_map.update(
            {
                professor_free_time_sheet.title:
                    tuple(professor_week_free_time)
            }
        )


def get_professor_free_time(professor):
    global free_times_map

    if free_times_map is not None:
        return free_times_map.get(professor, None)
    else:
        return None
