"""
    Copyright 2017 Inmanta

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
import re

import yaml
from pkg_resources import parse_version

from inmanta import module
from inmanta.module import Project
from inmanta.moduletool import ModuleTool
from moduletool.common import add_file, commitmodule, install_project, make_module_simple, makeproject
from test_app_cli import app


def test_versioning():
    mt = ModuleTool()

    newversion = mt.determine_new_version(parse_version("1.2.3"), None, False, False, True, False)
    assert str(newversion) == "1.2.4"
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, False, True, False, False)
    assert str(newversion) == "1.3.0"
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, False, False, False)
    assert str(newversion) == "2.0.0"
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, True, False, False)
    assert newversion is None
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, False, True, False)
    assert newversion is None
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, True, True, False)
    assert newversion is None
    newversion = mt.determine_new_version(parse_version("1.2.3.dev025"), None, False, False, True, False)
    assert str(newversion) == "1.2.3"
    newversion = mt.determine_new_version(parse_version("1.2.3.dev025"), None, False, False, False, False)
    assert str(newversion) == "1.2.3"

    newversion = mt.determine_new_version(parse_version("1.2.3"), None, False, False, True, True)
    assert re.search("1.2.4.dev[0-9]+", str(newversion))
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, False, True, False, True)
    assert re.search("1.3.0.dev[0-9]+", str(newversion))
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, False, False, True)
    assert re.search("2.0.0.dev[0-9]+", str(newversion))
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, True, False, True)
    assert newversion is None
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, False, True, True)
    assert newversion is None
    newversion = mt.determine_new_version(parse_version("1.2.3"), None, True, True, True, True)
    assert newversion is None
    newversion = mt.determine_new_version(parse_version("1.2.3.dev025"), None, False, False, True, True)
    assert re.search("1.2.3.dev[0-9]+", str(newversion))
    newversion = mt.determine_new_version(parse_version("1.2.3.dev025"), None, False, False, False, True)
    assert re.search("1.2.3.dev[0-9]+", str(newversion))


def test_rewrite(tmpdir):
    module_path = tmpdir.join("mod").mkdir()
    model = module_path.join("model").mkdir()
    model.join("_init.cf").write("\n")

    module_yml = module_path.join("module.yml")
    module_yml.write(
        """
name: mod
license: ASL
version: 1.2
compiler_version: 2017.2
    """
    )

    mod = module.Module(None, module_path.strpath)

    assert mod.version == "1.2"
    assert mod.compiler_version == "2017.2"

    mod.rewrite_version("1.3.1")
    assert mod.version == "1.3.1"
    assert mod.compiler_version == "2017.2"


def test_module_corruption(modules_dir, modules_repo):
    mod9 = make_module_simple(modules_repo, "mod9", [("mod10", None)])
    add_file(mod9, "signal", "present", "third commit", version="3.3")
    add_file(mod9, "model/b.cf", "import mod9", "fourth commit", version="4.0")

    mod10 = make_module_simple(modules_repo, "mod10", [])
    add_file(mod10, "signal", "present", "a commit", version="3.3")
    add_file(mod10, "secondsignal", "import mod9", "b commit", version="4.0")
    add_file(mod10, "badsignal", "import mod9", "c commit", version="5.0")

    p9 = makeproject(modules_repo, "proj9", [("mod9", "==3.3")], ["mod9"])
    commitmodule(p9, "first commit")

    # setup project
    proj = install_project(modules_dir, "proj9")
    app(["modules", "install"])
    print(os.listdir(proj))
    # overwrite main to import unknown sub module
    # unfreeze deps to allow update
    main = os.path.join(proj, "main.cf")
    projectyml = os.path.join(proj, "project.yml")
    assert os.path.exists(main)
    assert os.path.exists(projectyml)

    with open(main, "w", encoding="utf-8") as fh:
        fh.write("import mod9::b")

    with open(projectyml, "r", encoding="utf-8") as fh:
        pyml = yaml.load(fh)

    pyml["requires"] = ["mod10 == 4.0"]

    with open(projectyml, "w", encoding="utf-8") as fh:
        yaml.dump(pyml, fh)

    # clear cache
    Project._project = None

    # attempt to update
    app(["modules", "update"])

    # Additional output
    Project._project = None
    app(["modules", "list"])

    # Verify
    m9dir = os.path.join(proj, "libs", "mod9")
    assert os.path.exists(os.path.join(m9dir, "model", "b.cf"))
    m10dir = os.path.join(proj, "libs", "mod10")
    assert os.path.exists(os.path.join(m10dir, "secondsignal"))
    # should not be lastest version
    assert not os.path.exists(os.path.join(m10dir, "badsignal"))
