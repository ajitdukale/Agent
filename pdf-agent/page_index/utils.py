import PyPDF2
import os
import json
import copy
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def get_pdf_title(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    meta = pdf_reader.metadata
    title = meta.title if meta and meta.title else 'Untitled'
    return title

def get_pdf_name(pdf_path):
    return os.path.basename(pdf_path)

def get_number_of_pages(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    return len(pdf_reader.pages)

def get_text_of_pages(pdf_path, start_page, end_page, tag=True):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(start_page - 1, end_page):
        page_text = pdf_reader.pages[page_num].extract_text()
        if tag:
            text += f"<start_index_{page_num+1}>\n{page_text}\n<end_index_{page_num+1}>\n"
        else:
            text += page_text
    return text

def structure_to_list(structure):
    if isinstance(structure, dict):
        nodes = [structure]
        if 'nodes' in structure:
            nodes.extend(structure_to_list(structure['nodes']))
        return nodes
    elif isinstance(structure, list):
        nodes = []
        for item in structure:
            nodes.extend(structure_to_list(item))
        return nodes

def get_leaf_nodes(structure):
    if isinstance(structure, dict):
        if not structure.get('nodes'):
            return [structure]
        else:
            leaf_nodes = []
            for key in structure:
                if key == 'nodes':
                    leaf_nodes.extend(get_leaf_nodes(structure[key]))
            return leaf_nodes
    elif isinstance(structure, list):
        leaf_nodes = []
        for item in structure:
            leaf_nodes.extend(get_leaf_nodes(item))
        return leaf_nodes

def list_to_tree(data):
    def get_parent_structure(structure):
        if not structure:
            return None
        parts = str(structure).split('.')
        return '.'.join(parts[:-1]) if len(parts) > 1 else None

    nodes = {}
    root_nodes = []

    for item in data:
        structure = item.get('structure')
        node = {
            'title': item.get('title'),
            'start_index': item.get('start_index'),
            'end_index': item.get('end_index'),
            'nodes': []
        }

        nodes[structure] = node
        parent_structure = get_parent_structure(structure)

        if parent_structure and parent_structure in nodes:
            nodes[parent_structure]['nodes'].append(node)
        else:
            root_nodes.append(node)

    def clean_node(node):
        if not node['nodes']:
            del node['nodes']
        else:
            for child in node['nodes']:
                clean_node(child)
        return node

    return [clean_node(node) for node in root_nodes]

def post_processing(structure, end_physical_index):
    for i, item in enumerate(structure):
        item['start_index'] = item.get('physical_index')
        if i < len(structure) - 1:
            item['end_index'] = structure[i + 1]['physical_index'] - 1
        else:
            item['end_index'] = end_physical_index
    return list_to_tree(structure)

def add_node_text(node, pdf_pages):
    if isinstance(node, dict):
        start = node.get('start_index') - 1
        end = node.get('end_index')
        node['text'] = "\n".join([pdf_pages[i][0] for i in range(start, end)])
        if 'nodes' in node:
            add_node_text(node['nodes'], pdf_pages)
    elif isinstance(node, list):
        for child in node:
            add_node_text(child, pdf_pages)
