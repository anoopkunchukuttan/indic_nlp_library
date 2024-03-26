# Indic NLP Library
This repository is a fork of the original [Indic NLP Library](https://github.com/anoopkunchukuttan/indic_nlp_library) and integrates [UrduHack](https://github.com/urduhack/urduhack) submodule and [Indic NLP Resources](https://github.com/anoopkunchukuttan/indic_nlp_resources) directly. This allows to work with Urdu normalization and tokenization without needing to install [urduhack](https://pypi.org/project/urduhack/) and `indic_nlp_resources` separately, which can be an issue sometimes as it is `TensorFlow` based. This repository is mainly created and mainted for [IndicTrans2](https://github.com/AI4Bharat/IndicTrans2) and [IndicTransTokenizer](https://github.com/VarunGumma/IndicTransTokenizer)

For any queries, please get in touch with the original authors/maintainers of the respective libraries:

- `Indic NLP Library`: [anoopkunchukuttan](https://github.com/anoopkunchukuttan)
- `Indic NLP Resources`: [anoopkunchukuttan](https://github.com/anoopkunchukuttan) 
- `UrduHack`: [UrduHack](https://github.com/urduhack)

## Usage:
```
git clone https://github.com/VarunGumma/indic_nlp_library.git

cd indic_nlp_library
pip install --editable ./
```

## Updates:
- Integrated `urduhack` directly into the repository.
- Renamed `master` branch as `main`.
- Integrated `indic_nlp_resources` directly into the repository.
