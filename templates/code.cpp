#include "{{ name }}.h"

namespace {{ name }} {
    
    Model::Model(){
        //Handle the idx loading and graph creation in ctx

    }
    Model::~Model(){
        //Optionally destroy stuff

    }

    {% for definition in definitions %}
    {{definition}}
    {% endfor %}
}
