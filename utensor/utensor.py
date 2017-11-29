import argparse
from jinja2 import Template
import os
import shutil
import sys
from view_node import GraphInspector, load_graph

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-q", "--quantize", help="Quantize graph", action="store_true")
parser.add_argument("-o", help="override output name", metavar="NAME")
parser.add_argument("file", help="input protobuf file")
parser.add_argument('-m','--model-outputs', nargs='+', help='<Required> select model outputs to dump to uTensor', required=True, dest="mOutputs", metavar="var")

def process_graph(fName):
    graph = load_graph(fName, name="")
    inspector = GraphInspector(graph)
    bName = os.path.splitext(os.path.basename(fName))[0]

    # Handle optional quantization

    # Dump the constants to IDX files
    if os.path.exists(bName):
        shutil.rmtree(bName)
    os.mkdir(bName)

    for i in graph.get_operations():
        if i.type == "Const":
            inspector.snap(i.name, path=bName)

def generate(fName, numInputs):
    bName = os.path.splitext(os.path.basename(fName))[0]
    print("Generating: " + bName + ".hpp")
    with open(os.path.join("templates", "header.hpp")) as fp:
        t = Template(fp.read())
        print(t.render(name=bName, num_inputs=numInputs))
    
    print("Generating: " + bName + ".cpp")
    with open(os.path.join("templates", "code.cpp")) as fp:
        t = Template(fp.read())
        print(t.render(name=bName, num_inputs=numInputs))


def main():
    args = parser.parse_args()
    if args.verbose:
        print "verbosity turned on"

    print(args.mOutputs)
    sys.exit(-1)
    process_graph(args.file)
    generate(args.file, 3)

if __name__ == '__main__':
    main()
