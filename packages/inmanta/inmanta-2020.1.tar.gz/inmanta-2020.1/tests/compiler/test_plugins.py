"""
    Copyright 2018 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import os

import inmanta.compiler as compiler
from inmanta.ast import Namespace


def test_plugin_excn(snippetcompiler):
    snippetcompiler.setup_for_error(
        """
        import std
        std::template("/tet.tmpl")
""",
        """Exception in plugin std::template (reported in std::template('/tet.tmpl') ({dir}/main.cf:3))
caused by:
  jinja2.exceptions.TemplateNotFound: /tet.tmpl
""",
    )


def test_1221_plugin_incorrect_type_annotation(snippetcompiler):
    modpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "modules", "test_1221")
    snippetcompiler.setup_for_error(
        """
import test_1221
        """,
        "could not find type std::WrongName in namespace std (%s/plugins/__init__.py:5:1)" % modpath,
    )


def test_kwargs_in_plugin_call(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
str = std::replace("Hello World!", new = "You", old = "World")
        """,
    )
    (_, scopes) = compiler.do_compile()
    root: Namespace = scopes.get_child("__config__")
    assert root.lookup("str").get_value() == "Hello You!"


def test_wrapped_kwargs_in_plugin_call(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
dct = {
    "new": "You",
    "old": "World",
}
str = std::replace("Hello World!", **dct)
        """,
    )
    (_, scopes) = compiler.do_compile()
    root: Namespace = scopes.get_child("__config__")
    assert root.lookup("str").get_value() == "Hello You!"


def test_kwargs_in_plugin_call_missing_arg(snippetcompiler):
    snippetcompiler.setup_for_error(
        """
std::equals(42, desc="they differ")
        """,
        "Missing 1 required arguments for equals(): arg2" " (reported in std::equals(42,desc='they differ') ({dir}/main.cf:2))",
    )


def test_kwargs_in_plugin_call_double_arg(snippetcompiler):
    snippetcompiler.setup_for_error(
        """
std::equals(42, 42, arg1=42)
        """,
        "Multiple values for arg1 in equals() (reported in std::equals(42,42,arg1=42) ({dir}/main.cf:2))",
    )


def test_kwargs_in_plugin_call_double_kwarg(snippetcompiler):
    snippetcompiler.setup_for_error(
        """
std::equals(42, arg2=42, arg2=42)
        """,
        "Keyword argument arg2 repeated in function call std::equals()"
        " (reported in std::equals(42,arg2=42) ({dir}/main.cf:2))",
    )


def test_1774_plugin_returning_entity_in_list(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
import test_1774

test_1774::test_list(test_1774::Test())
        """,
    )
    compiler.do_compile()


def test_1774_plugin_returning_entity_in_dict(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
import test_1774

test_1774::test_dict(test_1774::Test())
        """,
    )
    compiler.do_compile()


def test_674_nullable_type_in_plugin_arguments(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
import test_674

test_674::test_nullable("str")
test_674::test_nullable(null)
        """,
    )
    compiler.do_compile()


def test_674_not_nullable_type_in_plugin_arguments(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
import test_674

test_674::test_not_nullable("Hello World!")
        """,
    )
    compiler.do_compile()


def test_674_not_nullable_type_in_plugin_arguments_error(snippetcompiler):
    snippetcompiler.setup_for_error(
        """
import test_674

test_674::test_not_nullable(null)
        """,
        "Invalid value 'null', expected String (reported in test_674::test_not_nullable(null) ({dir}/main.cf:4))",
    )


def test_674_nullable_list_type_in_plugin_arguments(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
import test_674

test_674::test_nullable_list([42, 12])
test_674::test_nullable_list(null)
        """,
    )
    compiler.do_compile()


def test_674_not_nullable_list_type_in_plugin_arguments(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
import test_674

test_674::test_not_nullable_list([1,2])
        """,
    )
    compiler.do_compile()


def test_674_not_nullable_list_type_in_plugin_arguments_error(snippetcompiler):
    snippetcompiler.setup_for_error(
        """
import test_674

test_674::test_not_nullable_list(null)
        """,
        "Invalid value 'null', expected number[] (reported in test_674::test_not_nullable_list(null) ({dir}/main.cf:4))",
    )


def test_674_nullable_type_in_plugin_return(snippetcompiler):
    snippetcompiler.setup_for_snippet(
        """
import test_674

x = test_674::test_returns_none()
x = null
        """,
    )
    compiler.do_compile()


def test_1778_context_as_kwarg_reject(snippetcompiler):
    snippetcompiler.setup_for_error(
        """
std::generate_password("pw_id", context=42)
        """,
        "Invalid keyword argument 'context' for 'generate_password()'"
        " (reported in std::generate_password('pw_id',context=42) ({dir}/main.cf:2))",
    )
