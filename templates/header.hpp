#include "utensor.h"

namespace {{ name }} {
    
    class Model {
        private:
            Context ctx;
        public:
            Model();
            ~Model();

            S_TENSOR predict_proba({% for i in range(num_inputs-1) %}S_TENSOR input{{i}}, {% endfor %}S_TENSOR input{{ num_inputs-1 }});
    };
}
