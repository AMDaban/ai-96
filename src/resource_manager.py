from openpyxl import load_workbook
from functools import reduce

professor_skills_map = None
lessons_list = None
classes_list = None


def load_resources(professor_skills, classes):
    load_professor_skills(professor_skills_file_name=professor_skills)
    load_classes(classes_file_name=classes)


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

    lessons_list = []

    for item in lessons:
        for lesson in item:
            lessons_list.append(lesson.value)


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
