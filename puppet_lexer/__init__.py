from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

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
            (r'(.*?)(\s*)(\{)(\s*)', bygroups(Name.Class, Text, Punctuation, Text), 'resource'),
            (r'(\s*)(\})', bygroups(Text, Punctuation)),
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
            (r"([A-Z].+?)(\[)(\".+\"|'.+')(\])", bygroups(Name.Namespace, Punctuation, String, Punctuation), '#pop'),
            (r'[0-9]+', Number, '#pop'),
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
        'if': [

        ],
    }
