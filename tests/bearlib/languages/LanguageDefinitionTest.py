import unittest

from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.misc.ContextManagers import make_temp


class LanguageDefinitionTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("any")
        self.section.append(Setting("language", "CPP"))

    def test_nonexistant_file(self):
        self.section.append(Setting("language", "bullshit"))

        with self.assertRaises(FileNotFoundError):
            LanguageDefinition.from_section(self.section)

    def test_loading(self):
        uut = LanguageDefinition.from_section(self.section)
        self.assertEqual(list(uut["extensions"]), [".c", ".cpp", ".h", ".hpp"])

    def test_key_contains(self):
        uut = LanguageDefinition.from_section(self.section)
        self.assertIn("extensions", uut)
        self.assertNotIn("randomstuff", uut)

    def test_external_coalang(self):
        with make_temp() as coalang:
            with open(coalang, "w") as file:
                file.write('extensions = .lol, .ROFL')
            uut = LanguageDefinition("random_language", coalang_path=coalang)
            self.assertIn("extensions", uut)
            self.assertEqual(list(uut["extensions"]), [".lol", ".ROFL"])
