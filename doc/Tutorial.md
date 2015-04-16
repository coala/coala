# coala Tutorial

Welcome to this little tutorial. It is meant to be a gentle introduction to the
usage of coala.

# Prerequisites

In order to complete this tutorial you will need coala installed. (Installation
is actually not required but it's more convenient and recommended.)

# Get Some Code

In order to perform a static code analysis on your code you will need some code
to check. If you do not have own code you want to check, you can retrieve our
tutorial samples:

```
git clone https://github.com/coala-analyzer/coala-tutorial.git
```

Please note that the commands given in this tutorial are intended for use with
this sample code and may need minor adjustments.

# Let's Start!

There are two options how to let coala know what kind of analysis it should
perform on which code.

## Command Line Interface

In order to specify the files to analyze, you can use the `--files` argument of
coala like demonstrated below. For all file paths, you can specify (recursive)
globs.

Because analysis routines can do many various things we named them _Bears_.
Thus you can specify the kind of analysis with the `--bears` argument.

Please type the following commands into the console:
```
cd coala-tutorial
coala --files=src/*.c --bears=SpaceConsistencyBear --save
```

coala will now ask you for missing values that are needed to perform the
analysis, which in this case is only the `use_spaces` setting. I recommend
setting it to `true`.

coala will now check the code and, in case you use the tutorial code, yield two
results. In the case of the SpaceConsistencyBear you will probably not be able
to see those trailing whitespace errors on your console (yet, we're working on
that).

Feel free to experiment a bit. You've successfully analysed some code! But
don't stop reading - you don't have to enter all those values again!

## Configuration Files

coala supports a very simple configuration file. If you've executed the
instructions from the CLI section above, coala will already have such a file
readily prepared for you. Go, take a look at it:

```
cat .coafile
```

This should yield something like this:

```
[Default]
bears = SpaceConsistencyBear
files = src/*.c
use_spaces = yeah
```

If you now invoke `coala` it will parse this `.coafile` from your current
directory. This makes it easy to specify once for your project what is checked
with which bears and make it available to all contributors.

Feel free to play around with this file. You can either edit it manually or
add/edit settings via `coala --save ...` invocations. If you want coala to save
settings every time, you can add `Save = True` manually into your `.coafile`.

# Sections

Thats all nice and well but we also have a Makefile for our project we want to
check. So let me introduce another feature of our configuration syntax:
_sections_.

The line `[Default]` specifies that everything below will belong to the Default
section. If nothing is specified, a setting will implicitly belong to this
section.

Let's check the line lengths of our Makefile:

```
coala -S Makefiles.bears=LineLengthBear Makefiles.files=Makefile --save
```

As you can see, the `-S` (or `--settings`) option allows to specify arbitrary
settings. Settings can be directly stored into a section with the
`section.setting` syntax.

It is recommended to enter `80` for the `max_line_length` setting.

coala will now yield any result you didn't correct last time plus a new one
for the Makefile. This time coala (or better, the LineLengthBear) doesn't know
how to fix the issue but still tries to provide as much helpful information as
possible and provides you the option to directly open the file in an editor
of your choice.

Note: If your editor is already open this will probably not work because the
other process will shortly communicate with the existent process and return
immediately. There is no way coala can know when you finished editing the file.

If you changed one file in multiple results, coala will merge the changes if
this is possible.

coala should have appended something like this to your `.coafile`:
```
[Makefiles]
bears = LineLengthBear
files = Makefile
max_line_length = 80
```

As you see, sections provide a way to have different configurations for
possibly different languages in one file. They are executed sequentially.

# Setting Inheritance

All settings in the default section are implicitly inherited to all other
sections (if they do not override their values). We can use that to save a few
lines!

Lets add the following section to our `.coafile`:

```
[TODOS]
bears = KeywordBear
```

And execute coala with the `-s` argument which is the same as `--save`. I
recommend setting case insensitive keywords to `TODO, FIXME` and case sensitive
keywords empty.

After the results we've already seen, we'll see a new informational one which
informs us that we have a TODO in our code.

Did you note that we didn't specify which files to check this time? This is
because all settings, including `files = src/*.c`, from the Default section
are already available in every other section implicitly. Thus the default
section is a good point to set things like logging and output settings or
specifying a default set of files to check.

# Enabling/Disabling Sections

Now that we have sections we need some way to control, which sections are
executed. coala provides two ways to do that:

## Manual Enabling/Disabling

If you add the line `TODOS.enabled=False` to some arbitrary place to
your `.coafile` or just `enabled=False` into the `TODOS` section, coala will
not show the TODOs on every run.

Especially for those bears yielding informational messages which you might want
to see from time to time this is a good way to silence them.

## Specifying Targets

If you provide positional arguments, like `coala Makefiles`, coala will execute
exclusively those sections that are specified. This will not get stored in your
`.coafile` and will take precedence over all enabled settings. You can specify
several targets seperated by a space.

What was that TODO again?

# Integrating coala into Your Project

It's easy to add coala to your project in a way that does not force your
developers even to install coala using git submodules. This also has the
advantage that all your developers are using exactly the same version of coala.
You can try it out in the coala-tutorial repository:

```
git submodule add https://github.com/coala-analyzer/coala.git
git commit -m 'Add coala submodule'
git add .coafile
git commit -m 'Add .coafile'
```

You can now use `coala/coala` as if it were the installed binary. Here's the
instructions for your developers:

```
git submodule init
git submodule update
coala/coala
```

# Continuing the Journey

If you want to know about more options, take a look at our help with
`coala -h`. If you liked or disliked this tutorial, feel free to drop us a note
at our bug tracker (github) or mailing list
(https://groups.google.com/forum/#!forum/coala-devel).

If you need more flexibility, know that coala is extensible in many ways due to
its modular design:

 * If you want to write your own bears, take a look at sources lying in `bears`
   and `coalib/bearlib`.
 * If you want to add custom actions for results, take a look at the code in
   `coalib/results/results_actions`.
 * If you want to have some custom outputs (e.g. HTML pages, a GUI or voice
   interaction) take a look at modules lying in `coalib/output`.

Happy coding!
