import os.path
from tempfile import TemporaryDirectory
import unittest

from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class LanguageDefinitionTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('any')
        self.section.append(Setting('language', 'CPP'))

    def test_key_contains(self):
        uut = LanguageDefinition.from_section(self.section)
        self.assertIn('extensions', uut)
        self.assertNotIn('randomstuff', uut)

    def test_external_coalang(self):
        with TemporaryDirectory() as directory:
            coalang_file = os.path.join(directory, 'random_language.coalang')
            with open(coalang_file, 'w') as file:
                file.write('extensions = .lol, .ROFL')
            uut = LanguageDefinition('random_language', coalang_dir=directory)
            self.assertIn('extensions', uut)
            self.assertEqual(list(uut['extensions']), ['.lol', '.ROFL'])
