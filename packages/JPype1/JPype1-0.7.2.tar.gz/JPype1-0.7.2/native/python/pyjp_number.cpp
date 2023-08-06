/*
 * Copyright 2020 nelson85.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "jpype.h"
#include "pyjp.h"
#include "jp_boxedclasses.h"

static bool isNull(PyObject *self)
{
	JPValue *javaSlot = PyJPValue_getJavaSlot(self);
	if (javaSlot != NULL
			&& !javaSlot->getClass()->isPrimitive()
			&& javaSlot->getValue().l == 0)
		return true;
	return false;
}

#ifdef __cplusplus
extern "C"
{
#endif

static PyObject *PyJPNumber_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
	JP_PY_TRY("PyJPNumberLong_new", type);
	ASSERT_JVM_RUNNING();
	JPJavaFrame frame;
	JPClass *cls = (JPClass*) PyJPClass_getJPClass((PyObject*) type);
	if (cls == NULL)
		JP_RAISE(PyExc_TypeError, "Class type incorrect");
	PyObject *self;
	if (PyObject_IsSubclass((PyObject*) type, (PyObject*) & PyLong_Type))
	{
		self = PyLong_Type.tp_new(type, args, kwargs);
	} else if (PyObject_IsSubclass((PyObject*) type, (PyObject*) & PyFloat_Type))
	{
		self = PyFloat_Type.tp_new(type, args, kwargs);
	} else
	{
		PyErr_Format(PyExc_TypeError, "Type '%s' is not a number class", type->tp_name);
		return NULL;
	}
	if (!self)
		JP_RAISE_PYTHON("type new failed");
	jvalue val = cls->convertToJava(self);
	PyJPValue_assignJavaSlot(self, JPValue(cls, val));
	JP_TRACE("new", self);
	return self;
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberLong_int(PyObject *self)
{
	JP_PY_TRY("PyJPNumberLong_int");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		JP_RAISE(PyExc_TypeError, "cast of null pointer would return non-int")
		return PyLong_Type.tp_as_number->nb_int(self);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberLong_float(PyObject *self)
{
	JP_PY_TRY("PyJPNumberLong_float");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		JP_RAISE(PyExc_TypeError, "cast of null pointer would return non-float")
		return PyLong_Type.tp_as_number->nb_float(self);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberFloat_int(PyObject *self)
{
	JP_PY_TRY("PyJPNumberFloat_int");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		JP_RAISE(PyExc_TypeError, "cast of null pointer would return non-int")
		return PyFloat_Type.tp_as_number->nb_int(self);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberFloat_float(PyObject *self)
{
	JP_PY_TRY("PyJPNumberFloat_float");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		JP_RAISE(PyExc_TypeError, "cast of null pointer would return non-float")
		return PyFloat_Type.tp_as_number->nb_float(self);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberLong_str(PyObject *self)
{
	JP_PY_TRY("PyJPNumberLong_str");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		return Py_TYPE(Py_None)->tp_str(Py_None);
	return PyLong_Type.tp_str(self);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberFloat_str(PyObject *self)
{
	JP_PY_TRY("PyJPNumberFloat_float");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		return Py_TYPE(Py_None)->tp_str(Py_None);
	return PyFloat_Type.tp_str(self);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberLong_repr(PyObject *self)
{
	JP_PY_TRY("PyJPNumberLong_repr");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		return Py_TYPE(Py_None)->tp_str(Py_None);
	return PyLong_Type.tp_repr(self);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberFloat_repr(PyObject *self)
{
	JP_PY_TRY("PyJPNumberFloat_float");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
		return Py_TYPE(Py_None)->tp_str(Py_None);
	return PyFloat_Type.tp_repr(self);
	JP_PY_CATCH(NULL);
}

static const char* op_names[] = {
	"<", "<=", "==", "!=", ">", ">="
};

static PyObject *PyJPNumberLong_compare(PyObject *self, PyObject *other, int op)
{
	JP_PY_TRY("PyJPNumberLong_oompare");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
	{
		if (op == Py_EQ)
			return PyBool_FromLong(other == Py_None);
		if (op == Py_NE)
			return PyBool_FromLong(other != Py_None);
		PyErr_Format(PyExc_TypeError, "'%s' not supported with null pointer", op_names[op]);
		JP_RAISE_PYTHON("fail");
	}
	return PyLong_Type.tp_richcompare(self, other, op);
	JP_PY_CATCH(NULL);
}

static PyObject *PyJPNumberFloat_compare(PyObject *self, PyObject *other, int op)
{
	JP_PY_TRY("PyJPNumberLong_oompare");
	ASSERT_JVM_RUNNING();
	if (isNull(self))
	{
		if (op == Py_EQ)
			return PyBool_FromLong(other == Py_None);
		if (op == Py_NE)
			return PyBool_FromLong(other != Py_None);
		PyErr_Format(PyExc_TypeError, "'%s' not supported with null pointer", op_names[op]);
		JP_RAISE_PYTHON("fail");
	}
	return PyFloat_Type.tp_richcompare(self, other, op);
	JP_PY_CATCH(NULL);
}

static Py_hash_t PyJPNumberLong_hash(PyObject *self)
{
	JP_PY_TRY("PyJPNumberLong_hash");
	ASSERT_JVM_RUNNING();
	JPValue *javaSlot = PyJPValue_getJavaSlot(self);
	if (javaSlot == NULL || javaSlot->getClass() == NULL)
		return Py_TYPE(Py_None)->tp_hash(Py_None);
	jobject o = javaSlot->getJavaObject();
	if (o == NULL)
		return Py_TYPE(Py_None)->tp_hash(Py_None);
	return PyLong_Type.tp_hash(self);
	JP_PY_CATCH(0);
}

static Py_hash_t PyJPNumberFloat_hash(PyObject *self)
{
	JP_PY_TRY("PyJPNumberFloat_hash");
	ASSERT_JVM_RUNNING();
	JPValue *javaSlot = PyJPValue_getJavaSlot(self);
	if (javaSlot == NULL || javaSlot->getClass() == NULL)
		return Py_TYPE(Py_None)->tp_hash(Py_None);
	jobject o = javaSlot->getJavaObject();
	if (o == NULL)
		return Py_TYPE(Py_None)->tp_hash(Py_None);
	return PyFloat_Type.tp_hash(self);
	JP_PY_CATCH(0);
}

static PyObject *PyJPChar_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
	JP_PY_TRY("PyJPValueChar_new", type);
	ASSERT_JVM_RUNNING();
	JPJavaFrame frame;
	PyObject *self;
	if (PyTuple_Size(args) == 1 && JPPyString::checkCharUTF16(PyTuple_GetItem(args, 0)))
	{
		jchar i = JPPyString::asCharUTF16(PyTuple_GetItem(args, 0));
		PyObject *args2 = PyTuple_Pack(1, PyLong_FromLong(i));
		self = PyLong_Type.tp_new(type, args2, kwargs);
		Py_DECREF(args2);
	} else
	{
		self = PyLong_Type.tp_new(type, args, kwargs);
	}
	if (!self)
		JP_RAISE_PYTHON("type new failed");
	JPClass *cls = PyJPClass_getJPClass((PyObject*) type);
	if (cls == NULL)
		JP_RAISE(PyExc_TypeError, "Class type incorrect");
	jvalue val = cls->convertToJava(self);
	PyJPValue_assignJavaSlot(self, JPValue(cls, val));
	JP_TRACE("new", self);
	return self;
	JP_PY_CATCH(NULL);
}

static PyObject* PyJPChar_str(PyObject* self)
{
	JP_PY_TRY("PyJPChar_str", self);
	if (isNull(self))
		return Py_TYPE(Py_None)->tp_str(Py_None);
	JPValue *value = PyJPValue_getJavaSlot(self);
	if (value == NULL)
		JP_RAISE(PyExc_RuntimeError, "Java slot missing");
	return JPPyString::fromCharUTF16(value->getValue().c).keep();
	JP_PY_CATCH(NULL);
}

static PyObject* PyJPBoolean_str(PyObject* self)
{
	JP_PY_TRY("PyJPBoolean_str", self);
	if (isNull(self))
		return Py_TYPE(Py_None)->tp_str(Py_None);
	if (PyLong_AsLong(self) == 0)
		return Py_TYPE(Py_False)->tp_str(Py_False);
	return Py_TYPE(Py_True)->tp_str(Py_True);
	JP_PY_CATCH(NULL);
}

static PyType_Slot numberLongSlots[] = {
	{Py_tp_new,      (void*) &PyJPNumber_new},
	{Py_tp_getattro, (void*) &PyJPValue_getattro},
	{Py_tp_setattro, (void*) &PyJPValue_setattro},
	{Py_nb_int,      (void*) &PyJPNumberLong_int},
	{Py_nb_float,    (void*) &PyJPNumberLong_float},
	{Py_tp_str,      (void*) &PyJPNumberLong_str},
	{Py_tp_repr,     (void*) &PyJPNumberLong_repr},
	{Py_tp_hash,     (void*) &PyJPNumberLong_hash},
	{Py_tp_richcompare, (void*) &PyJPNumberLong_compare},
	{0}
};

PyTypeObject *PyJPNumberLong_Type = NULL;
PyType_Spec numberLongSpec = {
	"_jpype._JNumberLong",
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	numberLongSlots
};

static PyType_Slot numberFloatSlots[] = {
	{Py_tp_new,      (void*) &PyJPNumber_new},
	{Py_tp_getattro, (void*) &PyJPValue_getattro},
	{Py_tp_setattro, (void*) &PyJPValue_setattro},
	{Py_nb_int,      (void*) &PyJPNumberFloat_int},
	{Py_nb_float,    (void*) &PyJPNumberFloat_float},
	{Py_tp_str,      (void*) &PyJPNumberFloat_str},
	{Py_tp_repr,     (void*) &PyJPNumberFloat_repr},
	{Py_tp_hash,     (void*) &PyJPNumberFloat_hash},
	{Py_tp_richcompare, (void*) &PyJPNumberFloat_compare},
	{0}
};

PyTypeObject *PyJPNumberFloat_Type = NULL;
PyType_Spec numberFloatSpec = {
	"_jpype._JNumberFloat",
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	numberFloatSlots
};

static PyType_Slot numberCharSlots[] = {
	{Py_tp_new,      (void*) PyJPChar_new},
	{Py_tp_getattro, (void*) &PyJPValue_getattro},
	{Py_tp_setattro, (void*) &PyJPValue_setattro},
	{Py_tp_str,      (void*) &PyJPChar_str},
	{Py_tp_repr,     (void*) &PyJPChar_str},
	{Py_nb_int,      (void*) &PyJPNumberLong_int},
	{Py_nb_float,    (void*) &PyJPNumberLong_float},
	{Py_tp_hash,     (void*) &PyJPNumberLong_hash},
	{Py_tp_richcompare, (void*) &PyJPNumberLong_compare},
	{0}
};

PyTypeObject *PyJPNumberChar_Type = NULL;
PyType_Spec numberCharSpec = {
	"_jpype._JChar",
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	numberCharSlots
};

static PyType_Slot numberBooleanSlots[] = {
	{Py_tp_new,      (void*) PyJPChar_new},
	{Py_tp_getattro, (void*) &PyJPValue_getattro},
	{Py_tp_setattro, (void*) &PyJPValue_setattro},
	{Py_tp_str,      (void*) &PyJPBoolean_str},
	{Py_tp_repr,     (void*) &PyJPBoolean_str},
	{Py_nb_int,      (void*) &PyJPNumberLong_int},
	{Py_nb_float,    (void*) &PyJPNumberLong_float},
	{Py_tp_hash,     (void*) &PyJPNumberLong_hash},
	{Py_tp_richcompare, (void*) &PyJPNumberLong_compare},
	{0}
};

PyTypeObject *PyJPNumberBool_Type = NULL;
PyType_Spec numberBooleanSpec = {
	"_jpype._JBoolean",
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	numberBooleanSlots
};

#ifdef __cplusplus
}
#endif

void PyJPNumber_initType(PyObject* module)
{
	PyObject *bases;

	bases = PyTuple_Pack(2, &PyLong_Type, PyJPObject_Type);
	PyJPNumberLong_Type = (PyTypeObject*) PyJPClass_FromSpecWithBases(&numberLongSpec, bases);
	Py_DECREF(bases);
	JP_PY_CHECK();
	PyModule_AddObject(module, "_JNumberLong", (PyObject*) PyJPNumberLong_Type);
	JP_PY_CHECK();

	bases = PyTuple_Pack(2, &PyFloat_Type, PyJPObject_Type);
	PyJPNumberFloat_Type = (PyTypeObject*) PyJPClass_FromSpecWithBases(&numberFloatSpec, bases);
	Py_DECREF(bases);
	JP_PY_CHECK();
	PyModule_AddObject(module, "_JNumberFloat", (PyObject*) PyJPNumberFloat_Type);
	JP_PY_CHECK();

	bases = PyTuple_Pack(1, &PyLong_Type, PyJPObject_Type);
	PyJPNumberChar_Type = (PyTypeObject*) PyJPClass_FromSpecWithBases(&numberCharSpec, bases);
	Py_DECREF(bases);
	JP_PY_CHECK();
	PyModule_AddObject(module, "_JChar", (PyObject*) PyJPNumberChar_Type);
	JP_PY_CHECK();

	bases = PyTuple_Pack(1, &PyLong_Type, PyJPObject_Type);
	PyJPNumberBool_Type = (PyTypeObject*) PyJPClass_FromSpecWithBases(&numberBooleanSpec, bases);
	Py_DECREF(bases);
	JP_PY_CHECK();
	PyModule_AddObject(module, "_JBoolean", (PyObject*) PyJPNumberBool_Type);
	JP_PY_CHECK();

}

JPPyObject PyJPNumber_create(JPPyObject& wrapper, const JPValue& value)
{
	// Bools are not numbers in Java
	if (value.getClass() == JPTypeManager::_java_lang_Boolean)
	{
		jlong l = 0;
		if (value.getValue().l != 0)
			l = JPJni::booleanValue(value.getJavaObject());
		PyObject *args = PyTuple_Pack(1, PyLong_FromLongLong(l));
		return JPPyObject(JPPyRef::_call,
				PyLong_Type.tp_new((PyTypeObject*) wrapper.get(), args, NULL));
	}
	if (value.getClass() == JPTypeManager::_java_lang_Character)
	{
		jlong l = 0;
		if (value.getValue().l != 0)
			l = JPJni::charValue(value.getJavaObject());
		PyObject *args = PyTuple_Pack(1, PyLong_FromLongLong(l));
		return JPPyObject(JPPyRef::_call,
				PyLong_Type.tp_new((PyTypeObject*) wrapper.get(), args, NULL));
	}
	if (PyObject_IsSubclass(wrapper.get(), (PyObject*) & PyLong_Type))
	{
		jlong l = 0;
		if (value.getValue().l != 0)
			l = JPJni::longValue(value.getJavaObject());
		PyObject *args = PyTuple_Pack(1, PyLong_FromLongLong(l));
		return JPPyObject(JPPyRef::_call,
				PyLong_Type.tp_new((PyTypeObject*) wrapper.get(), args, NULL));
	}
	if (PyObject_IsSubclass(wrapper.get(), (PyObject*) & PyFloat_Type))
	{
		jdouble l = 0;
		if (value.getValue().l != 0)
			l = JPJni::doubleValue(value.getJavaObject());
		PyObject *args = PyTuple_Pack(1, PyFloat_FromDouble(l));
		return JPPyObject(JPPyRef::_call,
				PyFloat_Type.tp_new((PyTypeObject*) wrapper.get(), args, NULL));
	}
	JP_RAISE(PyExc_TypeError, "unable to convert");
}
