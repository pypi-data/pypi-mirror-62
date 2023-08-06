Usage
=====

Basic usage
-----------

The most basic usage of |project| requires the use of the :func:`setting`, :func:`config` and
:func:`omniconf_load` functions:

.. autofunction :: omniconf.setting
.. autofunction :: omniconf.config
.. autofunction :: omniconf.omniconf_load

Define Settings using :func:`setting`:

.. code-block:: python

   from omniconf import setting
   setting("app.username")
   setting("app.hostname")


After defining the Settings, use :func:`omniconf_load` to load values:

.. code-block:: python

   from omniconf import omniconf_load
   omniconf_load()

Afterwards, you can use :func:`config` to retrieve values.

.. code-block:: python

   >>> from omniconf import config
   >>> print config("app.username")
   "user"


By default, all Settings defined using :func:`setting` will be stored as :class:`str`. To use another class, do this:

.. code-block:: python

   from omniconf import setting
   setting("app.firstname", _type=unicode)
   setting("app.load_order", _type=list)

Any class can be used. See :ref:`setting-types` for more information.

Advanced usage
--------------

By default all Settings and Configs are registered in global Registries. These are defined in their respective modules:

.. autodata:: omniconf.config.DEFAULT_REGISTRY
.. autodata:: omniconf.setting.DEFAULT_REGISTRY

This allows you to easily define Settings. Sometimes you might want to have specific Settings and Configs however. You
can achieve this by specifying your own Registries:

.. code-block:: python

   from omniconf.setting import SettingRegistry
   from omniconf.config import ConfigRegistry
   from omniconf import omniconf_load

   settings = SettingRegistry()
   configs = ConfigRegistry(setting_registry=settings)

   setting("app.username", registry=settings)

   omniconf_load(config_registry=configs)


|project| actually uses this mechanism to build the context needed for autoconfiguring. You can check this out in
:func:`autoconfigure_backends`

.. autofunction :: omniconf.loader.autoconfigure_backends


Autoconfigure prefix usage
--------------------------

Prefixes are used during autoconfiguring step to load Settings, while trying to avoid name clashes with user defined
Settings. By default, `omniconf.prefix` will be loaded from the environment and cli arguments, by looking for
``OMNICONF_PREFIX`` and ``--omniconf-prefix`` respectively. In these settings, `omniconf` is the prefix.

To change the used during autoconfiguring, do the following:

.. code-block:: python

   from omniconf import omniconf_load
   omniconf_load(config_registry=configs, autoconfigure_prefix="application")

The above example will set the prefix to `application`, which will cause autoconfiguring to look for
``APPLICATION_PREFIX`` and ``--application-prefix`` instead. Good if you don't want to leak that you're using |project|
to your users.


Backend prefix usage
--------------------

Backends may allow a prefix to be defined. By default, this setting is loaded from the ``omniconf.prefix`` key (see
previous section). If defined, this value is passed to all available backends, and will influence how they will load
Config values.

For instance. if ``omniconf.prefix`` is not set, :class:`.EnvBackend` will load ``some.setting`` from the
``SOME_SETTING`` environment variable. If ``omniconf.prefix`` is set to ``app``, the value is loaded from
``APP_SOME_SETTING`` instead. See the :ref:`supported-backends` section for which Backends allow a prefix to be
configured, and how this changes the loading of values.


Prefix usage examples
---------------------

Working with prefixes can be a little tricky. The thing to keep in mind is that there are two prefix types, one that is
used during the autoconfigure step where the backends are initialized (the autoconfiguration prefix), and one that is
used when loading the configuration (the backend prefix).

Given this code snippet:

.. code-block:: python

   from omniconf import omniconf_load, config, setting

   setting("db.url", required=True)
   omniconf_load(autoconfigure_prefix="test")

   print config("db.url")


A step-by-step analysis:

1. The setting `db.url` is defined and marked as required.
2. Autoconfiguration is started and the `autoconfigure_prefix` is defined as 'test'.

   a. During autoconfiguration, by default `omniconf.prefix` will be looked up. Because we override `autoconfigure_prefix`,
      `test.prefix` is looked up instead.
   b. The contents of `test.prefix` is used by certain backends (:class:`.EnvBackend` in this example) to determine where
      they should look for their settings.

3. Config values are loaded, and the backend prefix is used to determine how it should be loaded.

Example 1
^^^^^^^^^

.. code-block:: shell

   $ python test.py

   Traceback (most recent call last):
   ...
   omniconf.exceptions.UnconfiguredSettingError: No value was configured for db.url

An error is raised because we don't set any config values at all, and `db.url` is marked as required.

Example 2
^^^^^^^^^

.. code-block:: shell

   $ TEST_DB_URL=bla python test.py
   Traceback (most recent call last):
   ...
   omniconf.exceptions.UnconfiguredSettingError: No value was configured for db.url

An error is raised because we set `TEST_DB_URL`, but no backend prefix has been configured. The value of `db.url` is
looked up in `DB_URL` which is not set.

Example 3
^^^^^^^^^

.. code-block:: shell

   $ TEST_PREFIX=OTHER OTHER_DB_URL=foo python test.py
   foo

The backend prefix is set to `OTHER`. This means that the setting for `db.url` is looked up in `OTHER_DB_URL`, which is
also set.

Example 4
^^^^^^^^^

.. code-block:: shell

   $ DB_URL=foo python test.py
   foo

No backend prefix is set. This means that the setting for `db.url` is looked up in `DB_URL`, which is also set.

Outputting usage information
----------------------------

To output :mod:`.argparse`-like usage information based on :class:`.Setting` objects contained in a
:class:`.SettingRegistry`, use the :func:`show_usage` function.

.. autofunction :: omniconf.show_usage

For instance, the output for this piece of code:

.. code-block:: python

   from omniconf import setting, show_usage

   setting("verbose", _type=bool, default=False, help="Enable verbose mode.")
   setting("section1.setting", help="An optional setting")
   setting("section1.other_setting", help="A different optional setting.")
   setting("section2.setting", required=True, help="A required setting.")

   show_usage(name="usage_example")

Looks like this:

.. code-block:: bash

   usage: usage_example [--verbose] [--section1-other_setting SOS]
                     [--section1-setting SS] --section2-setting SS

   optional arguments:
   --verbose             Enable verbose mode.

   section1:
   --section1-other_setting SOS
                        A different optional setting.
   --section1-setting SS
                        An optional setting

   section2:
   --section2-setting SS
                        A required setting.

An user who wants to show usage information, usually specifies a command line flag like ``--help``. To detect this,
|project| provides a convenience method:

.. autofunction :: omniconf.help_requested

Two other methods are also provided, one to detect a version flag, and one to detect any flag:

.. autofunction :: omniconf.version_requested
.. autofunction :: omniconf.flag_requested
