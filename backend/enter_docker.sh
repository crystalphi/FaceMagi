CONTAINER=backend_py_web_1
if [ x`uname`x = xLinuxx ]; then
    CONTAINER=backend_py_web_1
else
    echo ''
fi

docker exec -it $CONTAINER /bin/bash

