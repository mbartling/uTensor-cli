#include "utensor.h"

namespace {{ name }} {
    
    class Model {
        private:
            Context ctx;
        public:
            Model();
            ~Model();

            {% for declaration in declarations %}
            {{declaration}}
            {% endfor %}

    };
}
