# The DRASTIC corpus
[![CC BY 4.0][cc-by-shield]][cc-by]

Dataset and scripts for the DRASTIC corpus of DRS-annotated texts.

The repository has the following structure:

```
├── data
│   ├── anaphora-resolution
│   │   ├── dvorak
│   │   ├── marbles
│   │   ├── nida
│   │   └── short-texts
│   └── no-anaphora-resolution
│       ├── dvorak
│       ├── marbles
│       ├── nida
│       └── short-texts
└── scripts
```

`data` contains two versions of the DRS-annotated texts: one with sentence-internal anaphora resolved (`anaphora-resolution`) and one without (`no-anaphora-resolution`). Within each of these, the texts are divided by sub-corpus, and named for their corresponding GUM sent\_id (for details, see the paper, referenced below).

`scripts` contains a script (`flatten_clause_notation.py`) which will 'flatten' PMB-style DRSs into our simplified format. We also provide a shell script (`flatten_clause_notation_in_batch.sh`) to run this on multiple files at once.

If you use this data, please cite the following paper:

Haug, Dag T. T., Jamie Y. Findlay and Ahmet Yıldırım. 2023. The long and the short of it: DRASTIC, a semantically annotated dataset containing sentences of more natural length. _Proceedings of the 4th International Workshop on Designing Meaning Representations (DMR 2023)_. Association for Computational Linguistics.

```
  @inproceedings{haug_etal:drastic,
    title           = {The long and the short of it: \textsc{drastic}, a semantically annotated dataset containing sentences of more natural length},
    year            = {2023},
    author          = {Dag T. T. Haug and Jamie Y. Findlay and Ahmet Y\i{}ld\i{}r\i{}m},
    booktitle       = {{Proceedings of the 4th International Workshop on Designing Meaning Representations (DMR 2023)}},
    pages           = {},
    publisher       = {Association for Computational Linguistics},
    url             = {}
  }
```

This data is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
