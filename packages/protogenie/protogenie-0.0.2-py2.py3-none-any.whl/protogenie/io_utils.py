from typing import List
import os


def get_name(output_folder, dataset, filename):
    return os.path.join(output_folder, dataset, os.path.basename(filename))


def add_sentence(
        output_folder: str, dataset: str, filename: str,
        sentence: List[str], source_marker: str, output_marker: str):
    """ Write a sentence in the given dataset

    :param output_folder:
    :param dataset:
    :param filename:
    :param sentence:
    :return:
    """
    filename = get_name(output_folder, dataset, filename)
    if not os.path.isfile(filename):
        mode = "w"
    else:
        mode = "a"
    with open(filename, mode) as f:
        f.write("".join([s.replace(source_marker, output_marker) for s in sentence])+"\n")  # Add a secondary line break to keep things separated
