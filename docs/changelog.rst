=========
Changelog
=========

0.2.3
=====

- :bug:`2` Fixed a typo in the call to ``InteractionError``.
- Documentation improvments

0.2.2
=====

- :bug:`1` Fixed a bug where setup.py was crashing with an ``ImportError`` when
  importing the version string from ``netscaler.py`` in the case where suds was not
  installed.

0.2.1
=====

- Replaced all usage of dictionaries passed by reference in examples with
  keyword args.

0.2 
===

- Added setup.py
- Added examples
- Added is_readonly() method to validate commands.
- Added save() shortcut method to self.client.service.savensconfig()
- Implemented autosave whenever a command executed ia run() is not read-only
  (Autosave can be disabled by passing autosave=False)

0.1 
===

- Initial release
