# Transliteration Models for Indian languages
These are models for transliteration involving Indian languages. 
The models are essentially Statistical Machine Translation systems trained using Moses over a
character-level parallel corpora of transliterations. Hence, you will need Moses to use these transliteration models.
The transliteration corpus has itself been mined in an unsupervised fashion from a translation corpus. 

Currently we have trained transliteration models for five language pairs: bn-hi, ta-hi, te-hi, en-hi and mr-hi

Support for transliteration has been introduced in Moses from version 2.1  
So please ensure that you have minimum 2.1 version setup for Moses  

Commands to run the transliteration module using moses

$moseshome/mosesdecoder/scripts/Transliteration/post-decoding-transliteration.pl  \  
--moses-src-dir $moseshome/mosesdecoder --external-bin-dir $moseshome/tools \  
--transliteration-model-dir {path to transliteration model folder} --oov-file {path to file containing oov words, oovs are space separated with each line containing all oovs for the input line}\  
 --input-file {input file to transliterated}  --output-file {output file location} \  
 --input-extension {input language code for eg. en} --output-extension {output language code for eg. hi} --language-model {path to language model} \  
 --decoder $moseshome/mosesdecoder/bin/moses  

A sample execution of the model will be as follows:   

export moseshome={path to moses installation}  
$moseshome/mosesdecoder/scripts/Transliteration/post-decoding-transliteration.pl  \  
--moses-src-dir $moseshome/mosesdecoder --external-bin-dir $moseshome/tools \  
--transliteration-model-dir /home/ratish/project/nlp_resources/indic_nlp_resources/transliterate/en-hi \  
--oov-file /home/ratish/project/translit/input.oov \  
 --input-file /home/ratish/project/translit/input.en  \  
 --output-file /home/ratish/project/translit/output.hi \  
 --input-extension en --output-extension hi --language-model /home/ratish/project/translit/lm/nc.binlm.1 \  
 --decoder $moseshome/mosesdecoder/bin/moses  

So far, we have seen the use of transliteration in a post-editing task for machine translation task.
In case, the models are needed for purely transliteration purpose, the input file and OOV file are the same.  
Sample input file:  
New Delhi is capital of India  
India is worlds seventh largest nation in the World  

OOV file  
New Delhi is capital of India  
India is worlds seventh largest nation in the World  

On running the transliteration module, the output is:  
न्यू डेल्ही इस कैपिटल आफ इंडिया    
इंडिया इस वर्ल्ड सेवंथ लारगेस्ट नेशन इन थे वर्ल्ड   
