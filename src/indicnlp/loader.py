# Copyright Anoop Kunchukuttan 2014 - present
#
# This file is part of Indic NLP Library.
# 
# Indic NLP Library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Indic NLP Library is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
# 
#        You should have received a copy of the GNU General Public License
#        along with Indic NLP Library.  If not, see <http://www.gnu.org/licenses/>.

from indicnlp import common
from indicnlp.script import indic_scripts
from indicnlp.script import english_script

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


