External Bears
==============

Welcome. This tutorial will teach you how to use the
``@external_bear_wrap`` decorator in order to write Bears in languages other
than Python.

.. note::

  This tutorial assumes that you already know the basics. If you are new,
  please refer to the
  :doc:`Writing Native Bears<Writing_Native_Bears>` section.

  If you are planning to create a bear that uses an already existing tool (aka
  linter), please refer to the
  :doc:`Linter Bears<Writing_Linter_Bears>` section.

Why is This Useful?
-------------------

coala is a great language independent static analysis tool, where users can
write their own static analysis routines.

Enabling users to write external ``bears`` means that they can write their own
static analysis routine in their favourite language.

How Does This Work?
-------------------

By using the ``@external_bear_wrap`` decorator you will have all the necessary
data sent to your external executable (filename, lines, settings) as a JSON
string via ``stdin``. Afterwards, the analysis takes place in your executable
that can be written in **literally** any language. In the end, you will have to
provide the ``Results`` in a JSON string via stdout.

In this tutorial, we will go through 2 examples where we create a very simple
bear. The first example will use a **compiled** language, ``C++``, that creates
a standalone binary whilst in the second example we will take a look at
``JS`` that needs ``node`` in order to run out of the browser.

External Bear Generation Tool
-----------------------------

If you really do not want to write any Python code, there is a tool
`here <https://gitlab.com/coala/coala-bear-management>`__,
``coala-bears-create``, that will create the wrapper for you. We will be using

::

    $ coala-bears-create -ext

in order to generate the wrapper for the bear.

Writing a Bear in C++
---------------------

The bear that will be created with this tutorial will check whether there is
any **coala** spelled with a capital ``C`` since that is a horrible mistake for
one to make.

1. Create a new directory and make it your current working directory.
2. Run ``coala-bears-create`` as mentioned above in order to create the wrapper
   for our ``C++`` bear. Answer the first question with a path to your created
   directory (since it should be the current one you can choose the default
   value and just hit ``Enter``).
3. The most important questions are the ones regarding the executable name and
   the bear name. Use ``coalaCheckBear`` for the bear name and
   ``coalaCheck_cpp`` for the executable name.
4. The rest of the questions are not important (languages, developer name and
   contact info, license, etc) to the tutorial and you can go with the
   defaults.
   When you are prompted about ``settings`` answer ``no`` (default). After the
   script is finished running there should be 2 files in your current
   directory:
   ``coalaCheckBear.py`` (the wrapper) and ``coalaCheckBearTest.py``.
5. This tutorial will not focus on testing so ignore the second file for now.
   The wrapper should look similar to the code block presented below. Some code
   has been cleaned for convenience of explanation.

.. note::

    The ``LICENSE`` specified applies only to the python code. You can license
    your executable however you see fit.

::

    import os

    from coalib.bearlib.abstractions.ExternalBearWrap import external_bear_wrap


    @external_bear_wrap(executable='coalaCheck_cpp',
                        settings={})
    class coalaCheckBear:
        """
        Checks for coala written with uppercase 'C'
        """
        LANGUAGES = {'All'}
        REQUIREMENTS = {''}
        AUTHORS = {'Me'}
        AUTHORS_EMAILS = {'me@mail.com'}
        LICENSE = 'AGPL'

        @staticmethod
        def create_arguments():
            return ()

6. Since the input will be a JSON string some kind of JSON class is needed.
   nlohmann's JSON library (
   `https://github.com/nlohmann/json <https://github.com/nlohmann/json>`__) is a
   great choice because it is easy to integrate and is used in this tutorial.
7. Create ``coalaCheck.cpp`` and start by testing the input. The best thing
   about nlohmann's JSON library is that you can parse JSON directly
   from stdin like this:

::

    #include <iostream>

    #include "json.hpp"

    using json = nlohmann::json;
    using namespace std;

    json in;

    int main() {

        cin >> in;

        cout << in;

        return 0;
    }

8. Create a ``Makefile``. The JSON library requires C++11 so a sample
   ``Makefile`` would look like this:

::

    build: coalaCheck.cpp
        g++ -std=c++11 -o coalaCheck_cpp coalaCheck.cpp

9. Compile and test the binary by giving it a JSON string. It should print the
   JSON string back at ``stdout``.

10. Read about the JSON Spec that the input uses (`The JSON Spec`_).
    The filename is found in ``in["filename"]`` and the list of lines is found
    in ``in["file"]``.
11. Create a result adding function, also an init function proves quite useful
    for initializing the output json.

::

    #include <iostream>
    #include <string>

    #include "json.hpp"

    using json = nlohmann::json;
    using namespace std;

    json in;
    json out;
    string origin;

    void init_results(string bear_name) {
        origin = bear_name;
        out["results"] = json::array({});
    }

    void add_result(string message, int line, int column, int severity) {
        json result = {
            {"origin", origin},
            {"message", message},
                {"affected_code", json::array({{
                    {"file", in["filename"]},
                    {"start", {
                        {"column", column},
                        {"file", in["filename"]},
                        {"line", line}
                    }},
                    {"end", {
                        {"column", column+6},
                        {"file", in["filename"]},
                        {"line", line}
                    }}
                }})},
            {"severity", severity}
        };
        out["results"] += result;
    }

    int main() {

        cin >> in;

        init_results("coalaCheckBear");

        cout << out;
        return 0;
    }

.. note::

    The ``C++`` operators and syntax are not well suited for JSON manipulation
    but nlohmann's JSON lib makes it as easy as possible.

12. Iterate over the lines and check for ``"coala"`` with an uppercase ``"C"``.
    Use ``string``'s ``find`` function like so:

::

    #include <iostream>
    #include <string>

    #include "json.hpp"

    using json = nlohmann::json;
    using namespace std;

    json in;
    json out;
    string origin;

    void init_results(string bear_name) {
        origin = bear_name;
        out["results"] = json::array({});
    }

    void add_result(string message, int line, int column, int severity) {
        json result = {
            {"origin", origin},
            {"message", message},
                {"affected_code", json::array({{
                    {"file", in["filename"]},
                    {"start", {
                        {"column", column},
                        {"file", in["filename"]},
                        {"line", line}
                    }},
                    {"end", {
                        {"column", column+6},
                        {"file", in["filename"]},
                        {"line", line}
                    }}
                }})},
            {"severity", severity}
        };
        out["results"] += result;
    }

    int main() {

        cin >> in;

        init_results("coalaCheckBear");

        int i = 0;
        for (auto it=in["file"].begin(); it !=in["file"].end(); it++) {
            i++;
            string line = *it;
            size_t found = line.find("Coala");
            while (found != string::npos) {
                add_result("Did you mean 'coala'?", i, found, 2);
                found = line.find("Coala", found+1);
            }
        }

        cout << out;

        return 0;
    }

13. After building the executable it has to be added to the ``PATH`` env
    variable. It is possible to modify the wrapper and give it the full
    path. Add the current directory to the ``PATH`` like so:

::

    $ export PATH=$PATH:$PWD

The last step is to test if everything is working properly. This is the
testfile used in this tutorial (
`testfile <https://raw.githubusercontent.com/Redridge/coalaCheckBear-cpp/master/testfile>`__).

14. Execute the Bear by running:

::

    $ coala -d . -b coalaCheckBear -f testfile

.. note::

  If you have ran ``coala`` over a file more than once without modifying it,
  coala will try to cache it. In order to avoid such behavior add
  ``--flush-cache`` at the end of the command.

Writing a Bear With Javascript and Node
---------------------------------------

This part of the tutorial will demonstrate how to make an External Bear that
uses a script that needs another binary to run (e.g. python, bash, node).

1. Run ``coala-bears-create -ext`` but supply ``node`` as the
   executable name.

.. note::

  This tutorial uses ``node v6.2.2``. It should work with older versions too
  but we suggest that you update.

When another binary is needed to run the source code, the ``create_arguments``
method comes in handy.

2. Add the source code file as an argument to the ``create_arguments`` method
   (so that the command becomes ``node coalaCheck.js``).

The ``create_arguments`` method returns a tuple so if only one
argument is added then a comma has to be used at the end
(e.g. ``(one_item,)``).

.. note::

    The ``LICENSE`` specified applies only to the python code. You can license
    your executable however you see fit.

::

    import os

    from coalib.bearlib.abstractions.ExternalBearWrap import external_bear_wrap


    @external_bear_wrap(executable='node',
                        settings={})
    class coalaCheckBear:
        """
        Checks for coala written with uppercase 'C'
        """
        LANGUAGES = {'All'}
        REQUIREMENTS = {'node'}
        AUTHORS = {'Me'}
        AUTHORS_EMAILS = {'me@mail.com'}
        LICENSE = 'AGPL'

        @staticmethod
        def create_arguments():
            return ('coalaCheck.js',)

3. Create ``coalaCheck.js`` and add basic I/O handling.

::

    var input = "";

    console.log = (msg) => {
        process.stdout.write(`${msg}\n`);
    };

    process.stdin.setEncoding('utf8');

    process.stdin.on('readable', () => {
        var chunk = process.stdin.read();
        if (chunk !== null) {
            input += chunk;
        }
    });

    process.stdin.on('end', () => {
        input = JSON.parse(input);
        console.log(JSON.stringify(input));
    });

4. The I/O can be tested by running ``node coalaCheck.js`` and
   supplying a valid JSON string in the stdin.
5. Add the init and the add result functions.

::

    var out = {};
    var origin;

    init_results = (bear_name) => {
        origin = bear_name;
        out["results"] = [];
    };

    add_result = (message, line, column, severity) => {
        var result = {
            "origin": origin,
            "message": message,
            "affected_code": [{
                    "file": input["filename"],
                    "start": {
                        "column": column,
                        "file": input["filename"],
                        "line": line
                    },
                    "end": {
                        "column": column+6,
                        "file": input["filename"],
                        "line": line
                    }
                }],
            "severity": severity
        };
        out["results"].push(result)
    };

6. Iterate over the lines and check for ``"coala"`` spelled with a capital
   ``"C"``. The final source should look like this:

::

    var input = "";
    var out = {};
    var origin;

    console.log = (msg) => {
        process.stdout.write(`${msg}\n`);
    };

    init_results = (bear_name) => {
        origin = bear_name;
        out["results"] = [];
    };

    add_result = (message, line, column, severity) => {
        var result = {
            "origin": origin,
            "message": message,
            "affected_code": [{
                    "file": input["filename"],
                    "start": {
                        "column": column,
                        "file": input["filename"],
                        "line": line
                    },
                    "end": {
                        "column": column+6,
                        "file": input["filename"],
                        "line": line
                    }
                }],
            "severity": severity
        };
        out["results"].push(result)
    };

    process.stdin.setEncoding('utf8');

    process.stdin.on('readable', () => {
        var chunk = process.stdin.read();
        if (chunk !== null) {
            input += chunk;
        }
    });

    process.stdin.on('end', () => {
        input = JSON.parse(input);
        init_results("coalaCheckBear");
        for (i in input["file"]) {
            var line = input["file"][i];
            var found = line.indexOf("Coala");
            while (found != -1) {
                add_result("Did you mean 'coala'?", parseInt(i)+1, found+1, 2);
                found = line.indexOf("Coala", found+1)
            }
        }
        console.log(JSON.stringify(out));
    });


In order to run this Bear there is no need to add the source code to the path
because the binary being run is ``node``. Although there is a problem: the
argument supplied will be looked up only in the current directory. To fix this
you can add the full path of the ``.js`` file in the argument list. In this
case just run the bear from the same directory as ``coalaCheck.js``. The code
for this example can be found
`here <https://github.com/Redridge/coalaCheckBear-js>`__.

The JSON Spec
-------------

coala will send you data in a JSON string via stdin and the executable has to
provide a JSON string via stdout. The specs are the following:

* input JSON spec

+--------------------------------+-------+-----------------------------------+
|Tree                            |Type   |Description                        |
+--------------------------------+-------+-----------------------------------+
|filename                        |str    |the name of the file being analysed|
+--------------------------------+-------+-----------------------------------+
|file                            |list   |file contents as a list of lines   |
+--------------------------------+-------+-----------------------------------+
|settings                        |obj    |settings as key:value pairs        |
+--------------------------------+-------+-----------------------------------+

* output JSON spec

+--------------------------------+-------+-----------------------------------+
|Tree                            |Type   |Description                        |
+--------------------------------+-------+-----------------------------------+
|results                         |list   |list of results                    |
+---+----------------------------+-------+-----------------------------------+
|   |origin                      |str    |usually the name of the bear       |
+---+----------------------------+-------+-----------------------------------+
|   |message                     |str    |message to be displayed to the user|
+---+----------------------------+-------+-----------------------------------+
|   |affected_code               |list   |contains SourceRange objects       |
+---+---+------------------------+-------+-----------------------------------+
|   |   |file                    |str    |the name of the file               |
+---+---+------------------------+-------+-----------------------------------+
|   |   |start                   |obj    |start position of affected code    |
+---+---+---+--------------------+-------+-----------------------------------+
|   |   |   |file                |str    |the name of the file               |
+---+---+---+--------------------+-------+-----------------------------------+
|   |   |   |line                |int    |line number                        |
+---+---+---+--------------------+-------+-----------------------------------+
|   |   |   |column              |int    |column number                      |
+---+---+---+--------------------+-------+-----------------------------------+
|   |   |end                     |obj    |end position of affected code      |
+---+---+---+--------------------+-------+-----------------------------------+
|   |   |   |file                |str    |the name of the file               |
+---+---+---+--------------------+-------+-----------------------------------+
|   |   |   |line                |int    |line number                        |
+---+---+---+--------------------+-------+-----------------------------------+
|   |   |   |column              |int    |column number                      |
+---+---+---+--------------------+-------+-----------------------------------+
|   |severity                    |int    |severity of the result (0-2)       |
+---+----------------------------+-------+-----------------------------------+
|   |debug_msg                   |str    |message to be shown in DEBUG log   |
+---+----------------------------+-------+-----------------------------------+
|   |additional_info             |str    |additional info to be displayed    |
+---+----------------------------+-------+-----------------------------------+

.. note::

  The output JSON spec is the same as the one that ``coala --json`` uses. If you
  ever get lost you can run ``coala --json`` over a file and check the results.
