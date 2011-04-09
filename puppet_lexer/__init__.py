from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

# TODO
# File { foo => bar }
# File["bar"] { baz => gronk }
# class foo inherits baz
# [Package["foo"], Package["bar"]]
# class foo($bar) {
# File["foo"] -> File["bar"] -> File["baz"] <- ~> 
#

class PuppetLexer(RegexLexer):
    name = 'Puppet'
    aliases = ['puppet']
    filenames = ['*.pp']

    tokens = {
        'root': [
            (r'(\s*)(include)(\s*)(\S+)(\n)', bygroups(Text, Keyword.Namespace, Text, Name.Class, Text)),
            (r'(class)(\s*)(.*?)(\s*)(\{)', bygroups(Keyword.Declaration, Text, Name.Class, Text, Punctuation)),
            (r'(define)(\s*)(.*?)(\()', bygroups(Keyword.Declaration, Text, Name.Class, Punctuation), 'argumentlist'),
            (r'(\s*)(if)(\s*)', bygroups(Text, Keyword, Text), 'if'),
            (r'(\s*)(\})(\s*)(else)(\s*)(\{)', bygroups(Text, Punctuation, Text, Keyword, Text, Punctuation)),
            (r'(.*?)(\s*)(\{)(\s*)', bygroups(Name.Class, Text, Punctuation, Text), 'resource'),
            (r'(\s*)(\})', bygroups(Text, Punctuation)),
            (r'(\S+)(\()', bygroups(Name.Function, Punctuation)),
            (r'\s*#.*\n', Comment.Singleline),
            (r'\s*\n', Text),
        ],
        # TODO: test \" in namevar
        'resource': [
            (r'(\s*)(".+?")(:)', bygroups(Text, String, Punctuation), 'instance'),
            (r"(\s*)('.+?')(:)", bygroups(Text, String, Punctuation), 'instance'),
            (r'(\s*)(\$\S+)(:)', bygroups(Text, Name.Variable, Punctuation), 'instance'),
            (r'(\s*)(\S+?)(:)', bygroups(Text, String, Punctuation), 'instance'),
            (r'(\s*)(\})', bygroups(Text, Punctuation), '#pop'),
        ],
        'instance': [
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)", bygroups(Text, Name.Attribute, Text, Operator, Text), 'value'),
            (r'(\,)', Punctuation),
            (r'(;)', Punctuation, '#pop'),
            (r'(\s*)(\})', bygroups(Text, Punctuation), '#pop:2'),
        ],
        'value': [
            # TODO: File['arr1', 'arr2'] support
            (r"([A-Z].+?)(\[)(\".+\"|'.+'|\S+)(\])", bygroups(Name.Namespace, Punctuation, String, Punctuation), '#pop'),
            (r'[0-9]+', Number, '#pop'),
            (r'\$\S+', Name.Variable, '#pop'),
            (r"[^;,\"'\s]+", String, '#pop'),
            (r'"', String, 'valdblstring'),
            (r"'.+?'", String, '#pop'),
        ],
        # TODO: test \" in argument
        'argumentlist': [
            (r"(\$\S+)(\s*)(=)(\s*)(\".*?\"|'.*?'|\S+)(\,)?(\s*)", bygroups(Name.Variable, Text, Operator, Text, String, Punctuation, Text)),
            (r'(\$\S+)(\,)?(\s*)', bygroups(Name.Variable, Punctuation, Text)),
            (r'(\))(\s*)(\{)', bygroups(Punctuation, Text, Punctuation), '#pop'),
        ],
        'valdblstring': [
            (r'(?:\\(?:[bdefnrstv\'"\\/]|[0-7][0-7]?[0-7]?|\^[a-zA-Z]))', String.Escape),
            (r'[^"\\]+', String),
            (r'"', String, '#pop:2'),
        ],
        'dblstring': [
            (r'(?:\\(?:[bdefnrstv\'"\\/]|[0-7][0-7]?[0-7]?|\^[a-zA-Z]))', String.Escape),
            (r'[^"\\]+', String),
            (r'"', String, '#pop'),
        ],
        'if': [
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'functionarglist'),
            (r'(\$\w+)(\s*)', bygroups(Name.Variable, Text)),
            (r'"', String, 'dblstring'),
            (r'(\[|\]|\*\*|<<?|>>?|and|or|not|>=|<=|<=>|=~|={3}|!~|&&?|\|\||\.{1,3})', Operator),
            (r'[-+/*%=<>&!^|~]=?', Operator),
            (r'(true|false)(\s*)', bygroups(Keyword.Constant, Text)),
            (r'(\()(\s*)', bygroups(Punctuation, Text)),
            (r'(\))(\s*)', bygroups(Punctuation, Text)),
            (r'\s', Text),
            (r'\{', Punctuation, '#pop'),
        ],
        'functionarglist': [
            (r'(\$\w+)(\,)?(\s*)', bygroups(Name.Variable, Punctuation, Text)),
            (r'(\d+)(\,)?(\s*)', bygroups(Number, Punctuation, Text)),
            (r'"', String, 'valdblstring'),
            (r'\)', Punctuation, '#pop'),
        ],
    }
