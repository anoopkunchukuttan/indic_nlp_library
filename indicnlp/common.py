# 
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#  
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
# 

import os

"""
Path to the Indic NLP Resources directory
"""
INDIC_RESOURCES_PATH=''

def init():
    """
    Initialize the module. The following actions are performed:

    - Checks of INDIC_RESOURCES_PATH variable is set. If not, checks if it can beb initialized from 
        INDIC_RESOURCES_PATH environment variable. If that fails, an exception is raised
    """
    global INDIC_RESOURCES_PATH 
    try: 
        if INDIC_RESOURCES_PATH=='':
            INDIC_RESOURCES_PATH=os.environ['INDIC_RESOURCES_PATH']
    except Exception as e: 
        raise IndicNlpException('INDIC_RESOURCES_PATH not set')

    if INDIC_RESOURCES_PATH=='': 
        raise IndicNlpException('INDIC_RESOURCES_PATH not set')



def get_resources_path(): 
    """
        Get the path to the Indic NLP Resources directory
    """
    return INDIC_RESOURCES_PATH

def set_resources_path(resources_path): 
    """
        Set the path to the Indic NLP Resources directory
    """
    global INDIC_RESOURCES_PATH 
    INDIC_RESOURCES_PATH=resources_path

class IndicNlpException(Exception):
    """
        Exceptions thrown by Indic NLP Library components are instances of this class.  
        'msg' attribute contains exception details.
    """
    def __init__(self, msg):
        self.msg = msg 

    def __str__(self):
        return repr(self.msg)

