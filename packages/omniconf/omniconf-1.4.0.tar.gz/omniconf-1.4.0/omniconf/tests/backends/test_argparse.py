# Copyright (c) 2016 Cyso < development [at] cyso . com >
#
# This file is part of omniconf, a.k.a. python-omniconf .
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see
# <http://www.gnu.org/licenses/>.

from omniconf.backends import available_backends
from omniconf.backends.argparse import ArgparseBackend
from omniconf.config import ConfigRegistry
from omniconf.setting import Setting, SettingRegistry
from mock import patch
import nose.tools

ARGS_FILE = [
    "--foo", "bar",
    "--section-bar", "baz",
    "--section-subsection-baz", "foo",
    "--bool-normal", "1",
    "--bool-true",
    "--bool-false",
    "--missing-value"  # Has to be the last because we're omitting the value
]

PREFIX_ARGS_FILE = [
    "--prefix-foo", "bar",
    "--prefix-section-bar", "baz",
    "--prefix-section-subsection-baz", "foo",
    "--prefix-bool-normal", "1",
    "--prefix-bool-true",
    "--prefix-bool-false",
    "--prefix-missing-value"  # Has to be the last because we're
                              # omitting the value
]

CONFIGS = [
    (Setting(key="foo", _type=str), "bar", None),
    (Setting(key="section.bar", _type=str), "baz", None),
    (Setting(key="section.subsection.baz", _type=str), "foo", None),

    (Setting(key="", _type=str), None, KeyError),
    (Setting(key="missing.value", _type=str), None, KeyError),
    (Setting(key="missing.arg", _type=str), None, IndexError),  # Raise in test

    (Setting(key="bool.normal", _type=bool), "1", None),
    (Setting(key="bool.true", _type=bool, default=False), True, None),
    (Setting(key="bool.false", _type=bool, default=True), False, None),
    (Setting(key="bool.default.true", _type=bool, default=True), True, None),
    (Setting(key="bool.default.false", _type=bool, default=False), False, None)
]


def test_argparse_backend_in_available_backends():
    nose.tools.assert_in(ArgparseBackend, available_backends)


def test_argparse_backend_autoconfigure():
    prefix = "testconf"
    backend = ArgparseBackend.autoconfigure(
        {"{0}.prefix".format(prefix): "bar"}, prefix)
    nose.tools.assert_is_instance(backend, ArgparseBackend)
    nose.tools.assert_equal(backend.prefix, "bar")


def test_argparse_backend_get_value():
    with nose.tools.assert_raises(NotImplementedError):
        backend = ArgparseBackend()
        backend.get_value(None)


def test_argparse_backend_get_values():
    for setting, value, sideeffect in CONFIGS:
        yield _test_get_values, setting, value, sideeffect, None
        yield _test_get_values, setting, value, sideeffect, 'prefix'


def _test_get_values(setting, value, sideeffect, prefix):
    with patch('omniconf.backends.argparse.ARGPARSE_SOURCE',
               ARGS_FILE if not prefix else PREFIX_ARGS_FILE):
        backend = ArgparseBackend(prefix=prefix)
        if sideeffect:
            with nose.tools.assert_raises(sideeffect):
                setting, config = backend.get_values([setting])[0]
        else:
            setting, config = backend.get_values([setting])[0]
            nose.tools.assert_equal(config, value)


def test_mixed_flags_and_settings():
    MIXED_ARGS = [
        "--verbose", "--loud",
        "--foo-bar", "baz",
        "--bar", "buzz"
    ]

    settings = SettingRegistry()
    settings.add(Setting(key="verbose", _type=bool, default=False))
    settings.add(Setting(key="loud", _type=bool, default=True))
    settings.add(Setting(key="foo.bar", _type=str))
    settings.add(Setting(key="bar", _type=str))
    configs = ConfigRegistry(setting_registry=settings)

    with patch('omniconf.backends.argparse.ARGPARSE_SOURCE', MIXED_ARGS):
        backend = ArgparseBackend(prefix=None)
        configs.load([backend])

        nose.tools.assert_true(configs.get("verbose"))
        nose.tools.assert_false(configs.get("loud"))
        nose.tools.assert_equal(configs.get("foo.bar"), "baz")
        nose.tools.assert_equal(configs.get("bar"), "buzz")
