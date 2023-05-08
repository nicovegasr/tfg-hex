import os


def get_available_algorithms() -> list:
    path = os.path.dirname(os.path.realpath(__file__))
    algotihms_path = path.rsplit("aplication", 1)[0] + "/domain/algorithms/files"
    try:
        algorithms = [dir for dir in os.listdir(algotihms_path) if os.path.isdir(os.path.join(algotihms_path, dir))]
        return algorithms
    except:
        raise ValueError("Something is wrong with algorithm path files")
