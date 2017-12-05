import argparse
from jinja2 import Template
from json import dumps
import os
import shutil
import sys
from tf_viewer import GraphInspector, load_graph
from graph_dumper import GraphDumper, clean_name
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-q", "--quantize", help="Quantize graph", action="store_true")
parser.add_argument("-o", help="override output name", metavar="NAME")
parser.add_argument("file", help="input protobuf file")
parser.add_argument('-m','--model-outputs', nargs='+', help='<Required> select model outputs to dump to uTensor', required=True, dest="mOutputs", metavar="var")

def dump_graph_constants(fName):
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

def generate_output_graph(graph, fName, outVar):
    """ Given an output variable generate a uTensor graph.
        Basic idea: build a stack of operations backwards from an output variable to input variables.
        Do breadth first graph traversal.

        [Return] functiond declaration and definition
    """
    declaration = ''
    definition = ''
    inputs = []
    input_tensors = []

    G = GraphDumper(fName)
    obj = G.find_inputs(graph, outVar)
    for m_input in obj["inputs"]:
        inputs.append(m_input.name)
        input_tensors.append(clean_name(m_input.outputs[0].name))

    with open(os.path.join("templates", "function_decl.tmplt")) as fp:
        t = Template(fp.read())
        declaration = t.render(decl_name=outVar, num_inputs=len(inputs), inputs=inputs)
    with open(os.path.join("templates", "function_def.tmplt")) as fp:
        t = Template(fp.read())
        definition = t.render(def_name=outVar, num_inputs=len(inputs), inputs=input_tensors, output=clean_name(graph.get_operation_by_name(outVar).outputs[0].name), graphOps=obj["operations"])
    return (declaration, definition, obj["intermediates"])


def generate(fName, args):
    bName = os.path.splitext(os.path.basename(fName))[0]
    graph = load_graph(fName, name="")
    defs = []
    decls = []
    intermediates = {}
    for mOutput in args.mOutputs:
        (declaration, definition, intermediates_l) = generate_output_graph(graph, fName, mOutput)
        defs.append(definition)
        decls.append(declaration)
        for key in intermediates_l.keys():
            intermediates[key] = intermediates_l[key]

    print("Generating: " + bName + ".hpp")
    with open(os.path.join("templates", "header.hpp")) as fp:
        t = Template(fp.read())
        print(t.render(name=bName, declarations=decls, intermediates=intermediates))
    
    print("Generating: " + bName + ".cpp")
    with open(os.path.join("templates", "code.cpp")) as fp:
        t = Template(fp.read())
        print(t.render(name=bName, definitions=defs, intermediates=intermediates))


def main():
    args = parser.parse_args()
    if args.verbose:
        print "verbosity turned on"

    dump_graph_constants(args.file)
    generate(args.file, args)

if __name__ == '__main__':
    main()
