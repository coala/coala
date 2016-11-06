from coalib.bearlib.aspects import Root, Taste


@Root.subaspect
class Metadata:
    """
    This describes any aspect that is related to metadata that is not
    inside your source code.
    """


@Metadata.subaspect
class CommitMessage:
    """
    Your commit message is important documentation associated with your
    source code. It can help you to identify bugs (e.g. through
    `git bisect`) or find missing information about unknown source code
    (through `git blame`).

    Commit messages are also sometimes used to generate - or write
    manually - release notes.
    """


@CommitMessage.subaspect
class Emptiness:
    """
    Your commit message serves as important documentation for your source
    code.
    """
    class docs:
        example = '(no text at all)'
        example_language = 'English'
        importance_reason = """
        An empty commit message shows the lack of documentation for your
        change.
        """
        fix_suggestions = 'Write a commit message.'


@CommitMessage.subaspect
class Shortlog:
    """
    Your commit shortlog is the first line of your commit message. It is
    the most crucial part and summarizes the change in the shortest possible
    manner.
    """


@Shortlog.subaspect
class ColonExistence:
    """
    Some projects force to use colons in the commit message shortlog
    (first line).
    """
    class docs:
        example = """
        FIX: Describe change further
        context: Describe change further
        """
        example_language = 'English'
        importance_reason = """
        The colon can be a useful separator for a context (e.g. a filename) so
        the commit message makes more sense to the reader or a classification
        (e.g. FIX, ...) or others. Some projects prefer not using colons
        specifically: consistency is key.
        """
        fix_suggestions = """
        Add or remove the colon according to the commit message guidelines.
        """

    shortlog_colon = Taste[bool](
        'Whether or not the shortlog has to contain a colon.',
        (True, False), default=True)


@Shortlog.subaspect
class TrailingPeriod:
    """
    Some projects force not to use trailing periods in the commit
    message shortlog (first line).
    """
    class docs:
        example = """
        Describe change.
        Describe change
        """
        example_language = 'English'
        importance_reason = """
        Consistency is key to make messages more readable. Removing a trailing
        period can also make the message shorter by a character.
        """
        fix_suggestions = """
        Add or remove the trailing period according to the commit message
        guidelines.
        """

    shortlog_period = Taste[bool](
        'Whether or not the shortlog has to contain a trailing period.',
        (True, False), default=False)


@Shortlog.subaspect
class Tense:
    """
    Most projects have a convention on which tense to use in the commit
    shortlog (the first line of the commit message).
    """
    class docs:
        example = """
        Add file
        Adding file
        Added file
        """
        example_language = 'English'
        importance_reason = """
        Consistency is key to make messages more readable.
        """
        fix_suggestions = """
        Rephrase the shortlog into the right tense.
        """

    shortlog_tense = Taste[str](
        'The tense of the shortlog.',
        ('imperative', 'present continuous', 'past'),
        default='imperative')


@Shortlog.subaspect
class Length:
    """
    The length of your commit message shortlog (first line).
    """
    class docs:
        example = """
        Some people just write very long commit messages. Too long. "
        Even full sentences. And more of them, too!
        """
        example_language = 'English'
        importance_reason = """
        A good commit message should be quick to read and concise. Also, git
        and platforms like GitHub do cut away everything beyond 72, sometimes
        even 50 characters making any longer message unreadable.
        """
        fix_suggestions = """
        Try to compress your message:

        - Using imperative tense usually saves a character or two
        - Omitting a trailing period saves another character
        - Leave out unneeded words or details
        - Use common abbreviations like w/, w/o or &.
        """

    max_shortlog_length = Taste[int](
        'The maximal number of characters the shortlog may contain.',
        (50, 72, 80), default=72)


@Shortlog.subaspect
class FirstCharacter:
    """
    The first character of your commit message shortlog (first line) usually
    should be upper or lower case consistently.

    If the commit message contains a colon, only the first character after
    the colon will be checked.
    """
    class docs:
        example = """
        Add coverage pragma
        Compatability: Add coverage pragma
        add coverage pragma
        Compatability: add coverage pragma
        """
        example_language = 'English'
        importance_reason = """
        Consistent commit messages are easier to read through.
        """
        fix_suggestions = """
        Convert your first character to upper/lower case. If your message starts
        with an identifier, consider rephrasing. Usually starting with a verb is
        a good idea.
        """

    shortlog_starts_upper_case = Taste[bool](
        'Whether or not the shortlog (first line) of a commit message should '
        'start with an upper case letter consistently.',
        (True, False), default=True)


@CommitMessage.subaspect
class Body:
    """
    Your commit body may contain an elaborate description of your commit.
    """


@Body.subaspect
class Existence:
    """
    Forces the commit message body to exist (nonempty).
    """
    class docs:
        example = """
        aspects: Add CommitMessage.Body
        """
        example_language = 'English'
        importance_reason = """
        Having a nonempty commit body is important if you consistently want
        elaborate documentation on all commits.
        """
        fix_suggestions = """
        Write a commit message with a body.
        """


@Body.subaspect
class Length:
    """
    The length of your commit message body lines.
    """
    class docs:
        example = """
        Some people just write very long commit messages. Too long.
        Way too much actually. If they would just break their lines!
        """
        example_language = 'English'
        importance_reason = """
        Git and platforms like GitHub usually break everything beyond 72
        characters, making a message containing longer lines hard to read.
        """
        fix_suggestions = """
        Simply break your lines right before you hit the border.
        """

    max_body_length = Taste[int](
        'The maximal number of characters the body may contain in one line. '
        'The newline character at each line end does not count to that length.',
        (50, 72, 80), default=72)
