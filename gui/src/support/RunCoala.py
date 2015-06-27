from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.processes.Processing import execute_section
from coalib.output.NullInteractor import NullInteractor


def run_coala():
    bear_results = {}
    yielded_results = None
    (sections,
     local_bears,
     global_bears,
     targets,
     interactor,
     log_printer) = gather_configuration()

    interactor = NullInteractor(log_printer)

    for section_name in sections:
        section = sections[section_name]
        if not section.is_enabled(targets):
            continue

        interactor.begin_section(section)
        results = execute_section(section=section,
                                  global_bear_list=global_bears[section_name],
                                  local_bear_list=local_bears[section_name],
                                  print_results=interactor.print_results,
                                  finalize=interactor.finalize,
                                  log_printer=log_printer)
        yielded_results = yielded_results or results[0]
        for file, result_list in results[1].items():
            if file in bear_results:
                bear_results[file].extend(result_list)
            else:
                bear_results[file] = result_list

        for bear, result_list in results[2].items():
            for result in result_list:
                if result.file in bear_results:
                    bear_results[result.file].append(result)
                else:
                    bear_results[result.file] = [result]
    return bear_results

