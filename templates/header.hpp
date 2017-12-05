#include "utensor.h"

namespace {{ name }} {

    class Model {
        private:
            TensorIdxImporter t_import;
            Context ctx;
        public:
            Model();
            ~Model();

            {% for declaration in declarations %}
            {{declaration}}
            {% endfor %}

    };
}
