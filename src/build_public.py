import os
import shutil


def clone_folder_to_folder(src_folder, dist_folder):
    src_elements = os.listdir(src_folder)
    if len(src_elements) == 0:
        return
    for src_element in src_elements:
        element_path = os.path.join(src_folder, src_element)
        if os.path.isfile(element_path):
            shutil.copy(element_path, dist_folder)
            print(f"File {src_element} copy operation src: {src_folder} to dist: {dist_folder}")
        else:
            if not os.path.exists(os.path.join(dist_folder, src_element)):
                os.mkdir(os.path.join(dist_folder, src_element))
                print(f"Direction created at dist: {os.path.join(dist_folder, src_element)}")
            clone_folder_to_folder(element_path, os.path.join(dist_folder, src_element))




def build_public():

    public_path = 'public'
    static_path = 'static'
    #HARD RESET PUBLIC
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    if not os.path.exists(public_path):
        os.mkdir(public_path)

    clone_folder_to_folder(static_path, public_path)


if __name__ == "__main__":
    build_public()