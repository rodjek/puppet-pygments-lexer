from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

class PuppetLexer(RegexLexer):
    name = 'Puppet'
    aliases = ['puppet']
    filenames = ['*.pp']

    tokens = {
        'root': [
            (r' .*\n', Text),
            (r'\s*#.*\n', Comment.Singleline),
            (r'(class)(\s*)(.*?)(\s*)(\{)', bygroups(Keyword.Declaration, Text, Name.Class, Text, Punctuation)),
            (r'(.*?)(\s*)(\{)(\s*)', bygroups(Name.Class, Text, Punctuation, Text), 'resource'),
            (r'.*\n', Text),
        ],
        'resource': [
            (r'(\s*)(".+?")(:)', bygroups(Text, String, Punctuation), 'instance'),
            (r"(\s*)('.+?')(:)", bygroups(Text, String, Punctuation), 'instance'),
            (r'(\s*)(\S+?)(:)', bygroups(Text, String, Punctuation), 'instance'),
            (r'(\s*)(\})', bygroups(Text, Punctuation), '#pop'),
        ],
        'instance': [
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)", bygroups(Text, Name.Attribute, Text, Operator, Text), 'value'),
            (r'(\,)', Punctuation),
            (r'(;)', Punctuation, '#pop:2'),
        ],
        'value': [
            (r"([A-Z].+?)(\[)(\".+\"|'.+')(\])", bygroups(Name.Namespace, Punctuation, String, Punctuation), '#pop'),
            (r'[0-9]+', Number, '#pop'),
            (r"[^;,\"'\s]+", String, '#pop'),
            (r'".+?"', String, '#pop'),
            (r"'.+?'", String, '#pop'),
        ],
    }
