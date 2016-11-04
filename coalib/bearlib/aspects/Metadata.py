from coalib.bearlib.aspects import Root, AspectDocumentation, AspectSetting


Root.new_subaspect(
    "Metadata",
    AspectDocumentation(
        definition="""
        This describes any aspect that is related to metadata that is not
        inside your source code.
        """
    )
)

Root.Metadata.new_subaspect(
    "CommitMessage",
    AspectDocumentation(
        definition="""
        Your commit message is important documentation associated with your
        source code. It can help you to identify bugs (e.g. through
        `git bisect`) or find missing information about unknown source code
        (through `git blame`).

        Commit messages are also sometimes used to generate - or write
        manually - release notes.
        """
    )
)

Root.Metadata.CommitMessage.new_subaspect(
    "Emptiness",
    AspectDocumentation(
        definition="""
        Your commit message serves as important documentation for your source
        code.
        """,
        example="(no text at all)",
        example_language="English",
        importance_reason="""
        An empty commit message shows the lack of documentation for your
        change.
        """,
        fix_suggestions="Write a commit message."
    )
)

Root.Metadata.CommitMessage.new_subaspect(
    "Shortlog",
    AspectDocumentation(
        definition="""
        Your commit shortlog is the first line of your commit message. It is
        the most crucial part and summarizes the change in the shortest possible
        manner.
        """
    )
)

Root.Metadata.CommitMessage.Shortlog.new_subaspect(
    "ColonExistence",
    AspectDocumentation(
        definition="""
        Some projects force to use colons in the commit message shortlog
        (first line).
        """,
        example="""
        FIX: Describe change further
        context: Describe change further
        """,
        example_language="English",
        importance_reason="""
        The colon can be a useful separator for a context (e.g. a filename) so
        the commit message makes more sense to the reader or a classification
        (e.g. FIX, ...) or others. Some projects prefer not using colons
        specifically: consistency is key.
        """,
        fix_suggestions="""
        Add or remove the colon according to the commit message guidelines.
        """
    ),
    settings=(AspectSetting(
        "shortlog_colon",
        "Whether or not the shortlog has to contain a colon.",
        bool,
        (True, False),
        True
    ),)
)

Root.Metadata.CommitMessage.Shortlog.new_subaspect(
    "TrailingPeriod",
    AspectDocumentation(
        definition="""
        Some projects force not to use trailing periods in the commit
        message shortlog (first line).
        """,
        example="""
        Describe change.
        Describe change
        """,
        example_language="English",
        importance_reason="""
        Consistency is key to make messages more readable. Removing a trailing
        period can also make the message shorter by a character.
        """,
        fix_suggestions="""
        Add or remove the trailing period according to the commit message
        guidelines.
        """
    ),
    settings=(AspectSetting(
        "shortlog_period",
        "Whether or not the shortlog has to contain a trailing period.",
        bool,
        (True, False),
        False
    ),)
)

Root.Metadata.CommitMessage.Shortlog.new_subaspect(
    "Tense",
    AspectDocumentation(
        definition="""
        Most projects have a convention on which tense to use in the commit
        shortlog (the first line of the commit message).
        """,
        example="""
        Add file
        Adding file
        Added file
        """,
        example_language="English",
        importance_reason="""
        Consistency is key to make messages more readable.
        """,
        fix_suggestions="""
        Rephrase the shortlog into the right tense.
        """
    ),
    settings=(AspectSetting(
        "shortlog_tense",
        "The tense of the shortlog.",
        str,
        ("imperative", "present continuous", "past"),
        "imperative"
    ),)
)

Root.Metadata.CommitMessage.Shortlog.new_subaspect(
    "Length",
    AspectDocumentation(
        definition="""
        The length of your commit message shortlog (first line).
        """,
        example="Some people just write very long commit messages. Too long. "
                "Even full sentences. And more of them, too!",
        example_language="English",
        importance_reason="""
        A good commit message should be quick to read and concise. Also, git
        and platforms like GitHub do cut away everything beyond 72, sometimes
        even 50 characters making any longer message unreadable.
        """,
        fix_suggestions="""
        Try to compress your message:

        - Using imperative tense usually saves a character or two
        - Omitting a trailing period saves another character
        - Leave out unneeded words or details
        - Use common abbreviations like w/, w/o or &.
        """
    ),
    settings=(AspectSetting(
        "max_shortlog_length",
        "The maximal number of characters the shortlog may contain.",
        int,
        (50, 72, 80),
        72
    ))
)

Root.Metadata.CommitMessage.Shortlog.new_subaspect(
    "FirstCharacter",
    AspectDocumentation(
        definition="""
        The first character of your commit message shortlog (first line) usually
        should be upper or lower case consistently.

        If the commit message contains a colon, only the first character after
        the colon will be checked.
        """,
        example="""
        Add coverage pragma
        Compatability: Add coverage pragma
        add coverage pragma
        Compatability: add coverage pragma
        """,
        example_language="English",
        importance_reason="Consistent commit messages are easier to read "
                          "through.",
        fix_suggestions="""
        Convert your first character to upper/lower case. If your message starts
        with an identifier, consider rephrasing. Usually starting with a verb is
        a good idea.
        """
    ),
    settings=(AspectSetting(
        "shortlog_starts_upper_case",
        "Whether or not the shortlog (first line) of a commit message should "
        "start with an upper case letter consistently.",
        bool,
        (True, False),
        True
    ))
)

Root.Metadata.CommitMessage.new_subaspect(
    "Body",
    AspectDocumentation(
        definition="""
        Your commit body may contain an elaborate description of your commit.
        """
    )
)

Root.Metadata.CommitMessage.Body.new_subaspect(
    "Existence",
    AspectDocumentation(
        definition="""
        Forces the commit message body to exist (nonempty).
        """,
        example="""
        aspects: Add CommitMessage.Body
        """,
        example_language="English",
        importance_reason="""
        Having a nonempty commit body is important if you consistently want
        elaborate documentation on all commits.
        """,
        fix_suggestions="""
        Write a commit message with a body.
        """
    )
)
