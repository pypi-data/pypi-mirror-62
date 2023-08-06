/**
Copyright (c) 2016-2019 cloudover.io ltd.

Licensee holding a valid commercial license for dinemic library may use it with
accordance to terms of the license agreement between cloudover.io ltd. and the
licensee, or on GNU Affero GPL v3 license terms.

Licensee not holding a valid commercial license for dinemic library may use it
under GNU Affero GPL v3 license.

Terms of GNU Affero GPL v3 license are available on following site:
https://www.gnu.org/licenses/agpl-3.0.en.html
*/

#include "pydmodel.h"

using namespace boost::python;
using namespace std;

PyDModel::PyDModel(PyObject *self_ptr, string db_id)
    : obj(db_id, py_store, py_sync),
      caller(NULL),
      self(self_ptr)
{
    if (py_sync == NULL || py_store == NULL) {
        throw Dinemic::DException("Dinemic is not initialized. Call pydinemic.launch or pydinemic.prepare first");
    }

    map_fields();
}

PyDModel::PyDModel(PyObject *self_ptr, string db_id, string caller_id)
    : obj(db_id, py_store, py_sync),
      caller(NULL),
      self(self_ptr)
{
    if (py_sync == NULL || py_store == NULL) {
        throw Dinemic::DException("Dinemic is not initialized. Call pydinemic.launch or pydinemic.prepare first");
    }
    if (caller_id != "") {
        caller = new Dinemic::DModel(caller_id, py_store, py_sync);
        obj.set_caller(caller);
        INFO("Caller set to " + caller->get_db_id());
    }

    map_fields();
}

PyDModel::PyDModel(PyObject *self_ptr, boost::python::list authorized_objects)
    : obj(self_ptr->ob_type->tp_name, py_store, py_sync, std::vector<string>(boost::python::stl_input_iterator<string>(authorized_objects), boost::python::stl_input_iterator<string>() )),
      caller(NULL),
      self(self_ptr)
{
    if (py_sync == NULL || py_store == NULL) {
        throw Dinemic::DException("Dinemic is not initialized. Call pydinemic.launch or pydinemic.prepare first");
    }

    map_fields();
}

PyDModel::PyDModel(PyObject *self_ptr, const PyDModel &o)
    : obj(o.obj),
      caller(NULL),
      self(self_ptr)
{
    if (o.caller != NULL) {
        caller = new Dinemic::DModel(o.caller->get_db_id(), py_store, py_sync);
        obj.set_caller(caller);
    }
    map_fields();
}

PyDModel::~PyDModel() {
    if (!caller) {
        obj.set_caller(NULL);
        delete caller;
    }
}

string PyDModel::get_id() {
    return obj.get_id();
}

string PyDModel::get_db_id() {
    return obj.get_db_id();
}

string PyDModel::get_model() {
    return obj.get_model();
}

void PyDModel::set(string key, string value) {
    obj.set(key, value);
}

string PyDModel::get(string key, string default_value) {
    return obj.get(key, default_value);
}

void PyDModel::del(string key) {
    obj.del(key);
}

void PyDModel::remove() {
    obj.remove();
}

string PyDModel::encrypt(const string &value) {
    return obj.encrypt(value);
}

string PyDModel::decrypt(const string &value) {
    return obj.decrypt(value);
}

bool PyDModel::is_read_authorized(const string &object_id) {
    return obj.is_read_authorized(object_id);
}

void PyDModel::append_read_authorized(const string &object_id) {
    obj.append_read_authorized(object_id);
}

void PyDModel::revoke_read_authorized(const string &object_id) {
    obj.revoke_read_authorized(object_id);
}

bool PyDModel::is_update_authorized(const string &object_id) {
    return obj.is_update_authorized(object_id);
}

void PyDModel::append_update_authorized(const string &object_id) {
    obj.append_update_authorized(object_id);
}

void PyDModel::revoke_update_authorized(const string &object_id) {
    obj.revoke_update_authorized(object_id);
}

void PyDModel::map_fields() {
    PyObject *attrs = PyObject_Dir(self);
    if (!attrs) {
        cerr << "Attrs not present" << endl;
        return;
    }
    for (int i = 0; i < PyList_Size(attrs); i++) {
        PyObject *attr = PyList_GetItem(attrs, i);
        if (!attr)
            continue;

        PyObject *field = PyObject_GetAttr(self, attr);
        if (!field)
            continue;

        PyObject *obj_id = PyUnicode_FromString(obj.get_db_id().c_str());

        PyObject *clr_id;
        if (caller != NULL)
            clr_id = PyUnicode_FromString(caller->get_db_id().c_str());
        else
            clr_id = PyUnicode_FromString("");

        if (string(field->ob_type->tp_name) == "DField") {
            PyObject_SetAttrString(field, "_caller_id", clr_id);
            PyObject_SetAttrString(field, "_object_id", obj_id);
        } else if (string(field->ob_type->tp_name) == "DList") {
            PyObject_SetAttrString(field, "_caller_id", clr_id);
            PyObject_SetAttrString(field, "_object_id", obj_id);
        } else if (string(field->ob_type->tp_name) == "DDict") {
            PyObject_SetAttrString(field, "_caller_id", clr_id);
            PyObject_SetAttrString(field, "_object_id", obj_id);
        }
        Py_XDECREF(clr_id);
        Py_XDECREF(obj_id);

        Py_XDECREF(field);
        Py_XDECREF(attr);
    }
}
