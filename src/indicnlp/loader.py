# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

from indicnlp import common
from indicnlp.script import indic_scripts
from indicnlp.script import english_script
from indicnlp.transliterate import unicode_transliterate

def load():
    """
        Initializes the Indic NLP library. Clients should call this method before using the library. 

        Any module requiring initialization should have a init() method, to which a call must be made from this method 
    """

    ### Order of intialization may matter 

    # Common has to be loaded first to get access to resources 
    common.init()

    ## Initialization of Indic scripts module 
    indic_scripts.init()

    ## Initialization of English scripts module 
    english_script.init()

    ## Initialization of unicode_transliterate module 
    unicode_transliterate.init()


