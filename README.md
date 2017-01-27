# landing-frontend
coala Landing Page - https://gitlab.com/coala/landing is needed as backend


## Usage

To run locally:

    $ git clone https://github.com/coala/landing-frontend.git
    $ cd landing-frontend
    $ python -m SimpleHTTPServer 8080


Open http://localhost:8080 in your browser.


## Adding new code snippets

- Open /data/snippets and add .md file with code snippet in it.
- Enclose that code snippet with ```.
- Open /resources/js/snippets.js and add the name of newly added
 language and the name of its corresponding .md file.
