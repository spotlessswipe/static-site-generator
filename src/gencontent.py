import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entries = os.listdir(dir_path_content)
    print(entries)

    for entry in entries:
        os.makedirs(dest_dir_path, exist_ok=True)

        full_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(full_path):
            extension = os.path.splitext(entry)[1]
            if extension == '.md':
                destination_path = destination_path[:-3] + '.html'
                generate_page(full_path, template_path, destination_path, basepath)
        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, destination_path, basepath)




def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
