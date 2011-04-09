from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *

# TODO
# File { foo => bar }
# class foo($bar) {
# File["foo"] -> File["bar"] -> File["baz"] <- ~> 
# import ''
# Resource <<| foo == bar |>>
# Resource <| foo == bar |>
# regexp strings

class PuppetLexer(RegexLexer):
    name = 'Puppet'
    aliases = ['puppet']
    filenames = ['*.pp']

    tokens = {
        'root': [
            (r'(\s*)(include)(\s*)(\S+)(\n)', bygroups(Text, Keyword.Namespace, Text, Name.Class, Text)),
            (r'(class)(\s*)(.*?)(\s*)(inherits)?(\s*)(\S+)?(\s*)(\{)', bygroups(Keyword.Declaration, Text, Name.Class, Text, Keyword.Declaration, Text, Name.Class, Text, Punctuation)),
            (r'(define)(\s*)(.*?)(\()', bygroups(Keyword.Declaration, Text, Name.Class, Punctuation), 'argumentlist'),
            (r'(\s*)(if)(\s*)', bygroups(Text, Keyword, Text), 'if'),
            (r'(\s*)(\})(\s*)(else)(\s*)(\{)', bygroups(Text, Punctuation, Text, Keyword, Text, Punctuation)),
            (r'(\s*)(\$\w+)(\s*)(=)(\s*)', bygroups(Text, Name.Variable, Text, Operator, Text), 'var_assign'),
            (r'(\s*)([A-Z]\S+)(\[)', bygroups(Text, Name.Namespace, Punctuation), ('instance', 'defined_resource_namevar')),
            (r'(\s*)(case)(\s*)', bygroups(Text, Keyword, Text), 'case_conditional'),
            (r'(\s*)(\w+)(:)(\s*)(\{)', bygroups(Text, Name.Attribute, Punctuation, Text, Punctuation)),
            (r'(\s*)(\w+?)(\()', bygroups(Text, Name.Function, Punctuation), 'functionarglist'),
            (r'(\s*)([A-Z][\w\:]+)(\s*)(<<?\|)', bygroups(Text, Name.Namespace, Text, Punctuation), 'virtual'),
            (r'(.*?)(\s*)(\{)(\s*)', bygroups(Name.Class, Text, Punctuation, Text), 'resource'),
            (r'(\s*)(\})', bygroups(Text, Punctuation)),
            (r'(\S+)(\()', bygroups(Name.Function, Punctuation)),
            (r'\s*#.*\n', Comment.Singleline),
            (r'\s*\n', Text),
        ],
        'defined_resource_namevar': [
            (r'"', String, 'dblstring'),
            (r"'.+'", String),
            (r'[^\s\]]+', String),
            (r'(\])(\s*)(\{)', bygroups(Punctuation, Text, Punctuation), '#pop'),
            (r'\s', Text),
        ],
        'resource': [
            (r'(\s*)(")', bygroups(Text, String), 'dblstring'),
            (r"(\s*)('.+?')(:)", bygroups(Text, String, Punctuation), 'instance'),
            (r'(\s*)(\$\S+)(:)', bygroups(Text, Name.Variable, Punctuation), 'instance'),
            (r'(\s*)(\S+?)(:)', bygroups(Text, String, Punctuation), 'instance'),
            (r'(\s*)(\[)', bygroups(Text, Punctuation), 'valarray'),
            (r'(\s*)(\})', bygroups(Text, Punctuation), '#pop'),
        ],
        'case_conditional': [
            (r'"', String, 'dblstring'),
            (r"'.+'", String),
            (r'\$\w+', Name.Variable),
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'functionarglist'),
            (r'\s', Text),
            (r'\{', Punctuation, '#pop'),
        ],
        'instance': [
            (r"(\S+?)(\s*)(=>)(\s*)", bygroups(Name.Attribute, Text, Operator, Text), 'value'),
            (r'(\,)', Punctuation),
            (r'(\?)(\s*)(\{)', bygroups(Operator, Text, Punctuation), '#push'),
            (r'\}?;', Punctuation, '#pop'),
            (r'\}\,', Punctuation),
            (r'#.*\n', Comment.Singleline),
            (r'\s', Text),
            (r'', Text, '#pop'),
        ],
        'value': [
            (r"([A-Z].+?)(\[)", bygroups(Name.Namespace, Punctuation), 'valarray'),
            (r'\$\S+', Name.Variable, '#pop'),
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'functionarglist'),
            (r"[^\[;,\"'\s\}\]\?]+", String, '#pop'),
            (r'"', String, 'valdblstring'),
            (r'\[', Punctuation, 'valarray'),
            (r"'.+?'", String, '#pop'),
            (r'\s', Text),
            (r'\]', Punctuation, '#pop'),
            (r'', Text, '#pop'),
        ],
        # TODO: test \" in argument
        'argumentlist': [
            (r"(\$\w+)(\s*)(=)(\s*)(\".*?\"|'.*?'|\w+)(\,)?(\s*)", bygroups(Name.Variable, Text, Operator, Text, String, Punctuation, Text)),
            (r'(\$\w+)(\s*)(=)(\s*)(\[)', bygroups(Name.Variable, Text, Operator, Text, Punctuation), 'valarray'),
            (r'(\$\w+)(\,)?(\s*)', bygroups(Name.Variable, Punctuation, Text)),
            (r'(\))(\s*)(\{)', bygroups(Punctuation, Text, Punctuation), '#pop'),
            (r'\,', Punctuation),
            (r'\s', Text),
        ],
        'valdblstring': [
            (r'\$\{.+?\}', Name.Variable),
            (r'(?:\\(?:[bdefnrstv\'"\\/]|[0-7][0-7]?[0-7]?|\^[a-zA-Z]))', String.Escape),
            (r'[^"\\\$]+', String),
            (r'\$', String),
            (r'"', String, '#pop:2'),
        ],
        'dblstring': [
            (r'\$\{.+?\}', Name.Variable),
            (r'(?:\\(?:[bdefnrstv\'"\\/]|[0-7][0-7]?[0-7]?|\^[a-zA-Z]))', String.Escape),
            (r'[^"\\\$]+', String),
            (r'\$', String),
            (r'(")(\s*)(:)', bygroups(String, Text, Punctuation), ('#pop', 'instance')),
            (r'"', String, '#pop'),
        ],
        'valarray': [
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'functionarglist'),
            (r'([A-Z].+?)(\[)', bygroups(Name.Namespace, Punctuation), '#push'),
            (r"'.*?'", String),
            (r'"', String, 'dblstring'),
            (r'\$\w+', Name.Variable),
            (r'[^\s\,\]]+', String),
            (r'\,', Punctuation),
            (r'\s', Text),
            (r'\]:', Punctuation, ('#pop', 'instance')),
            (r'\]', Punctuation, '#pop'),
            (r'', Text, '#pop'),
        ],
        'conditional_items': [
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'functionarglist'),
            (r'(\$\w+)(\s*)', bygroups(Name.Variable, Text)),
            (r'"', String, 'dblstring'),
            (r"'.*'", String),
            (r'(\[|\]|\*\*|<<?|>>?|in|and|or|not|>=|<=|<=>|=~|={3}|!~|&&?|\|\||\.{1,3})', Operator),
            (r'[-+/*%=<>&!^|~]=?', Operator),
            (r'(true|false)(\s*)', bygroups(Keyword.Constant, Text)),
            (r'(\()(\s*)', bygroups(Punctuation, Text)),
            (r'(\))(\s*)', bygroups(Punctuation, Text)),
            (r'\d+', Number),
            (r'\w+', String),
            (r'\s', Text),
        ],
        'if': [
            include('conditional_items'),
            (r'\{', Punctuation, '#pop'),
        ],
        'functionarglist': [
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), '#push'),
            (r'(\$\w+)(\,)?(\s*)', bygroups(Name.Variable, Punctuation, Text)),
            (r'(\d+)(\,)?(\s*)', bygroups(Number, Punctuation, Text)),
            (r'"', String, 'dblstring'),
            (r'\)\,[ \t]+', Punctuation, '#pop'),
            (r'\)\,', Punctuation, '#pop:2'),
            (r'\)', Punctuation, '#pop'),
        ],
        'var_assign': [
            (r'(\w+)(\()', bygroups(Name.Function, Punctuation), 'functionarglist'),
            (r'(\$\w+)(\s*)', bygroups(Name.Variable, Text)),
            (r'"', String, 'dblstring'),
            (r"'.*'", String),
            (r'(\[|\]|\*\*|<<?|>>?|in|and|or|not|>=|<=|<=>|=~|={3}|!~|&&?|\|\||\.{1,3})', Operator),
            (r'[-+/*%=<>&!^|~]=?', Operator),
            (r'(true|false)(\s*)', bygroups(Keyword.Constant, Text)),
            (r'(\()(\s*)', bygroups(Punctuation, Text)),
            (r'(\))(\s*)', bygroups(Punctuation, Text)),
            (r'\d+', Number),
            (r'\w+', String),
            (r'\n', Punctuation, '#pop'),
            (r'\s', Text),
            (r'', Text, '#pop'),
        ],
        'virtual': [
            (r'\|>>?', Punctuation, '#pop'),
            include('conditional_items'),
        ],
    }
