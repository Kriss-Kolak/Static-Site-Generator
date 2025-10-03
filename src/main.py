from build_public import build_public
from generate_page import generate_page, generate_pages_recursive

def main():

    build_public()
    generate_pages_recursive('content', 'template.html', 'public')

main()
