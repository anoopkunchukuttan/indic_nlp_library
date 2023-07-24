# Indic NLP Library
This repository is a fork of the original [Indic NLP Library](https://github.com/anoopkunchukuttan/indic_nlp_library) and integrates [UrduHack](https://github.com/urduhack/urduhack) submodule directly. This allows to work with Urdu normalization and tokenization without needing to install [urduhack](https://pypi.org/project/urduhack/) separately, which can be an issue sometimes as it is `TensorFlow` based. I am mainly maintaining this repository for [IndicTrans2](https://github.com/AI4Bharat/IndicTrans2). 

For any queries, please get in touch with the original authors/maintainers of the respective libraries:

- `Indic NLP Library`: [anoopkunchukuttan](https://github.com/anoopkunchukuttan)
- `UrduHack`: [UrduHack](https://github.com/urduhack)

The data resources required by the Indic NLP Library are hosted in a different repository. These resources are required for some modules. You can download it from [Indic NLP Resources](https://github.com/anoopkunchukuttan/indic_nlp_resources).

## Usage:
```
git clone https://github.com/VarunGumma/indic_nlp_library.git
git clone https://github.com/anoopkunchukuttan/indic_nlp_resources.git

cd indic_nlp_library
pip install --editable ./
```

## Updates:
- Renamed `master` branch as `main`
