coala-mobans
============= 
 
coala-moban is a collection of useful templates that are mainly used
by coala to have standardized configuration over all of the coala 
repositories.

These templates are applied using ``moban`` templating engine.

`Template Engine <https://en.wikipedia.org/wiki/Template_processor>`__ 

Usage
~~~~~
In order to apply templates of this repo to any of the coala repository :

1. Clone the coala-mobans repo. 

    ``$ git clone https://gitlab.com/coala/mobans coala-mobans``

2. Create a parent folder with coala repos and coala-moban as subdirectory.

3. **cd** into the root folder of any coala repository and run :

     ``$ moban``
     
This will automatically make all the necessary changes as mentioned in
the template files.

moban
~~~~~~~~~~
moban is a cli command tool which uses the high performance template 
engine (JINJA2) for static text generation.

`moban <http://moban.readthedocs.io/en/latest/>`__ 

Jinja2
~~~~~~
Jinja2 is a full featured template engine for Python. It has full unicode 
support, an optional integrated sandboxed execution environment, widely 
used and BSD licensed. It is similar to the Django template engine.

`Jinja2 <http://jinja.pocoo.org/docs/2.10/>`__
 
