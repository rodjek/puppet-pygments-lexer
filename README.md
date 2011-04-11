# Pygments lexer for the Puppet DSL

Pygments is a popular syntax highlighting tool used in many sites (like 
github.com).  This module allows Pygments to properly read Puppet manifests
so that we get nice pretty pages of code to look at too.

While this is pretty much working fine on my manifests, I'm not using all the 
features of the DSL.  Help me out by testing this out on your manifests and
reporting any rendering errors.  This is my first Pygments lexer, so I'm sure
this could be made more efficient if you wanted to as well.

## INSTALL

    python setup.py install

## HACKING

    vim puppet_lexer/__init__.py
    python setup.py install
    pygmentize -O full -f html -o <output file> <input file>
