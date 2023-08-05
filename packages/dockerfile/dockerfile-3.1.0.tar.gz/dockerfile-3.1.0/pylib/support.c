#include <Python.h>

/* Will come from go */
PyObject* all_cmds(PyObject*);
PyObject* parse_file(PyObject*, PyObject*);
PyObject* parse_string(PyObject*, PyObject*);

/* To shim go's missing variadic function support */
int PyDockerfile_PyArg_ParseTuple_U(PyObject* args, PyObject** s) {
    return PyArg_ParseTuple(args, "U", s);
}

/* go cannot access C macros */
PyObject* PyDockerfile_Py_RETURN_NONE() {
    Py_RETURN_NONE;
}

/* exception types */
PyObject* PyDockerfile_GoIOError;
PyObject* PyDockerfile_GoParseError;

/* Command namedtuple */
PyObject* PyDockerfile_Command;

PyObject* PyDockerfile_NewCommand(
    PyObject* cmd,
    PyObject* sub_cmd,
    PyObject* json,
    PyObject* original,
    PyObject* start_line,
    PyObject* end_line,
    PyObject* flags,
    PyObject* value
) {
    return PyObject_CallFunction(
        PyDockerfile_Command, "OOOOOOOO",
        cmd, sub_cmd, json, original, start_line, end_line, flags, value
    );
}

static struct PyMethodDef methods[] = {
    {"all_cmds", (PyCFunction)all_cmds, METH_NOARGS},
    {"parse_file", (PyCFunction)parse_file, METH_VARARGS},
    {"parse_string", (PyCFunction)parse_string, METH_VARARGS},
    {NULL, NULL}
};

static PyObject* _setup_module(PyObject* module) {
    if (module) {
        PyDockerfile_GoIOError = PyErr_NewException("dockerfile.GoIOError", PyExc_OSError, NULL);
        PyModule_AddObject(module, "GoIOError", PyDockerfile_GoIOError);
        PyDockerfile_GoParseError = PyErr_NewException("dockerfile.GoParseError", PyExc_ValueError, NULL);
        PyModule_AddObject(module, "GoParseError", PyDockerfile_GoParseError);

        PyObject* collections = PyImport_ImportModule("collections");
        PyDockerfile_Command = PyObject_CallMethod(
            collections, "namedtuple", "ss",
            "Command", "cmd sub_cmd json original start_line end_line flags value"
        );
        PyObject_SetAttrString(
            PyDockerfile_Command, "__module__",
            PyObject_GetAttrString(module, "__name__")
        );
        PyModule_AddObject(module, "Command", PyDockerfile_Command);
        Py_XDECREF(collections);
    }
    return module;
}

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "dockerfile",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_dockerfile(void) {
    return _setup_module(PyModule_Create(&module));
}
