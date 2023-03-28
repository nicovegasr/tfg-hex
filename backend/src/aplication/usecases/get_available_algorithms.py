import os

def get_available_algorithms() -> list:
    path = os.path.dirname(os.path.realpath(__file__))
    algotihms_path = path.rsplit("aplication", 1)[0] + '/domain/algorithms/files'
    try:
        algoritmos = os.listdir(algotihms_path) 
        return algoritmos
    except:
        raise ValueError("Something is wrong with algorithm path files")