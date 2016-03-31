A Hitchhiker's Guide to Git(1): Genesis
#######################################

Introduction
============

What is This?
-------------

This post tries to provide a **gentle introduction** to git. While it is
aimed at **newcomers** it is also meant to give a rather **good overview
and understanding** of what one can do with git and thus **is
extensive**. It follows the premise:

    If you know how a thing works, you can make it do what you want it
    to.

Please don't be afraid as I'm trying to use **light language** and
**many examples** so you can **read fast** through it and understand
anyway (if I succeed). I'm also trying to **highlight important things**
at least for long texts to ease reading a bit more. However, at some
points this tutorial *may* require you to **think for yourselves** a bit
- it's a feature, not a bug.

For Whom is This?
-----------------

This tutorial is meant for everyone willing to learn git - it does not
matter if you are a **developer** who never really got the hang of it or
a **student** wanting to learn. Even if you are doing non coding tasks
like **design** or **documentation** git can be a gift from heaven. This
tutorial is **for everyone** - don't be scared by its length and believe
me, **it pays off**! The only **requirement** is that you have **git
installed**, know ``cd``, ``ls`` and ``mkdir`` and **have something to
commit** - and who doesn't have any digital data!?

What's in There?
----------------

This tutorial is the **first out of three** tutorials which are meant to
**free your mind** from a **traditional view on filesystems**.

Genesis
~~~~~~~

This tutorial, **Genesis (i.e. "Creation" or "Beginning")**, will cover
some very basic things:

-  **Configuring** git so you can use it how you want. (Basic, aliases)
-  **Creating** your git **repository** (play god once!)
-  **Creating** your first git **commits**.
-  **Learning** what the **repository** is and **where commits get
   stored**.
-  **Browsing** through **history**.
-  **Ignoring files**.

Exodus
~~~~~~

**Exodus (i.e. "going out")** will cover:

-  **Store** temporary changes **without committing**.
-  **Navigating** commits in git.
-  **Sharing** commits to a **remote place**.
-  **Locally** (huh, that's sharing?)
-  Via **email**
-  To a **server**
-  To a **client**
-  Working **with others** (i.e. **non-linear**).
-  **Join** things.
-  **Linearize** things.
-  **Writing good** commits.
-  **Editing** commits. (Actually not editing but it feels like that.)

Apocalypse
~~~~~~~~~~

**Apocalypse (i.e. "uncovering")** will try to uncover some more
advanced features of git, finally freeing your mind from your
non-versioned filesystem:

-  **Finding more information** about code.
-  **Finding causes of bugs** in git.
-  **Reverting** commits.
-  **Reviewing** commits.
-  **Travelling though time** and **changing history** (you want me to
   believe you've never wanted to do that?)
-  **Getting back** lost things.
-  Let git **do things automatically**.

Some Warnings
-------------

A short warning: If you ever really got the hang of git you will not be
able to **use something else** without symptoms of **frustration and
disappointment** - you'll end up writing every document versioned as an
excuse to use git.

A warning for windows users: you may need to use equivalent commands to
some basic UNIX utilities or just install them with git. (Installer
provides an option for that.) In general it's a bit like travelling with
Vogons - avoid when possible.

A warning for GUI users: **Don't use your GUI**. Be it the GitHub App or
SourceTree or something else - they usually try to make things more
abstract for us, thus they hinder us from understanding git and we can
then not make git do what we want. Being able to communicate
**directly** with git is a great thing and really bumps
**productivity**!

I wrote this tutorial to the best of my knowledge and experience, if you
spot an error or find something important is missing, be sure to drop me
a message!

Preparation...
--------------

So go now, grab a cup of coffee (or any other drink), a towel, take your
best keyboard and open a terminal beneath this window!

What's Git for Anyway?
======================

Before we really get started it is important to know what git roughly
does: git is a program that allows you to **manage files**. To be more
specific git allows you to **define changes on files**. In the end your
repository is just a **bunch of changes** that may be related to each
other.

Setting Up Git
==============

Before we can continue we'll have to set up a few tiny things for git.
For this we will use the ``git config --global`` command which simply
**stores** a **key value pair** into your **user-global git
configuration file** (usually stored at ``~/.gitconfig``).

WHOAMI
------

Let's tell git who we are! This is pretty straightforward:

::

    $ git config --global user.name "Ford Prefect"
    $ git config --global user.email ford@prefect.bg

This makes git store values for "name" and "email" within the "user"
section of the gitconfig.

Editor
------

For some operations git will give you an **editor** so you can enter
needed data. This editor is **vim by default**. Some people think vim is
great (vim *is* great!), some do not. If you belong to the latter group
or don't know what vim is and how to operate it, let's **change the
editor**:

::

    $ # Take an editor of your choice instead of nano
    $ git config --global core.editor nano

Please make sure that the **command** you give to git always **starts as
an own process** and ends only when you finished editing the file. (Some
editors might detect running processes, pass the filename to them and
exit immediately. Use ``-s`` argument for gedit, ``--wait`` argument for
sublime.) Please **don't use notepad** on windows, this program is a
perfect example of a text editor which is too dumb to show text unless
the text is written by itself.

Create a Repository
===================

So, lets get started - with nothing. Let's make an empty directory. You
can do that from your usual terminal:

::

    $ mkdir git-tutorial
    $ cd git-tutorial
    $ ls -a
    ./  ../

So, lets do the first git command here:

::

    $ git init
    Initialized empty Git repository in /home/lasse/prog/git-tutorial/.git/
    $ ls -a
    ./  ../  .git/

So now we've got the ``.git`` folder. Since we just created a repository
with ``git init``, so we can deduce, that this **.git directory must in
fact be the repository**!

Creating a God Commit
=====================

So, let's create some content we can manage with git:

::

    $ echo 'Hello World!' >> README
    $ cat README
    Hello World!

Since we know, that the .git directory is our repository, we also know
that **we did not add this file to our repository** yet. So how do we do
that?

As I've hinted before, our git repository **does not contain files** but
only **changes** - so how do we make a change out of our file?

The answer lies in (1) ``git add`` and (2) ``git commit`` which allows us
to (1) specify what files/file changes we want to add to the change and
(2) that we want to pack those file changes into a so-called **commit**.
Git also offers a helper command so we can see what will be added to our
commit: ``git status``.

Let's try it out:

::

    $ git status
    On branch master

    Initial commit

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

        README

    nothing added to commit but untracked files present (use "git add" to track)
    $ git add README
    $ git status
    On branch master

    Initial commit

    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)

        new file:   README

So obviously with ``git add`` we can **stage** files. What does that
mean?

As we know, when we're working in our directory **any actions on files
won't affect our repository**. So in order to **add a file** to the
repository, we'll have to **put it into a commit**. In order to do that,
we need to **specify, what files/changes should go into our commit**,
i.e. stage them. When we did ``git add README``, we **staged** the file
README, thus every change we did until now to it will be **included in
our next commit**. (You can also partially stage files so if you edit
README now the change won't be committed.)

Now we'll do something very special in git - **creating the first
commit**! (We'll pass the ``-v`` argument to get a bit more info from
git on what we're doing.)

::

    $ git commit -v

You should now get your editor with contents similar to this:

::


    # Please enter the commit message for your changes. Lines starting
    # with '#' will be ignored, and an empty message aborts the commit.
    # On branch master
    #
    # Initial commit
    #
    # Changes to be committed:
    #   new file:   README
    #ref: refs/heads/master

    # ------------------------ >8 ------------------------
    # Do not touch the line above.
    # Everything below will be removed.
    diff --git a/README b/README
    new file mode 100644
    index 0000000..c57eff5
    --- /dev/null
    +++ b/README
    @@ -0,0 +1 @@
    +Hello World!

Since we're about to create a change, git asks us for a **description**.

.. note::
    Git actually allows creating commits without a description with
    a special argument. This is not recommended for productive
    collaborative work!)

Since we passed the ``-v`` parameter, git also shows us below what will
be included in our change. We'll look at this later.

**Commit messages** are usually written in **imperative present tense**
and should follow certain guidelines. We'll come to this later.

So, let's enter: ``Add README`` as our commit message, save and exit the
editor.

Now, let's take a look at what we've created, ``git show`` is the
command that shows us the **most recent commit**:

::

    $ git show
    commit ec6c903a0a18960cd73df18897e56738c4c6bb51
    Author: Lasse Schuirmann <lasse.schuirmann@gmail.com>
    Date:   Fri Feb 27 14:12:01 2015 +0100

        Add README

    diff --git a/README b/README
    new file mode 100644
    index 0000000..980a0d5
    --- /dev/null
    +++ b/README
    @@ -0,0 +1 @@
    +Hello World!

So what do we see here:

-  It seems that commits have an **ID**, in this case
   ``ec6c903a0a18960cd73df18897e56738c4c6bb51``.
-  Commits also have an **author** and a **creation date**.
-  Of course they hold the **message** we wrote and **changes** to some
   files.

What we see below the ``diff ...`` line is obviously the change. Let's
take a look at it: since **git can only describe changes**, it takes
``/dev/null`` (which is a bit special, kind of an empty file, not
important here), **renames** it to ``README`` and **fills** it with our
contents.

So, this commit is pretty godish: It exists purely on it's own, has no
relations to any other commit (yet, it's based on an empty repository,
right?) and **creates a file out of nothing** (/dev/null is somehow all
*and* nothing, kind of a unix black hole).

Inspecting What Happened
========================

So, let's look in our repository!

::

    $ ls -la .git
    total 52
    drwxrwxr-x. 8 lasse lasse 4096 Feb 27 16:05 ./
    drwxrwxr-x. 3 lasse lasse 4096 Feb 27 14:11 ../
    drwxrwxr-x. 2 lasse lasse 4096 Feb 27 14:11 branches/
    -rw-rw-r--. 1 lasse lasse  486 Feb 27 14:12 COMMIT_EDITMSG
    -rwxrw-r--. 1 lasse lasse   92 Feb 27 14:11 config*
    -rw-rw-r--. 1 lasse lasse   73 Feb 27 14:11 description
    -rw-rw-r--. 1 lasse lasse   23 Feb 27 14:11 HEAD
    drwxrwxr-x. 2 lasse lasse 4096 Feb 27 14:11 hooks/
    -rw-rw-r--. 1 lasse lasse  104 Feb 27 14:11 index
    drwxrwxr-x. 2 lasse lasse 4096 Feb 27 14:11 info/
    drwxrwxr-x. 3 lasse lasse 4096 Feb 27 14:12 logs/
    drwxrwxr-x. 7 lasse lasse 4096 Feb 27 14:12 objects/
    drwxrwxr-x. 4 lasse lasse 4096 Feb 27 14:11 refs/
    $

Now let's look into it further to get to know what it is a bit more. I
will try to cover only important parts here, if you're interested even
deeper, you can try DuckDuckGo or take a look at this:
http://git-scm.com/docs/gitrepository-layout

The config file
---------------

The **config file** is a similar file to the one where our **settings**
in the beginning got stored. (User and editor configuration, remember?)
You can use it to store settings **per repository**.

The objects directory
---------------------

The objects directory is an important one: It contains our commits.

One could do a full tutorial on those things but that's not covered
here. If you want that, check out:
http://git-scm.com/book/en/v2/Git-Internals-Git-Objects

We just saw the **ID** of the commit we made:
``ec6c903a0a18960cd73df18897e56738c4c6bb51``

Now let's see if we find it in the objects directory:

::

    $ ls .git/objects
    98/  b4/  ec/  info/  pack/
    $ ls .git/objects/ec
    6c903a0a18960cd73df18897e56738c4c6bb51

So, when we create a commit, the contents (including metadata) are
**hashed** and git stores it finely into the objects directory.

That isn't so complicated at all, is it?

Task: Objects
~~~~~~~~~~~~~

``git show`` accepts a commit ID as an argument. So you could e.g. do
``git show ec6c903a0a18960cd73df18897e56738c4c6bb51`` instead of
``git show`` if this hash is the current commit.

Investigate what the other two objects are, which are stored in the
objects directory. (Ignore the info and pack subdirectory.)

Do ``git show`` again and take a look at the line beginning with
"index". I'm sure you can make sense out of it!

The HEAD File
-------------

The HEAD file is here so git knows what the current commit is, i.e. with
which objects it has to compare the files in the file system to e.g.
generate a diff. Let's look into it:

::

    $ cat .git/HEAD
    ref: refs/heads/master

So it actually only references to something else.

So let's take a look into refs/heads/master - what ever this is:

::

    $ cat .git/refs/heads/master
    ec6c903a0a18960cd73df18897e56738c4c6bb51

So this ``HEAD`` file refers to this ``master`` file which refers to our
current commit. We'll see how that makes sense later.

Creating a Child Commit
=======================

Now, let's go on and create another commit. Let's add something to our
README. You can do that by yourself, I'm sure!

Let's see what we've done:

::

    $ git diff
    diff --git a/README b/README
    index 980a0d5..c9b319e 100644
    --- a/README
    +++ b/README
    @@ -1 +1,2 @@
     Hello World!
    +Don't panic!

Let's commit it. However, since we're a bit lazy we **don't** want to
**add** the README **manually** again; the commit command has an
argument that allows you to **auto-stage all changes** to all files that
are in our **repository**. (So if you added **another file** which is
**not in the repository** yet it **won't be staged**!)

::

    $ git commit -a -v

Well, you know the game. Can you come up with a **good message** on your
own?

::

    $ git show
    commit 7b4977cdfb3f304feffa6fc22de1007dd2bebf26
    Author: Lasse Schuirmann <lasse.schuirmann@gmail.com>
    Date:   Fri Feb 27 16:39:11 2015 +0100

        README: Add usage instructions

    diff --git a/README b/README
    index 980a0d5..c9b319e 100644
    --- a/README
    +++ b/README
    @@ -1 +1,2 @@
     Hello World!
    +Don't panic!

So this **commit** obviously represents the **change** from a file named
README which **contents** are **stored in object** ``980a0d5`` to a file
also named README which **contents** are **stored in object**
``c9b319e``.

A Glance At Our History
=======================

Let's see a timeline of what we've done:

::

    $ git log
    commit 7b4977cdfb3f304feffa6fc22de1007dd2bebf26
    Author: Lasse Schuirmann <lasse.schuirmann@gmail.com>
    Date:   Fri Feb 27 16:39:11 2015 +0100

        README: Add usage instructions

    commit ec6c903a0a18960cd73df18897e56738c4c6bb51
    Author: Lasse Schuirmann <lasse.schuirmann@gmail.com>
    Date:   Fri Feb 27 14:12:01 2015 +0100

        Add README

That looks fairly easy. However I cannot withstand to point out that
despite commits look so fine, linearly **arranged** here, they are
actually **nothing more than commit objects, floating around** in the
**.git/objects/ directory**. So ``git log`` just **looks where HEAD
points to** and recursively asks each commit **what it's parent is** (if
it has one).

Since every good hitchhiker does know how to travel through time and
change events, we'll learn to do that in the next chapter ;)

Configuring Git Even Better
===========================

Better staging
--------------

It is worth to mention that ``git add`` also **accepts directories** as
an argument. I.e. ``git add .`` **recursively adds all files** from the
**current directory**.

In order to generally **ignore certain patterns** of files (e.g. it's
**bad practice** to **commit any generated stuff**), one can write a
``.gitignore`` file. This file can look as follows:

::

    README~  # Ignore gedit temporary files
    *.o  # Ignore compiled object files

The **exact pattern** is defined here: http://git-scm.com/docs/gitignore

Files matching this pattern will:

-  Not be added with ``git add`` unless forced with ``-f``
-  Not be shown in ``git status`` as unstaged

It is usually a good idea to **commit** the ``.gitignore`` **to the
repository** so all developers don't need to care about those files.

Aliases
-------

So, we've learned quite some stuff. However git command's aren't as
**intuitive** as they could be sometimes. They could be **shorter** too.
So let's define us some **aliases** of the commands we know. The ones
given here are **only suggestions**, you should **choose the aliases in
a way that suits best for you**!

Aliasing Git Itself
~~~~~~~~~~~~~~~~~~~

If you're using git much, you might want to add ``alias g=git`` to your
``.bashrc`` or ``.zshrc`` or whatever. (On windows you're a bit screwed.
But what did you expect? Really?)

Aliasing Git Commands
~~~~~~~~~~~~~~~~~~~~~

Let's let git give us our editor since we don't want to edit just one
value:

::

    $ git config --global --edit

You can add aliases through the ``[alias]`` section, here are the
aliases I suggest:

::

    [alias]
    a = add
    c = commit -v
    ca = commit -v -a
    d = diff
    dif = diff # Thats a typo :)
    i = init
    l = log
    st = status
    stat = status

Conclusion
==========

So what did we learn?

We did some basic git commands:

-  ``git config``: accessing git configuration
-  ``git init``: creating a repository
-  ``git status``: getting the current status of files, staging and so on
-  ``git add``: staging files for the commit
-  ``git diff``: showing the difference between the current commit and
   what we have on our file system
-  ``git commit``: writing staged changes to a commit
-  ``git log``: browsing history

We also learned how git organizes commits, how it stores files and how
we can make git ignore files explicitly.

I hope this helped you **understanding** a bit **what git does** and
**what it is**. The next tutorial will hopefully cover all the basics.
(Some were already hinted here.)
