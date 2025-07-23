import re
from node import Node


def query_selector_all(root: Node, selector_str: str) -> list[Node]:
    selectors = [parse_selector(s.strip()) for s in selector_str.split(",")]
    result = []

    def dfs(node: Node):
        for sel in selectors:
            if matches(node, sel):
                result.append(node)
                break
        for child in node.children:
            dfs(child)

    dfs(root)
    return result


def parse_selector(selector: str) -> dict:
    """
    Parses a selector string like 'div#id.class1.class2' into:
    {
        'tag': 'div',
        'id': 'id',
        'classes': ['class1', 'class2']
    }
    """
    tag = None
    id_ = None
    classes = []

    pattern = r'(^[a-zA-Z][\w-]*)|(#([\w-]+))|(\.([\w-]+))'
    for match in re.finditer(pattern, selector):
        if match.group(1):
            tag = match.group(1)
        elif match.group(3):
            id_ = match.group(3)
        elif match.group(5):
            classes.append(match.group(5))

    return {'tag': tag, 'id': id_, 'classes': classes}


def matches(node: Node, selector: dict) -> bool:

    if selector['tag'] and node.tag != selector['tag']:
        return False


    node_id = node.attributes.get("id")
    if selector['id'] and node_id != selector['id']:
        return False

    node_class = node.attributes.get("class", "")
    node_classes = node_class.split()

    for cls in selector['classes']:
        if cls not in node_classes:
            return False

    return True
