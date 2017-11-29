#include "{{ name }}.h"

namespace {{ name }} {
    
    Model::Model(){
        //Handle the idx loading and graph creation in ctx

    }
    Model::~Model(){
        //Optionally destroy stuff

    }

    S_TENSOR Model::predict_proba({% for i in range(num_inputs-1) %}S_TENSOR input{{i}}, {% endfor %}S_TENSOR input{{ num_inputs-1 }}){
        {% for i in range(num_inputs) %}ctx.add(input{{i}}, "input{{i}}");{% endfor %}

        inference(ctx);
        return ctx.get("output");

    }
}
