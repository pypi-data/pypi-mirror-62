_RULE_FILE = {}


def get_rulefile():
    return _RULE_FILE


def set_rulefile(value):
    global _RULE_FILE
    _RULE_FILE = value
