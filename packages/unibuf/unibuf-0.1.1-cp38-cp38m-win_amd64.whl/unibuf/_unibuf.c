#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD

    PyObject *string;

    const char *string_encoding;
    int         string_kind;
    Py_ssize_t  string_length;
    size_t      string_itemsize;
} PyUnicodeBuffer;


#define UCS1_ENCODING_NAME "ISO-8859-1"

#if WORDS_BIGENDIAN
#define UCS2_ENCODING_NAME "UTF-16BE"
#define UCS4_ENCODING_NAME "UTF-32BE"
#else
#define UCS2_ENCODING_NAME "UTF-16LE"
#define UCS4_ENCODING_NAME "UTF-32LE"
#endif


static const char *encoding_name_from_itemsize(size_t itemsize) {
    switch (itemsize) {
        case 1:
            return UCS1_ENCODING_NAME;
        case 2:
            return UCS2_ENCODING_NAME;
        case 4:
            return UCS4_ENCODING_NAME;
        default:
            return "UNKNOWN";
    }
}


static PyObject *PyUnicodeBuffer_new(
    PyTypeObject *type,
    PyObject *args,
    PyObject *kwargs
) {
    static char *keywords[] = {"string", NULL};

    PyUnicodeBuffer *self;
    self = (PyUnicodeBuffer *) type->tp_alloc(type, 0);
    if (self != NULL) {
        PyObject *string = NULL;
        if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &string)) {
            Py_DECREF(self);
            return NULL;
        }
        if (!PyUnicode_Check(string)) {
            PyErr_Format(
                PyExc_TypeError,
                "UnicodeBuffer() argument must be a string, not '%.200s'",
                Py_TYPE(string)->tp_name
            );
            Py_DECREF(self);
            return NULL;
        }
        if (PyUnicode_READY(string)) {
            Py_DECREF(self);
            return NULL;
        }

        self->string = string;
        self->string_kind = PyUnicode_KIND(string);
        self->string_length = PyUnicode_GET_LENGTH(string);
        switch (PyUnicode_KIND(self->string)) {
            case PyUnicode_WCHAR_KIND:
                self->string_itemsize = sizeof(wchar_t);
                break;
            case PyUnicode_1BYTE_KIND:
                self->string_itemsize = 1;
                break;
            case PyUnicode_2BYTE_KIND:
                self->string_itemsize = 2;
                break;
            case PyUnicode_4BYTE_KIND:
                self->string_itemsize = 4;
                break;
            default:
                PyErr_Format(
                    PyExc_ValueError,
                    "invalid PyUnicode_KIND %i",
                    PyUnicode_KIND(self->string)
                );
                Py_DECREF(self);
                return NULL;
        }
        self->string_encoding = encoding_name_from_itemsize(self->string_itemsize);

        Py_INCREF(string);
    }
    return (PyObject *) self;
};

static void PyUnicodeBuffer_dealloc(PyUnicodeBuffer *self) {
    Py_XDECREF(self->string);
    Py_TYPE(self)->tp_free((PyObject *) self);
};

static PyObject *PyUnicodeBuffer_str(PyUnicodeBuffer *self) {
    return PyUnicode_FromFormat(
        "<UnicodeBuffer %R encoding='%s'>",
        self->string,
        self->string_encoding
    );
}


static int PyUnicodeBuffer_getbuffer(PyUnicodeBuffer *self, Py_buffer *view, int flags) {
    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }

    view->obj = (PyObject*) self;
    view->buf = PyUnicode_DATA(self->string);
    view->len = self->string_length * self->string_itemsize;
    view->readonly = 1;
    view->itemsize = self->string_itemsize;
    view->format = "i";
    view->ndim = 1;
    view->shape =  &self->string_length;
    view->strides = &self->string_itemsize;
    view->suboffsets = NULL;
    view->internal = NULL;

    Py_INCREF(self);
    return 0;
}

static PyBufferProcs PyUnicodeBuffer_as_buffer = {
    (getbufferproc) PyUnicodeBuffer_getbuffer,
    (releasebufferproc) NULL,
};


static PyMemberDef PyUnicodeBuffer_members[] = {
    {"encoding", T_STRING, offsetof(PyUnicodeBuffer, string_encoding), 0, "the underlying encoding"},
     {NULL}
};

static PyTypeObject py_unicode_buffer_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "unibuf.UnicodeBuffer",
    .tp_doc = "Buffer protocol for unicode objects.",
    .tp_basicsize = sizeof(PyUnicodeBuffer),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyUnicodeBuffer_new,
    .tp_dealloc = (destructor) PyUnicodeBuffer_dealloc,
    .tp_repr = (reprfunc) PyUnicodeBuffer_str,
    .tp_str = (reprfunc) PyUnicodeBuffer_str,
    .tp_as_buffer = &PyUnicodeBuffer_as_buffer,
    .tp_members = PyUnicodeBuffer_members
};

static PyModuleDef py_unibuf_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_unibuf",
    .m_doc = "A buffer protocol for unicode objects.",
    .m_size = -1,
};


PyMODINIT_FUNC PyInit__unibuf(void) {
    PyObject *module;

    if (PyType_Ready(&py_unicode_buffer_type) < 0) {
        return NULL;
    }

    module = PyModule_Create(&py_unibuf_module);
    if (module == NULL) {
        return NULL;
    }

    Py_INCREF(&py_unicode_buffer_type);
    if (PyModule_AddObject(module, "UnicodeBuffer", (PyObject *) &py_unicode_buffer_type) < 0) {
        Py_DECREF(&py_unicode_buffer_type);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
