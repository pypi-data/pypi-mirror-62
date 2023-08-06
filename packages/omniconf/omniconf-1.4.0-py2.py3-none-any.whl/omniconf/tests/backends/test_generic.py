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

from omniconf.backends.generic import ConfigBackend
from omniconf.setting import Setting
import nose.tools


def test_config_backend_autoconfigure():
    with nose.tools.assert_raises(NotImplementedError):
        ConfigBackend.autoconfigure(None, None)


def test_config_backend_autodetect_settings():
    nose.tools.assert_equal(ConfigBackend.autodetect_settings(None), ())


def test_config_backend_get_values_no_settings():
    nose.tools.assert_equal(ConfigBackend().get_values([]), [])


def test_config_backend_get_values_missing_value():
    backend = ConfigBackend(conf={})
    setting = Setting("foo", _type=str)
    values = backend.get_values([setting])
    nose.tools.assert_equal(values, [])


def test_config_backend_get_values():
    backend = ConfigBackend(conf={"foo": "bar"})
    setting = Setting("foo", _type=str)
    values = backend.get_values([setting])
    nose.tools.assert_equal(values, [(setting, "bar")])
