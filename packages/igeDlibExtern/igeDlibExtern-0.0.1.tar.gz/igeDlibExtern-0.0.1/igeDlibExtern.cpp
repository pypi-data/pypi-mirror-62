#include "igeDlibExtern.h"
#include "igeDlibExtern_doc_en.h"

PyObject* dlibExtern_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	dlibExtern_obj* self = NULL;

	self = (dlibExtern_obj*)type->tp_alloc(type, 0);
	self->dlibExtern = new DlibExtern();

	return (PyObject*)self;
}

void dlibExtern_dealloc(dlibExtern_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* dlibExtern_str(dlibExtern_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "Dlib Extern object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* dlib_detect(dlibExtern_obj* self, PyObject* args)
{
	PyObject* image = nullptr;
	int minWidth = 80, minHeight = 80;
	if (!PyArg_ParseTuple(args, "O|ii", &image, &minWidth, &minHeight)) return NULL;

	dlib::rectangle rect = self->dlibExtern->detect(image, minWidth, minHeight);
	PyObject* _res =
		Py_BuildValue(
			"{s:i,s:i,s:i,s:i}",
			"left", (int)rect.left(),
			"top", (int)rect.top(),
			"right", (int)rect.right(),
			"bottom", (int)rect.bottom());
	return _res;
}

PyMethodDef dlibExtern_methods[] = {
	{ "detect", (PyCFunction)dlib_detect, METH_VARARGS, dlib_detect_doc },
	{ NULL,	NULL }
};

PyGetSetDef dlibExtern_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject DlibExternType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeDlibExtern",							/* tp_name */
	sizeof(dlibExtern_obj),						/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)dlibExtern_dealloc,				/* tp_dealloc */
	0,											/* tp_print */
	0,											/* tp_getattr */
	0,											/* tp_setattr */
	0,											/* tp_reserved */
	0,											/* tp_repr */
	0,											/* tp_as_number */
	0,											/* tp_as_sequence */
	0,											/* tp_as_mapping */
	0,											/* tp_hash */
	0,											/* tp_call */
	(reprfunc)dlibExtern_str,					/* tp_str */
	0,											/* tp_getattro */
	0,											/* tp_setattro */
	0,											/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,							/* tp_flags */
	0,											/* tp_doc */
	0,											/* tp_traverse */
	0,											/* tp_clear */
	0,											/* tp_richcompare */
	0,											/* tp_weaklistoffset */
	0,											/* tp_iter */
	0,											/* tp_iternext */
	dlibExtern_methods,							/* tp_methods */
	0,											/* tp_members */
	dlibExtern_getsets,							/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	dlibExtern_new,									/* tp_new */
	0,											/* tp_free */
};

static PyModuleDef dlibExtern_module = {
	PyModuleDef_HEAD_INIT,
	"igeDlibExtern",							// Module name to use with Python import statements
	"Dlib Extern Module.",						// Module description
	0,
	dlibExtern_methods							// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeDlibExtern() {
	PyObject* module = PyModule_Create(&dlibExtern_module);

	if (PyType_Ready(&DlibExternType) < 0) return NULL;

	Py_INCREF(&DlibExternType);
	PyModule_AddObject(module, "dlibExtern", (PyObject*)&DlibExternType);

	return module;
}