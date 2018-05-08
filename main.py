from src import resource_manager, core

resource_manager.load_resources(
    professor_skills="resources/Prof_Skill.xlsx",
    classes="resources/Amoozesh.xlsx",
    subjects="resources/subjects.xlsx",
    free_times="resources/Proffosor_FreeTime.xlsx"
)


core.start_processing()
