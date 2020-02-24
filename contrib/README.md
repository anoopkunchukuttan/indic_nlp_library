# Contrib

Contains additional utilities and applications using Indic NLP library core

- `indic_scraper_project_sample.ipynb`: A simple pipeline for building monolingual corpora for Indian languages from crawled web content, Wikipedia, etc. An extensible framework which allows incorporation of website specific extractors, whereas generic NLP tasks like tokenization, sentence splitting, normalization, etc. are handled by the framework.
- `correct_moses_tokenizer.py`: This script corrects the incorrect tokenization done by Moses tokenizer.  The Moses tokenizer splits on nukta and halant characters.
- `hindi_to_kannada_transliterator.py`: This script transliterates Hindi to Kannada. It removes/remaps characters only found in Hindi. It also adds halanta to words ending with consonant - as is the convention in Kannada.
