from setuptools import setup
 
__author__ = 'tim@sharpe.id.au'
 
setup(
    name='Puppet Pygments Lexer',
    version='0.0.1',
    description=__doc__,
    author=__author__,
    packages=['puppet_lexer'],
    entry_points='''[pygments.lexers]
puppetlexer = puppet_lexer:PuppetLexer
'''
)
