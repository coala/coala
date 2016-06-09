from itertools import chain

from coalib.collecting.Collectors import collect_bears, \
    collect_all_bears_from_sections
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.Section import Section
from pyprint.ConsolePrinter import ConsolePrinter

if __name__ == '__main__':
    log_printer = LogPrinter(ConsolePrinter())
    local_bears, global_bears = collect_all_bears_from_sections(
        {'default': Section('default')}, log_printer)

    languages = set()
    for bear in chain(*list(local_bears.values()),
                      *list(global_bears.values())):
        languages |= set(bear.supported_languages)

    print(', '.join(sorted(languages ^ {'All'})))
