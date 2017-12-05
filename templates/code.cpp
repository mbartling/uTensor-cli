#include "{{ name }}.h"

namespace {{ name }} {
    
    Model::Model(){
        //Handle the idx loading and graph creation in ctx
        // Constants and Intermediates
        {% for name, intermediate in intermediates.iteritems() %}{{ intermediate["definition"] }}
        {% endfor %}

    }
    Model::~Model(){
        //Optionally destroy stuff

    }

    {% for definition in definitions %}{{definition}}
    {% endfor %}
}
