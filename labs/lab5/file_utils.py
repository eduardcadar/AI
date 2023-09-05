import tsplib95


def tspToNxGraph(file_path):
    pb = tsplib95.load(file_path)
    return pb.get_graph()
