#Indic NLP Library

The goal of this project is to build Python based libraries for common text processing and Natural Language Processing in Indian languages. Indian languages share a lot of similarity in terms of script, phonolofy, language syntax, etc. and this library is an attempt to provide a general solution to very commonly required toolsets for Indian language text. 

The library provides the following functionalities: 

- Text Normalization
- Transliteration
- Tokenization

##Text Normalization

Text written in Indic scripts display a lot of quirky behaviour on account of varying input methods, multiple representations for the same character, etc. There is a need to canonicalize the representation of text so that NLP applications can handle the data in a consistent manner. The canonicalization primarily handles the following issues: 

    - Non-spacing characters like ZWJ/ZWNL
    - Multiple representations of Nukta based characters 
    - Multiple representations of two part dependent vowel signs
    - Typing inconsistencies: e.g. use of pipe (|) for poorna virama

You can check the documentation for each normalizer in the file 
`src/normalize/indic_normalize.py` to know the script specific normalizations.    

###Commandline Usage

    python src/indic_nlp/normalize/indic_normalize.py <infile> <outfile> <language> [<replace_nukta>]
    
    <language>: 2-letter ISO 639-1 language code. 
                Codes for some language not covered in the standard
                kK: Konkani
                bD: Bodo
                mP: Manipuri
    <replace_nukta>: True/False. Default: False                

###API Usage

e.g.

    from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
    input_text=u"\u0929 \u0928\u093c"
    remove_nuktas=False
    factory=IndicNormalizerFactory()
    normalizer=factory.get_normalizer("hi",remove_nuktas)
    print normalizer.normalize(input_text)

##Unicode based Transliteration 

Transliterate from one Indic script to another. This is a simple script which exploits the fact that Unicode points of various Indic scripts are at corresponding offsets from the base codepoint for that script. The following scripts are supported:

_Devanagari(Hindi,Marathi,Sanskrit,Konkani,Nepali), Bengali, Oriya, Gujarati, Gurumukhi (Punjabi), Tamil, Telugu, Kannada, Malayalam_

###Commandline Usage

    python src/indic_nlp/transliterate/unicode_transliterate.py <infile> <outfile> <language1> <language2>
    
    <language1>,<language2>: 2-letter ISO 639-1 language code. 
                Codes for some language not covered in the standard
                kK: Konkani
                bD: Bodo
                mP: Manipuri

###API Usage

e.g.

    from indicnlp.transliterate.unicode_transliterate import IndicNormalizerFactory
    input_text=u"\u0929 \u0928\u093c"
    print UnicodeIndicTransliterator.transliterate(input_text,"hi","pa")

##Tokenization 

A trivial tokenizer which just tokenizes on the punctuation boundaries. This also includes punctuations for the Indian language scripts (the purna virama and the deergha virama). It returns a list of tokens   

###Commandline Usage
    python src/indicnlp/tokenize/indic_tokenize.py <infile> <outfile> <language> 
    
    <language>: 2-letter ISO 639-1 language code. 
                Codes for some language not covered in the standard
                kK: Konkani
                bD: Bodo
                mP: Manipuri

###API Usage
e.g.

    from indicnlp.tokenize import indic_tokenize  
    indic_string=u'\u0905\u0928\u0942\u092a,\u0905\u0928\u0942\u092a?\u0964 '
    trivial_tokenize(indic_string)

##Author
Anoop Kunchukuttan ( anoop.kunchukuttan@gmail.com )

##Version: 0.2

##Revision Log
0.2 : 13 Jun 2014: Supports transliteration between Indian languages and tokenization of Indian languages 
0.1 : 12 Mar 2014: Initial version. Supports text normalization.