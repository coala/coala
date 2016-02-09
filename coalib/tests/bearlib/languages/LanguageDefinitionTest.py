import unittest

from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class LanguageDefinitionTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("any")
        self.section.append(Setting("language_family", "C"))
        self.section.append(Setting("language", "CPP"))

    def test_nonexistant_file(self):
        self.section.append(Setting("language", "bullshit"))

        with self.assertRaises(KeyError):
            LanguageDefinition.from_section(self.section)

        self.section.append(Setting("language_family", "bullshit"))
        with self.assertRaises(FileNotFoundError):
            LanguageDefinition.from_section(self.section)

    def test_loading(self):
        uut = LanguageDefinition.from_section(self.section)
        self.assertEqual(list(uut["extensions"]), [".c", ".cpp", ".h", ".hpp"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
