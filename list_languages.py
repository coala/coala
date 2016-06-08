from coalib.collecting.Collectors import collect_bears, \
    collect_all_bears_from_sections
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.Section import Section
from pyprint.ConsolePrinter import ConsolePrinter

if __name__ == '__main__':
    log_printer = LogPrinter(ConsolePrinter())
    local_bears, global_bears = collect_all_bears_from_sections(
        {'default': Section('default')}, log_printer)

    
    for bear in local_bears:
        print(bear.supported_languages)
