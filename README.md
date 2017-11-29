# State-Level Demographic Data

A simple command-line utility for accessing economic demographic data from the National Broadband Map.

### Installation

To install, simply clone the repo, `cd` in and run `pip install -r requirements.txt` to install dependencies.

### Usage

The basic command line pattern is `python states.py <state1>,<state2> [csv/averages]`. Each state must be a three letter abbreviation. Optionally, an output format can be specified, either `csv` or `averages` (defaults to `csv`).

Example:

`python states.py cal,ore csv`

returns:

```
state, population, households, income_below_poverty_level, median_income
California, 38660952, 14450824, 0.1572, 69823.7016
Oregon, 3996309, 1779290, 0.1594, 53775.8649
```

### Testing

To run tests, `pip install -r test.requirements.txt` to get the test requirements. You will have to add the path to the repo to your `PYTHONPATH` variable in order to import the states module.  Optionally, you can execute the tests with `coverage` to see a coverage ruport.

### Design Assumptions

The first assumption is that invoking this with the `python` command is good enough for the purposes of this exercise. Were I to spend more time on this I would probably give it a 'proper' clever CLI utility command like `lsc` (late-stage capitalism).

This also assumes that a simple print statement for error messages is goon enough. A more rubust implementation might use `stderr`, or raise exceptions (which would _obviously_ be recorded in APM) depending on the usage.

Another assumption is that requiring the user to input exact state IDs is good enough for this exercise. Given more time I'd probably like to implement a more tolerant system that could handle different formats (eg, OR, ore, and oregon).

A final assumption/design decision I made after looking at the data is that weighting the average based on number of households instead of population will give a somewhat more accurate view.