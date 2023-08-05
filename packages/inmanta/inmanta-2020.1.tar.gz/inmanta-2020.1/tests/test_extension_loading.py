"""
    Copyright 2019 Inmanta

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
import importlib
import logging
import os
import sys
from contextlib import contextmanager
from typing import Any, Generator

import pytest
import yaml

import inmanta.server
import inmanta_ext
from inmanta.config import feature_file_config
from inmanta.server import SLICE_AGENT_MANAGER, SLICE_SERVER, SLICE_SESSION_MANAGER, SLICE_TRANSPORT, config
from inmanta.server.agentmanager import AgentManager
from inmanta.server.bootloader import InmantaBootloader, PluginLoadFailed
from inmanta.server.extensions import BoolFeature, FeatureManager, InvalidFeature, InvalidSliceNameException, StringListFeature
from inmanta.server.protocol import Server, ServerSlice
from utils import log_contains


@contextmanager
def splice_extension_in(name: str) -> Generator[Any, Any, None]:
    """Context manager to all extensions in tests/data/{name}/inmanta_ext/ to the interpreter and unload them again"""
    oldpath = sys.path
    try:
        sys.path = sys.path + [os.path.join(os.path.dirname(__file__), "data", name)]
        importlib.reload(inmanta_ext)
        yield
    finally:
        sys.path = oldpath
        importlib.reload(inmanta_ext)


def test_discover_and_load():
    with splice_extension_in("test_module_path"):

        config.server_enabled_extensions.set("testplugin")

        ibl = InmantaBootloader()
        print("plugins: ", ibl._discover_plugin_packages())

        assert "inmanta_ext.testplugin" in ibl._discover_plugin_packages()

        tpl = ibl._load_extension("inmanta_ext.testplugin")

        assert tpl == inmanta_ext.testplugin.extension.setup

        with pytest.raises(PluginLoadFailed):
            ibl._load_extension("inmanta_ext.noext")

        with pytest.raises(PluginLoadFailed):
            ibl._load_extension("inmanta_ext.noinit")


def test_phase_1(caplog):
    with splice_extension_in("test_module_path"):
        ibl = InmantaBootloader()

        config.server_enabled_extensions.set("testplugin,noext")

        all = ibl._load_extensions()

        assert "testplugin" in all
        assert all["testplugin"] == inmanta_ext.testplugin.extension.setup

        log_contains(caplog, "inmanta.server.bootloader", logging.WARNING, "Could not load extension inmanta_ext.noext")


def test_phase_2():
    with splice_extension_in("test_module_path"):
        import inmanta_ext.testplugin.extension

        ibl = InmantaBootloader()
        all = {"testplugin": inmanta_ext.testplugin.extension.setup}

        ctx = ibl._collect_slices(all)

        byname = {sl.name: sl for sl in ctx._slices}

        assert "testplugin.testslice" in byname

        # load slice in wrong namespace
        with pytest.raises(InvalidSliceNameException):
            all = {"test": inmanta_ext.testplugin.extension.setup}
            ctx = ibl._collect_slices(all)


def test_phase_3():
    with splice_extension_in("test_module_path"):
        from inmanta_ext.testplugin.extension import XTestSlice

        server = Server()
        server.add_slice(XTestSlice())
        server.add_slice(inmanta.server.server.Server())
        server.add_slice(AgentManager())

        order = server._get_slice_sequence()
        print([s.name for s in order])
        assert [s.name for s in order] == [
            SLICE_SERVER,
            SLICE_SESSION_MANAGER,
            SLICE_AGENT_MANAGER,
            SLICE_TRANSPORT,
            "testplugin.testslice",
        ]


def test_end_to_end():
    with splice_extension_in("test_module_path"):
        ibl = InmantaBootloader()

        config.server_enabled_extensions.set("testplugin")

        ctx = ibl.load_slices()
        byname = {sl.name: sl for sl in ctx.get_slices()}
        assert "testplugin.testslice" in byname


def test_end_to_end_2():
    with splice_extension_in("bad_module_path"):
        config.server_enabled_extensions.set("badplugin")

        ibl = InmantaBootloader()
        all = ibl._load_extensions()
        print(all)
        assert "badplugin" in all

    config.server_enabled_extensions.set("")
    all = ibl._load_extensions()
    assert "badplugin" not in all


@pytest.mark.asyncio
async def test_startup_failure(async_finalizer, server_config):
    with splice_extension_in("bad_module_path"):
        config.server_enabled_extensions.set("badplugin")

        ibl = InmantaBootloader()
        async_finalizer.add(ibl.stop)
        with pytest.raises(Exception) as e:
            await ibl.start()

        print(e.value)
        assert str(e.value) == "Slice badplugin.badslice failed to start because: Too bad, this plugin is broken"

    config.server_enabled_extensions.set("")
    all = ibl._load_extensions()
    assert "badplugin" not in all


def test_load_and_filter(caplog):
    caplog.set_level(logging.INFO)

    with splice_extension_in("test_module_path"):
        ibl = InmantaBootloader()

        plugin_pkgs = ibl._discover_plugin_packages()
        assert "inmanta_ext.core" in plugin_pkgs
        assert len(plugin_pkgs) == 1

        # When extensions are available but not enabled, log a message with the correct option
        log_contains(caplog, "inmanta.server.bootloader", logging.INFO, "Load extensions by setting configuration option")

        with pytest.raises(PluginLoadFailed):
            config.server_enabled_extensions.set("unknown")
            plugin_pkgs = ibl._discover_plugin_packages()


def test_load_feature_file(tmp_path):
    feature_file = tmp_path / "features.yml"
    feature_file.write_text(yaml.dump({"slices": {"test": {"feature1": False, "list_feature1": ["one"]}}}))
    feature_file_config.set(str(feature_file))

    fm = FeatureManager()
    f1 = BoolFeature(slice="test", name="feature1")
    f2 = BoolFeature(slice="test", name="feature2")
    fx = BoolFeature(slice="test", name="featurex")
    s1 = StringListFeature(slice="test", name="list_feature1")
    s2 = StringListFeature(slice="test", name="list_feature2")

    class MockSlice(ServerSlice):
        def __init__(self):
            super().__init__("test")

        def define_features(self):
            return [f1, f2, s1, s2]

    slice = MockSlice()
    fm.add_slice(slice)

    assert slice.feature_manager is fm

    assert not fm.enabled(f1)
    assert fm.enabled(f2)

    with pytest.raises(InvalidFeature):
        fm.enabled(fx)

    assert fm.contains(s1, "one")
    assert not fm.contains(s1, "two")
    assert fm.contains(s2, "random")


@pytest.mark.asyncio
async def test_custom_feature_manager(
    tmp_path, inmanta_config, postgres_db, database_name, clean_reset, unused_tcp_port_factory
):
    with splice_extension_in("test_module_path"):
        state_dir = str(tmp_path)
        port = str(unused_tcp_port_factory())
        config.Config.set("database", "name", database_name)
        config.Config.set("database", "host", "localhost")
        config.Config.set("database", "port", str(postgres_db.port))
        config.Config.set("database", "connection_timeout", str(1))
        config.Config.set("config", "state-dir", state_dir)
        config.Config.set("config", "log-dir", os.path.join(state_dir, "logs"))
        config.Config.set("agent_rest_transport", "port", port)
        config.Config.set("compiler_rest_transport", "port", port)
        config.Config.set("client_rest_transport", "port", port)
        config.Config.set("cmdline_rest_transport", "port", port)
        config.Config.set("server", "bind-port", port)
        config.Config.set("server", "bind-address", "127.0.0.1")
        config.server_enabled_extensions.set("testfm")

        ibl = InmantaBootloader()
        await ibl.start()
        server = ibl.restserver

        fm = server.get_slice(SLICE_SERVER).feature_manager

        assert not fm.enabled(None)
        assert not fm.enabled("a")

        await ibl.stop()
