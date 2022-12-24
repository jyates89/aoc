# Advent of Code Repository
This is a repository to store my solutions to the Advent of Code challenges at https://adventofcode.com. I've
put a starter file that can be used for future solutions just to make it easy to get started. The downloader
package includes a class to automate downloading of the input file.

If using the starter file, copy `begin.py` into a sub folder of this project, like `{year}/days/{day}` to make sure
it will _just work_. If  not, you'll have to adjust the section here to reflect the different folder structure:

```python
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
```

The requirements file should have all the external modules I use to implement the solutions, and the `.gitignore`
should ignore the auto downloaded input files.
