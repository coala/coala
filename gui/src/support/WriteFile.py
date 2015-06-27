from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.output.ConfWriter import ConfWriter
from gui.src.support.RunCoala import run_coala


def write_to_file_and_run(sections_view):
        sections_dict = {}
        confwriter = ConfWriter(".coafile")
        for section_name, section_listore in sections_view.items():
            section = Section(section_name)
            for row in section_listore:
                setting = Setting(key=row[0], value=row[1])
                section.append(setting)
            sections_dict[section_name] = section
        print(sections_dict)
        confwriter.write_sections(sections_dict)
        confwriter.close()
        return run_coala()
