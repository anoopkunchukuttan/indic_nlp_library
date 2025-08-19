# Indic NLP Library
This repository is a _de-bloated_ fork of the original [Indic NLP Library](https://github.com/anoopkunchukuttan/indic_nlp_library) and integrates [UrduHack](https://github.com/urduhack/urduhack) submodule and [Indic NLP Resources](https://github.com/anoopkunchukuttan/indic_nlp_resources) directly. This allows to work with Urdu normalization and tokenization without needing to install [urduhack](https://pypi.org/project/urduhack/) and `indic_nlp_resources` separately, which can be an issue sometimes as it is `TensorFlow` based. This repository is mainly created and mainted for [Rotary-IndicTrans2](https://huggingface.co/collections/prajdabre/indictrans2-rope-6742ddac669a05db0804db35), [IndicTrans2](https://huggingface.co/collections/ai4bharat/indictrans2-664ccb91d23bbae0d681c3ca) and [IndicTransToolkit](https://github.com/VarunGumma/IndicTransToolkit)

For any queries, please get in touch with the original authors/maintainers of the respective libraries:

- `Indic NLP Library`: [anoopkunchukuttan](https://github.com/anoopkunchukuttan)
- `Indic NLP Resources`: [anoopkunchukuttan](https://github.com/anoopkunchukuttan) 
- `UrduHack`: [UrduHack](https://github.com/urduhack)

## Usage:
```bash
pip install indic-nlp-library-itt
```

## Updates:
- Integrated `urduhack` directly into the repository.
- Renamed `master` branch as `main`.
- Integrated `indic_nlp_resources` directly into the repository.
- _Debloated_ and _Refactored_ the repository (Please raise any issues/bugs you find!)
