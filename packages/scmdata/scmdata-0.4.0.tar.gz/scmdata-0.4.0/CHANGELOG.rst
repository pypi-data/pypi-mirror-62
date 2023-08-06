Changelog
=========

master
------

v0.4.0
------

- (`#28 <https://github.com/lewisjared/scmdata/pull/28>`_) Expose ``scmdata.units.unit_registry``

v0.3.1
------

- (`#25 <https://github.com/lewisjared/scmdata/pull/25>`_) Make scipy an optional dependency
- (`#24 <https://github.com/lewisjared/scmdata/pull/24>`_) Fix missing "N2O" unit (see `#14 <https://github.com/lewisjared/scmdata/pull/14>`_). Also updates test of year to day conversion, it is 365.25 to within 0.01% (but depends on the Pint release).

v0.3.0
------

- (`#20 <https://github.com/lewisjared/scmdata/pull/20>`_) Add support for python=3.5
- (`#19 <https://github.com/lewisjared/scmdata/pull/19>`_) Add support for python=3.6

v0.2.2
------

- (`#16 <https://github.com/lewisjared/scmdata/pull/16>`_) Only rename columns when initialising data if needed

v0.2.1
------

- (`#13 <https://github.com/lewisjared/scmdata/pull/13>`_) Ensure ``LICENSE`` is included in package
- (`#11 <https://github.com/lewisjared/scmdata/pull/11>`_) Add SO2F2 unit and update to Pyam v0.3.0
- (`#12 <https://github.com/lewisjared/scmdata/pull/12>`_) Add ``get_unique_meta`` convenience method
- (`#10 <https://github.com/lewisjared/scmdata/pull/10>`_) Fix extrapolation bug which prevented any extrapolation from occuring

v0.2.0
------

- (`#9 <https://github.com/lewisjared/scmdata/pull/9>`_) Add ``time_mean`` method
- (`#8 <https://github.com/lewisjared/scmdata/pull/8>`_) Add ``make docs`` target

v0.1.2
------

- (`#7 <https://github.com/lewisjared/scmdata/pull/7>`_) Add notebook tests
- (`#4 <https://github.com/lewisjared/scmdata/pull/4>`_) Unit conversions for CH4 and N2O contexts now work for compound units (e.g. 'Mt CH4 / yr' to 'Gt C / day')
- (`#6 <https://github.com/lewisjared/scmdata/pull/6>`_) Add auto-formatting

v0.1.1
------

- (`#5 <https://github.com/lewisjared/scmdata/pull/5>`_) Add ``scmdata.dataframe.df_append`` to ``__init__.py``

v0.1.0
------

- (`#3 <https://github.com/lewisjared/scmdata/pull/3>`_) Added documentation for the api and Makefile targets for releasing
- (`#2 <https://github.com/lewisjared/scmdata/pull/2>`_) Refactored scmdataframe from openclimatedata/openscm@077f9b5 into a standalone package
- (`#1 <https://github.com/lewisjared/scmdata/pull/1>`_) Add docs folder
