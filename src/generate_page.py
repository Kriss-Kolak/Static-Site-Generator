from markdown_blocks import markdown_to_html_node, extract_title
import os

def read_file(file_path) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = read_file(from_path)
    template = read_file(template_path)
    html_node = markdown_to_html_node(md)
    content = html_node.to_html()
    title = extract_title(md)
    replaced = template.replace('{{ Title }}', title)
    replaced = replaced.replace('{{ Content }}', content)

    replaced = replaced.replace('href="/', f'href="{basepath}')
    replaced = replaced.replace('src="/', f'src="{basepath}')
    with open(dest_path, 'w') as file:
        file.write(replaced)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    folder_content = os.listdir(dir_path_content)
    if len(folder_content) == 0:
        return 
    for content_object in folder_content:
        content_object_src_path = os.path.join(dir_path_content, content_object)
        content_object_dest_path = os.path.join(dest_dir_path, content_object) 
        if os.path.isfile(content_object_src_path) and content_object.endswith(".md"):
            content_object_dest_path = content_object_dest_path.replace('.md','.html')
            generate_page(content_object_src_path, template_path, content_object_dest_path, basepath)
        elif os.path.isdir(content_object_src_path):
            if not os.path.exists(content_object_dest_path):
                os.mkdir(content_object_dest_path)
            generate_pages_recursive(content_object_src_path, template_path, content_object_dest_path, basepath)
