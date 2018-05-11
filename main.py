from src import resource_manager, core, constants, algorithm

least_confs = constants.infinity

for i in range(constants.total_rounds):
    print("round: ", i)

    resource_manager.load_resources(
        professor_skills="resources/Prof_Skill.xlsx",
        classes="resources/Amoozesh.xlsx",
        subjects="resources/subjects.xlsx",
        free_times="resources/Proffosor_FreeTime.xlsx"
    )

    core.start_processing()
    if algorithm.get_weighted_conflict_count(core.initial_state) < least_confs:
        core.create_result_excel_file()
        least_confs = algorithm.get_weighted_conflict_count(core.initial_state)

    if least_confs <= constants.answer_threshold:
        break

print("final result generated")
