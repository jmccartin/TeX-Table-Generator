TeX Table Generator
-------------

A collection of classes designed to calculate selection efficiencies and scaled events for a list of broc-made text inputs and then output them as a LaTeX compatible table.

- Replaces the old Perl project which was rather clunky
- Written in Python for clarity
  - Uses ConfigHandler to parse in a user-supplied config, no hard-coding!

Usage:

`./table_generator.py -x default_config.cfg`

An example of the output can be found [here][1].

[1]: http://mon.iihe.ac.be/~mccartin/top/acceptance/selection_efficiencies_8TeV_final.pdf
