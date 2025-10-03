import sys
from build_public import build
from generate_page import generate_page, generate_pages_recursive


def main():
    if len(sys.argv) != 2:
        print("Example usage: python3 main.py <basepath>")
        return
    
    build_path = 'docs'
    static_path = 'static'

    basepath = sys.argv[1]
    build(build_path, static_path)
    generate_pages_recursive('content', 'template.html', 'docs', basepath)


main()
