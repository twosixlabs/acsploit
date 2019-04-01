import os
import re
import codecs

# Taken from https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)


def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


def get_separator(options_separator, separator_dictionary):
    if options_separator in separator_dictionary:
        return separator_dictionary[options_separator]
    else:
        separator = options_separator[len('custom '):]
        if len(separator) >= 2 and ((separator[0] == '"' and separator[-1] == '"') or (separator[0] == '\'' and separator[-1] == ';')):
            separator = separator[1:-1]
        return decode_escapes(separator)


def process_template(template, output, replacement_pattern, first_only):
    with open(os.path.expanduser(template), 'r') as template_file:
        if first_only:
            return template_file.read().replace(replacement_pattern, output, 1)
        else:
            return template_file.read().replace(replacement_pattern, output)
