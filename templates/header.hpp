#include "utensor.h"

namespace {{ name }} {

    class Model {
        private:
            TensorIdxImporter t_import;
            Context ctx;

            // Constants and Intermediates
            {% for name, intermediate in intermediates.iteritems() %}{{ intermediate["declaration"] }}
            {% endfor %}
        public:
            Model();
            ~Model();

            {% for declaration in declarations %}
            {{declaration}}
            {% endfor %}

    };
}
