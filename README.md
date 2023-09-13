# undefined-concepts-tool

Find concepts that are referenced but undefined in an ontology.

## Installation

The script is tested with python 3.10. But most later versions of python3 should work.

The script requires the `rdflib` library. Install with `pip install rdflib`.

TODO: This should be either created as a package, or a virtual environment to reduce the
errors that might crop up in dependencies.

## Usage

The command takes to arguments context and a focus graph. The context should include all of the
ontology files that are imported by the focus graph. These files can all be in a directory, or specified
individually.
For example imagine a structure:

```
project
|--ontologies
|  |--- ontologyA.ttl
|  |--- ontolgoyB.ttl
|--taxonomies
|  |--- taxonomyA.ttl
|  |--- bad_taxonomy.ttl
|-- focus_ontology_a.ttl
|--- focus_ontology_b.ttl
```

If one does not want to include the file `bad_taxonomy.ttl`, run `./find_undefined_concepts focus_ontology_a.ttl focus_ontology_b.ttl -c ontologies/ taxonomies/taxonomyA.ttl`.
Or one could run: `./find_undefined_concepts -c ontologies/ taxonomies/taxonomyA.ttl -- focus_ontology_a.ttl focus_ontology_b.ttl`.

Everything after the `-c` or `--context` flag is treated as an array of either files or directories. The focus graph file or files needs to appear before the flag, or after a `--`, or directly after the command if there is no context flag added.
