from jinja2 import Template
from tf_viewer import GraphInspector, load_graph
import glob
import os
import re
import sys

def clean_name(name):
    """Change tensorflow names to allowed C names
    """
    return re.sub("[/:]", "_", name)

def find_const_file(files, name):
    for f in files:
        if name in f:
            return f
    return ""

def get_c_type(m_type):
    if m_type == "DT_QUINT8" or m_type == "quint8":
        return "uint8_t"
    if m_type == "DT_QUINT16" or m_type == "quint16":
        return "uint16_t"
    if m_type == "DT_QUINT32" or m_type == "quint32":
        return "uint32_t"
    if m_type == "DT_FLOAT" or m_type == "float32":
        return "float"
    if m_type == "DT_INT32" or m_type == "int32":
        return "int32_t"
    if m_type == "DT_INT64" or m_type == "int64":
        return "int64_t"

class GraphDumper:
    hitList = []
    constList = []
    intermediateList = set()
    inputList = set()
    opStack = []

    def __init__(self, fName):
        self.bName = os.path.splitext(os.path.basename(fName))[0]

    def find_inputs(self, graph, name):
        obj = {}
        self._find_inputs(graph, name)
    
        obj["opStack"] = self.opStack
        obj["inputs"] = self.inputList
        obj["intermediates"] = {}

        for i in G.get_intermediate_templates():
            obj["intermediates"][i["name"]] = i
    
        return obj

    def _find_inputs(self, graph, name):
        p = graph.get_operation_by_name(name)
        print p.node_def
        # Constants should be exposed to the Model
        if p.type == "Const":
            self.constList.append(p)
        
        # Placeholders are user defined inputs
        if p.type == "Placeholder":
            self.inputList.add(p)
        else:
            # Placeholders will be a part of the function call
            self.opStack.append(p)

        print list(p.inputs)
        print list(p.outputs)
        print "-------------"
        for i in p.inputs:
            tensor = graph.get_tensor_by_name(i.name)
            if i.name not in self.hitList:
                self.hitList.append(i.name)
                # Intermediate tensors should be exposed to the class
                # These are temporary tensors between operations
                self.intermediateList.add(i)
                self._find_inputs(graph, tensor.op.name)

#    def dump_graph_constants(self, graph, op):
#        inspector = GraphInspector(graph)
#        bName = os.path.splitext(os.path.basename(self.fName))[0]
#    
#        # Handle optional quantization
#    
#        # Assume path exists
#        inspector.snap(op.name, path=bName)
    def get_const_templates(self):
        for i in self.constList:
            obj = {}
            obj["name"] = clean_name(i.name)
            obj["declaration"] = "S_Tensor %s;" % obj["name"]
            yield obj

    def get_intermediate_templates(self):
        files = glob.glob("%s/*/*/*" % self.bName)
        print files
        for i in self.intermediateList:
            obj = {}
            obj["name"] = clean_name(i.name)
            obj["declaration"] = "S_Tensor %s;" % obj["name"]
            t_file_path = find_const_file(files, obj["name"])
            if t_file_path:
                with open(os.path.join("templates", "const.tmplt")) as fp:
                    t = Template(fp.read())
                    obj["definition"] = t.render(t_name=obj["name"], t_type=get_c_type(i.dtype.name), t_file_path=t_file_path)
            else:
                with open(os.path.join("templates", "intermediate.tmplt")) as fp:
                    t = Template(fp.read())
                    obj["definition"] = t.render(t_name=obj["name"], t_type=get_c_type(i.dtype.name))

            yield obj

    def get_inputs(self):
        print "=========Input List================="
        for i in self.inputList:
            print i.name

if __name__ == '__main__':
    import pprint
    #graph = load_graph("test-models/lin_reg_model.pb", name="")
    graph = load_graph(sys.argv[1], name="")
    
    G = GraphDumper(sys.argv[1])
    obj = G.find_inputs(graph, sys.argv[2])
#    g = obj["opStack"]
#    
#    print "==========OP stack============"
#    while g:
#        op = g.pop()
#        print op.node_def
#    
#    print "=========Intermediate LIST=========="
#    for i in G.get_intermediate_templates():
#        print i
#    G.get_inputs()

    pprint.pprint(obj)

