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
            (r'(".+?")(:)', bygroups(String, Punctuation), 'instance'),
            (r"('.+?')(:)", bygroups(String, Punctuation), 'instance'),
            (r'(\S+?)(:)', bygroups(String, Punctuation), 'instance'),
            (r'\}', Punctuation, '#pop'),
        ],
        'instance': [
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)(\S+)(,)", bygroups(Text, Name.Attribute, Text, Operator, Text, String, Punctuation)),
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)('.+')(,)", bygroups(Text, Name.Attribute, Text, Operator, Text, String, Punctuation)),
            (r'(\s*)(\S+?)(\s*)(=>)(\s*)(".+")(,)', bygroups(Text, Name.Attribute, Text, Operator, Text, String, Punctuation)),
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)(\S+)(;)", bygroups(Text, Name.Attribute, Text, Operator, Text, String, Punctuation), '#pop'),
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)('.+')(;)", bygroups(Text, Name.Attribute, Text, Operator, Text, String, Punctuation), '#pop'),
            (r'(\s*)(\S+?)(\s*)(=>)(\s*)(".+")(;)', bygroups(Text, Name.Attribute, Text, Operator, Text, String, Punctuation), '#pop'),
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)([^;'\"\s]+)", bygroups(Text, Name.Attribute, Text, Operator, Text, String)),
            (r"(\s*)(\S+?)(\s*)(=>)(\s*)('.*')", bygroups(Text, Name.Attribute, Text, Operator, Text, String)),
            (r'(\s*)(\S+?)(\s*)(=>)(\s*)(".+")', bygroups(Text, Name.Attribute, Text, Operator, Text, String)),
        ],
    }
