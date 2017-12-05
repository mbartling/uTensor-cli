from tf_viewer import GraphInspector, load_graph
import re
import sys

def clean_name(name):
    """Change tensorflow names to allowed C names
    """
    return re.sub("[/:]", "_", name)
class GraphDumper:
    hitList = []
    constList = []
    intermediateList = set()
    inputList = set()
    def find_inputs(self, graph, name):
        p = graph.get_operation_by_name(name)
        print p.node_def
        # Constants should be exposed to the Model
        if p.type == "Const":
            self.constList.append(p)
        
        # Placeholders are user defined inputs
        if p.type == "Placeholder":
            self.inputList.add(p)

        for i in p.inputs:
            tensor = graph.get_tensor_by_name(i.name)
            if i.name not in self.hitList:
                self.hitList.append(i.name)
                # Intermediate tensors should be exposed to the class
                # These are temporary tensors between operations
                self.intermediateList.add(i)
                #print(i)
                self.find_inputs(graph, tensor.op.name)
    def get_const_templates(self):
        print "=========CONST LIST=========="
        for i in self.constList:
            print i.node_def
    def get_intermediate_templates(self):
        print "=========Intermediate LIST=========="
        for i in self.intermediateList:
            print clean_name(i.name)

    def get_inputs(self):
        print "=========Input List================="
        for i in self.inputList:
            print i.name

#graph = load_graph("test-models/lin_reg_model.pb", name="")
graph = load_graph(sys.argv[1], name="")

G = GraphDumper()
g = G.find_inputs(graph, sys.argv[2])
G.get_const_templates()
G.get_intermediate_templates()
G.get_inputs()
