from enum import Enum
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes
import textwrap

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def extract_title(markdown: str):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            splited = line.split('# ', 1)
            return splited[1]
    raise Exception('Title has not been found')

def heading_helper(block: str) -> tuple[str, str]:
    if block.startswith("# "):
        return ("h1", '#')
    elif block.startswith("## "):
        return ("h2", '##')
    elif block.startswith("### "):
        return ("h3", '###')
    elif block.startswith("#### "):
        return ("h4", '####')
    elif block.startswith("##### "):
        return ("h5", '#####')
    elif block.startswith("###### "):
        return ("h6", '######')
    else:
        raise Exception("Not a heading block type!")

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block: str):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def _extract_code_inner(block: str) -> str:
    assert block.startswith("```") and block.endswith("```")
    body = block[3:-3]
    # Drop language line if present
    if "\n" in body and not body.startswith("\n"):
        first, rest = body.split("\n", 1)
        # If first line isn’t empty, treat it as language tag
        if first.strip() != "":
            body = rest
        else:
            body = body.lstrip("\n")
    # Remove a single leading newline
    if body.startswith("\n"):
        body = body[1:]
    # Dedent uniformly
    return textwrap.dedent(body)

def text_to_children(text_nodes: list) -> list[HTMLNode]:
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_node = ParentNode(tag='div', children=[])
    for block in blocks:
        if block != "":
            new_parent_node = None
            block_type = block_to_block_type(block)
            if block_type == BlockType.HEADING:
                heading_tag_tuple = heading_helper(block)
                no_tag_block = block.replace(heading_tag_tuple[1], "").strip()
                text_nodes = text_to_textnodes(no_tag_block)
                html_nodes = text_to_children(text_nodes)
                new_parent_node = ParentNode(heading_tag_tuple[0], html_nodes)
                html_node.children.append(new_parent_node)
            elif block_type == BlockType.CODE:
                inner = _extract_code_inner(block)
                code_html_node = LeafNode("code", inner)
                new_parent_node = ParentNode("pre", [code_html_node])
                html_node.children.append(new_parent_node)
            elif block_type == BlockType.QUOTE:
                result = []
                for line in block.split("\n"):
                    result.append(line.lstrip(">").lstrip())
                no_tag_block = " ".join(result)
                text_nodes = text_to_textnodes(no_tag_block)
                html_nodes = text_to_children(text_nodes)
                new_parent_node = ParentNode('blockquote', html_nodes)
                html_node.children.append(new_parent_node)
            elif block_type == BlockType.OLIST:
                new_parent_node = ParentNode('ol', children=[])
                for index, line in enumerate(block.split("\n"), start = 1):
                    replaced = line.replace(f"{index}.", "").lstrip()
                    text_nodes = text_to_textnodes(replaced)
                    html_nodes = text_to_children(text_nodes)
                    li_parent = ParentNode('li', html_nodes)
                    new_parent_node.children.append(li_parent)
                html_node.children.append(new_parent_node)
            elif block_type == BlockType.ULIST:
                new_parent_node = ParentNode('ul', children=[])
                for index, line in enumerate(block.split("\n"), start = 1):
                    replaced = line.lstrip("- ").strip()
                    text_nodes = text_to_textnodes(replaced)
                    html_nodes = text_to_children(text_nodes)
                    li_parent = ParentNode('li', html_nodes)
                    new_parent_node.children.append(li_parent)
                html_node.children.append(new_parent_node)
            elif block_type == BlockType.PARAGRAPH:
                result = []
                for line in block.split("\n"):
                    result.append(line.strip())
                no_tag_block = " ".join(result)
                text_nodes = text_to_textnodes(no_tag_block)
                html_nodes = text_to_children(text_nodes)
                new_parent_node = ParentNode('p', html_nodes)
                html_node.children.append(new_parent_node)
            else:
                raise ValueError("invalid block type")
    return html_node