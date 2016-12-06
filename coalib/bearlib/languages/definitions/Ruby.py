from coalib.bearlib.languages.Language import Language


@Language
class Ruby:
    extensions = ('.rb', '.rbw', '.rbx',
                  'Gemfile', '.gemspec',
                  'Rakefile', '.rake',
                  )
