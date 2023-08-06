/*****************************************************************************
   Copyright 2004-2008 Steve Ménard

   Licensed under the Apache License, Version 2.0 (the "License
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

	   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

 *****************************************************************************/
#include "jpype.h"
#include "jp_jniutil.h"
#include "jp_encoding.h"


namespace
{ // impl detail
jmethodID s_Object_GetClassID;
jmethodID s_Object_ToStringID;
jmethodID s_Object_HashCodeID;
jmethodID s_Object_EqualsID;

jmethodID s_Class_GetNameID;
jmethodID s_Class_GetComponentTypeID;
jmethodID s_Class_GetDeclaredFieldsID;
jmethodID s_Class_GetInterfacesID;
jmethodID s_Class_GetMethodsID;
jmethodID s_Class_GetDeclaredConstructorsID;
jmethodID s_Class_IsArrayID;
jmethodID s_Class_IsInterfaceID;
jmethodID s_Class_GetModifiersID;
jmethodID s_Class_GetCanonicalNameID;

jclass s_ModifierClass;
jmethodID s_Modifier_IsStaticID;
jmethodID s_Modifier_IsPublicID;
jmethodID s_Modifier_IsAbstractID;
jmethodID s_Modifier_IsFinalID;

jclass s_ClassLoaderClass;
jmethodID s_ClassLoader_GetSystemClassLoaderID;

jmethodID s_Member_GetModifiersID;
jmethodID s_Member_GetMemberNameID;

jmethodID s_Field_GetTypeID;
jmethodID s_Field_GetModifiersID;

jmethodID s_Method_GetReturnTypeID;
jmethodID s_Method_IsSyntheticMethodID;
jmethodID s_Method_IsVarArgsMethodID;
jmethodID s_Method_GetParameterTypesID;

jclass s_ConstructorClass;
jmethodID s_Constructor_GetParameterTypesID;

jclass s_ThrowableClass;
jmethodID s_Throwable_GetMessageID;
jmethodID s_Throwable_PrintStackTraceID;

jclass s_StringWriterClass;
jclass s_PrintWriterClass;
jmethodID s_StringWriterID;
jmethodID s_PrintWriterID;
jmethodID s_FlushID;
jmethodID s_Number_IntValueID;
jmethodID s_Number_LongValueID;
jmethodID s_Number_DoubleValueID;
jmethodID s_BooleanValueID;
jmethodID s_CharValueID;

jmethodID s_String_ToCharArrayID;
}

jfloat JPJni::s_Float_Min = 0 ;
jfloat JPJni::s_Float_Max = 0;
jclass JPJni::s_NoSuchMethodErrorClass;
jclass JPJni::s_RuntimeExceptionClass;
jclass JPJni::s_ProxyClass;
jclass JPJni::s_ClassClass;
jmethodID JPJni::s_NewProxyInstanceID;

void JPJni::init()
{
	JP_TRACE_IN("JPJni::init");
	JPJavaFrame frame(200);
	jclass cls;
	cls = (jclass) frame.FindClass("java/lang/Object");
	s_Object_GetClassID = frame.GetMethodID(cls, "getClass", "()Ljava/lang/Class;");
	s_Object_ToStringID = frame.GetMethodID(cls, "toString", "()Ljava/lang/String;");
	s_Object_HashCodeID = frame.GetMethodID(cls, "hashCode", "()I");
	s_Object_EqualsID = frame.GetMethodID(cls, "equals", "(Ljava/lang/Object;)Z");

	cls = (jclass) frame.FindClass("java/lang/String");
	s_String_ToCharArrayID = frame.GetMethodID(cls, "toCharArray", "()[C");

	s_ClassClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/Class"));
	s_Class_GetNameID = frame.GetMethodID(s_ClassClass, "getName", "()Ljava/lang/String;");

	s_Class_GetComponentTypeID = frame.GetMethodID(s_ClassClass, "getComponentType", "()Ljava/lang/Class;");
	s_Class_GetDeclaredFieldsID = frame.GetMethodID(s_ClassClass, "getDeclaredFields", "()[Ljava/lang/reflect/Field;");
	s_Class_GetMethodsID = frame.GetMethodID(s_ClassClass, "getMethods", "()[Ljava/lang/reflect/Method;");
	s_Class_GetDeclaredConstructorsID = frame.GetMethodID(s_ClassClass, "getDeclaredConstructors", "()[Ljava/lang/reflect/Constructor;");
	s_Class_IsArrayID = frame.GetMethodID(s_ClassClass, "isArray", "()Z");
	s_Class_IsInterfaceID = frame.GetMethodID(s_ClassClass, "isInterface", "()Z");
	s_Class_GetModifiersID = frame.GetMethodID(s_ClassClass, "getModifiers", "()I");
	s_Class_GetInterfacesID = frame.GetMethodID(s_ClassClass, "getInterfaces", "()[Ljava/lang/Class;");
	s_Class_GetCanonicalNameID = frame.GetMethodID(s_ClassClass, "getCanonicalName", "()Ljava/lang/String;");

	s_ModifierClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/reflect/Modifier"));
	s_Modifier_IsStaticID = frame.GetStaticMethodID(s_ModifierClass, "isStatic", "(I)Z");
	s_Modifier_IsPublicID = frame.GetStaticMethodID(s_ModifierClass, "isPublic", "(I)Z");
	s_Modifier_IsAbstractID = frame.GetStaticMethodID(s_ModifierClass, "isAbstract", "(I)Z");
	s_Modifier_IsFinalID = frame.GetStaticMethodID(s_ModifierClass, "isFinal", "(I)Z");

	s_ClassLoaderClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/ClassLoader"));
	s_ClassLoader_GetSystemClassLoaderID = frame.GetStaticMethodID(s_ClassLoaderClass, "getSystemClassLoader", "()Ljava/lang/ClassLoader;");

	s_NoSuchMethodErrorClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/NoSuchMethodError"));
	s_RuntimeExceptionClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/RuntimeException"));

	s_ProxyClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/reflect/Proxy"));
	s_NewProxyInstanceID = frame.GetStaticMethodID(s_ProxyClass, "newProxyInstance", "(Ljava/lang/ClassLoader;[Ljava/lang/Class;Ljava/lang/reflect/InvocationHandler;)Ljava/lang/Object;");

	cls = (jclass) frame.FindClass("java/lang/reflect/Member");
	s_Member_GetModifiersID = frame.GetMethodID(cls, "getModifiers", "()I");
	s_Member_GetMemberNameID = frame.GetMethodID(cls, "getName", "()Ljava/lang/String;");

	cls = (jclass) frame.FindClass("java/lang/reflect/Field");
	s_Field_GetTypeID = frame.GetMethodID(cls, "getType", "()Ljava/lang/Class;");
	s_Field_GetModifiersID = frame.GetMethodID(cls, "getModifiers", "()I");

	cls = (jclass) frame.FindClass("java/lang/reflect/Method");
	s_Method_GetReturnTypeID = frame.GetMethodID(cls, "getReturnType", "()Ljava/lang/Class;");
	s_Method_GetParameterTypesID = frame.GetMethodID(cls, "getParameterTypes", "()[Ljava/lang/Class;");
	s_Method_IsSyntheticMethodID = frame.GetMethodID(cls, "isSynthetic", "()Z");
	s_Method_IsVarArgsMethodID = frame.GetMethodID(cls, "isVarArgs", "()Z");

	s_ConstructorClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/reflect/Constructor"));
	s_Constructor_GetParameterTypesID = frame.GetMethodID(s_ConstructorClass, "getParameterTypes", "()[Ljava/lang/Class;");
	s_ThrowableClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/lang/Throwable"));
	s_Throwable_GetMessageID = frame.GetMethodID(s_ThrowableClass, "getMessage", "()Ljava/lang/String;");
	s_Throwable_PrintStackTraceID = frame.GetMethodID(s_ThrowableClass, "printStackTrace", "(Ljava/io/PrintWriter;)V");

	s_StringWriterClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/io/StringWriter"));
	s_PrintWriterClass = (jclass) frame.NewGlobalRef(frame.FindClass("java/io/PrintWriter"));
	s_StringWriterID = frame.GetMethodID(s_StringWriterClass, "<init>", "()V");
	s_PrintWriterID = frame.GetMethodID(s_PrintWriterClass, "<init>", "(Ljava/io/Writer;)V");
	s_FlushID = frame.GetMethodID(s_PrintWriterClass, "flush", "()V");

	cls = (jclass) frame.FindClass("java/lang/Number");
	s_Number_IntValueID = frame.GetMethodID(cls, "intValue", "()I");
	s_Number_LongValueID = frame.GetMethodID(cls, "longValue", "()J");
	s_Number_DoubleValueID = frame.GetMethodID(cls, "doubleValue", "()D");

	cls = (jclass) frame.FindClass("java/lang/Boolean");
	s_BooleanValueID = frame.GetMethodID(cls, "booleanValue", "()Z");

	cls = (jclass) frame.FindClass("java/lang/Character");
	s_CharValueID = frame.GetMethodID(cls, "charValue", "()C");

	jfieldID fid;
	cls = (jclass) frame.FindClass("java/lang/Float");
	fid = frame.GetStaticFieldID(cls, "MIN_VALUE", "F");
	s_Float_Min = frame.GetStaticFloatField(cls, fid);
	fid = frame.GetStaticFieldID(cls, "MAX_VALUE", "F");
	s_Float_Max = frame.GetStaticFloatField(cls, fid);
	JP_TRACE_OUT;
}

jclass JPJni::findClass(const string& str)
{
	JPJavaFrame frame;
	return (jclass) frame.keep((jobject) frame.FindClass(str));
}

bool JPJni::equalsObject(jobject obj1, jobject obj2)
{
	JPJavaFrame frame;
	jvalue v;
	v.l = obj2;
	return frame.CallBooleanMethodA(obj1, s_Object_EqualsID, &v) != 0;
}

jobject JPJni::stringToCharArray(jstring str)
{
	JPJavaFrame frame;
	jobject res = frame.CallObjectMethod(str, s_String_ToCharArrayID);
	return frame.keep(res);
}

jclass JPJni::getClass(jobject o)
{
	JPJavaFrame frame;
	return (jclass) frame.keep(frame.CallObjectMethod(o, s_Object_GetClassID));
}

string JPJni::toString(jobject o)
{
	JPJavaFrame frame;
	if (s_Object_ToStringID == NULL)
		return "not initialized";
	jstring jname = (jstring) frame.CallObjectMethod(o, s_Object_ToStringID);
	return toStringUTF8(jname);
}

jclass JPJni::getComponentType(jclass c)
{
	JPJavaFrame frame;
	return (jclass) frame.keep(frame.CallObjectMethod(c, s_Class_GetComponentTypeID));
}

string JPJni::getName(jclass c)
{
	JPJavaFrame frame;
	jstring jname = (jstring) frame.CallObjectMethod(c, s_Class_GetNameID);
	return toStringUTF8(jname);
}

string JPJni::getCanonicalName(jclass clazz)
{
	JP_TRACE_IN("getCanonicalName");
	JPJavaFrame frame;
	jstring str = (jstring) frame.CallObjectMethod(clazz, s_Class_GetCanonicalNameID);
	// Anonymous classes don't have canonical names so they return null
	if (str == NULL)
		str = (jstring) frame.CallObjectMethod(clazz, s_Class_GetNameID);
	JP_TRACE("toString");
	return JPJni::toStringUTF8(str);
	JP_TRACE_OUT;
}

bool JPJni::isArray(jclass clazz)
{
	JPJavaFrame frame;
	jboolean b = frame.CallBooleanMethod(clazz, s_Class_IsArrayID);
	return (b ? true : false);
}

bool JPJni::isInterface(jclass clazz)
{
	JPJavaFrame frame;
	jboolean b = frame.CallBooleanMethod(clazz, s_Class_IsInterfaceID);
	return (b ? true : false);
}

bool JPJni::isAbstract(jclass clazz)
{
	JPJavaFrame frame;
	jvalue modif;
	modif.i = frame.CallIntMethod(clazz, s_Class_GetModifiersID);
	jboolean res = frame.CallStaticBooleanMethodA(s_ModifierClass, s_Modifier_IsAbstractID, &modif);

	return (res ? true : false);
}

long JPJni::getClassModifiers(jclass clazz)
{
	JPJavaFrame frame;
	return frame.CallIntMethod(clazz, s_Class_GetModifiersID);
}

bool JPJni::isFinal(jclass clazz)
{
	JPJavaFrame frame;
	jvalue modif;
	modif.i = frame.CallIntMethod(clazz, s_Class_GetModifiersID);
	jboolean res = frame.CallStaticBooleanMethodA(s_ModifierClass, s_Modifier_IsFinalID, &modif);

	return (res ? true : false);
}

bool JPJni::isFieldPublic(jobject field)
{
	JPJavaFrame frame;
	jvalue modif;
	modif.i = frame.CallIntMethod(field, s_Field_GetModifiersID);
	jboolean res = frame.CallStaticBooleanMethodA(s_ModifierClass, s_Modifier_IsPublicID, &modif);

	return (res ? true : false);
}

jobjectArray JPJni::getInterfaces(JPJavaFrame& frame, jclass clazz)
{
	return (jobjectArray) frame.CallObjectMethod(clazz, s_Class_GetInterfacesID);
}

jobjectArray JPJni::getDeclaredFields(JPJavaFrame& frame, jclass clazz)
{
	return (jobjectArray) frame.CallObjectMethod(clazz, s_Class_GetDeclaredFieldsID);
}

jobjectArray JPJni::getDeclaredConstructors(JPJavaFrame& frame, jclass clazz)
{
	return (jobjectArray) frame.CallObjectMethod(clazz, s_Class_GetDeclaredConstructorsID);
}

jobjectArray JPJni::getMethods(JPJavaFrame& frame, jclass clazz)
{
	return (jobjectArray) frame.CallObjectMethod(clazz, s_Class_GetMethodsID);
}

// Returns local reference

jobject JPJni::getSystemClassLoader()
{
	JPJavaFrame frame;
	return frame.keep(frame.CallStaticObjectMethod(s_ClassLoaderClass, s_ClassLoader_GetSystemClassLoaderID));
}

string JPJni::getMemberName(jobject o)
{
	JPJavaFrame frame;
	jstring name = (jstring) frame.CallObjectMethod(o, s_Member_GetMemberNameID);

	string simpleName = toStringUTF8(name);
	return simpleName;
}

bool JPJni::isMemberPublic(jobject o)
{
	JPJavaFrame frame;
	jvalue modif;
	modif.i = frame.CallIntMethod(o, s_Member_GetModifiersID);
	jboolean res = frame.CallStaticBooleanMethodA(s_ModifierClass, s_Modifier_IsPublicID, &modif);

	return (res ? true : false);
}

bool JPJni::isMemberStatic(jobject o)
{
	JPJavaFrame frame;
	jvalue modif;
	modif.i = frame.CallIntMethod(o, s_Member_GetModifiersID);
	jboolean res = frame.CallStaticBooleanMethodA(s_ModifierClass, s_Modifier_IsStaticID, &modif);

	return (res ? true : false);
}

bool JPJni::isMemberFinal(jobject o)
{
	JPJavaFrame frame;
	jvalue modif;
	modif.i = frame.CallIntMethod(o, s_Member_GetModifiersID);
	jboolean res = frame.CallStaticBooleanMethodA(s_ModifierClass, s_Modifier_IsFinalID, &modif);

	return (res ? true : false);
}

bool JPJni::isMemberAbstract(jobject o)
{
	JPJavaFrame frame;
	jvalue modif;
	modif.i = frame.CallIntMethod(o, s_Member_GetModifiersID);
	jboolean res = frame.CallStaticBooleanMethodA(s_ModifierClass, s_Modifier_IsAbstractID, &modif);

	return (res ? true : false);
}

jint JPJni::hashCode(jobject obj)
{
	JPJavaFrame frame;
	return frame.CallIntMethod(obj, s_Object_HashCodeID);
}

jclass JPJni::getFieldType(jobject fld)
{
	JPJavaFrame frame;
	return (jclass) frame.keep(frame.CallObjectMethod(fld, s_Field_GetTypeID));
}

jclass JPJni::getMethodReturnType(jobject o)
{
	JPJavaFrame frame;
	return (jclass) frame.keep(frame.CallObjectMethod(o, s_Method_GetReturnTypeID));
}

bool JPJni::isMethodSynthetic(jobject o)
{
	JPJavaFrame frame;
	jboolean res = frame.CallBooleanMethod(o, s_Method_IsSyntheticMethodID);
	return (res ? true : false);
}

bool JPJni::isMethodVarArgs(jobject o)
{
	JPJavaFrame frame;
	jboolean res = frame.CallBooleanMethod(o, s_Method_IsVarArgsMethodID);
	return (res ? true : false);
}

//FIXME tough one

vector<JPClassRef> JPJni::getMethodParameterTypes(jobject o, bool isConstructor)
{
	JPJavaFrame frame;
	vector<JPClassRef> args;

	jobjectArray types;
	if (isConstructor)
	{
		types = (jobjectArray) frame.CallObjectMethod(o, s_Constructor_GetParameterTypesID);
	} else
	{
		types = (jobjectArray) frame.CallObjectMethod(o, s_Method_GetParameterTypesID);
	}

	int len = frame.GetArrayLength(types);
	{
		JPJavaFrame frame2(4 + len);
		for (int i = 0; i < len; i++)
		{
			args.push_back((jclass) frame.GetObjectArrayElement(types, i));
		}
	}
	return args;
}

bool JPJni::isConstructor(jobject obj)
{
	JPJavaFrame frame;
	return frame.IsInstanceOf(obj, s_ConstructorClass) != 0;
}

bool JPJni::isThrowable(jclass c)
{
	JPJavaFrame frame;
	return frame.IsAssignableFrom(c, s_ThrowableClass) != 0;
}

long JPJni::intValue(jobject obj)
{
	JPJavaFrame frame;
	return frame.CallIntMethod(obj, s_Number_IntValueID);
}

jlong JPJni::longValue(jobject obj)
{
	JPJavaFrame frame;
	return frame.CallLongMethod(obj, s_Number_LongValueID);
}

double JPJni::doubleValue(jobject obj)
{
	JPJavaFrame frame;
	return frame.CallDoubleMethod(obj, s_Number_DoubleValueID);
}

bool JPJni::booleanValue(jobject obj)
{
	JPJavaFrame frame;
	return frame.CallBooleanMethod(obj, s_BooleanValueID) ? true : false;
}

jchar JPJni::charValue(jobject obj)
{
	JPJavaFrame frame;
	return frame.CallCharMethod(obj, s_CharValueID);
}

jclass JPJni::getPrimitiveClass(jclass clz)
{
	JPJavaFrame frame;
	jfieldID fid = frame.GetStaticFieldID(clz, "TYPE", "Ljava/lang/Class;");
	jclass res = (jclass) frame.keep(frame.GetStaticObjectField(clz, fid));
	return res;
}

class JPStringAccessor
{
	JPJavaFrame& frame_;
	jboolean isCopy;

public:
	const char* cstr;
	int length;
	jstring jstr_;

	JPStringAccessor(JPJavaFrame& frame, jstring jstr)
	: frame_(frame), jstr_(jstr)
	{
		cstr = frame_.GetStringUTFChars(jstr, &isCopy);
		length = frame_.GetStringUTFLength(jstr);
	}

	~JPStringAccessor()
	{
		frame_.ReleaseStringUTFChars(jstr_, cstr);
	}
} ;

string JPJni::toStringUTF8(jstring str)
{
	JPJavaFrame frame;
	JPStringAccessor contents(frame, str);
	return transcribe(contents.cstr, contents.length, JPEncodingJavaUTF8(), JPEncodingUTF8());
}

jstring JPJni::fromStringUTF8(const string& str)
{
	JPJavaFrame frame;
	string mstr = transcribe(str.c_str(), str.size(), JPEncodingUTF8(), JPEncodingJavaUTF8());
	return (jstring) frame.keep(frame.NewStringUTF(mstr.c_str()));
}
