def remove_newlines_and_space(tag):
    for child in tag.children:
        if child == '\n':
            child.replace_with('')
        elif '\n' in child and child.string:
            child.replace_with(" ".join(child.string.split()))


def strip(tag):
    children = list(tag.children)
    for child in [children[0], children[-1]]:
        if child == '\n':
            child.replace_with('')
        return
