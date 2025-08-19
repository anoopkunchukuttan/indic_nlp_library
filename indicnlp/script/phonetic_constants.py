import numpy as np

# Start offset for the phonetic feature vector in the phonetic data vector
PHONETIC_VECTOR_START_OFFSET = 6

# Default length of phonetic vector, can be updated by specific script modules
DEFAULT_PHONETIC_VECTOR_LENGTH = 38

# PHONETIC PROPERTIES in order in which they occur in the vector
# This list must be in sync with the keys in the PV_PROP_RANGES dictionary
PV_PROP = [
    "basic_type",
    "vowel_length",
    "vowel_strength",
    "vowel_status",
    "consonant_type",
    "articulation_place",
    "aspiration",
    "voicing",
    "nasalization",
    "vowel_horizontal",
    "vowel_vertical",
    "vowel_roundness",
]

# Bit vector ranges for various properties
PV_PROP_RANGES = {
    "basic_type": [0, 6],
    "vowel_length": [6, 8],
    "vowel_strength": [8, 11],
    "vowel_status": [11, 13],
    "consonant_type": [13, 18],
    "articulation_place": [18, 23],
    "aspiration": [23, 25],
    "voicing": [25, 27],
    "nasalization": [27, 29],
    "vowel_horizontal": [29, 32],
    "vowel_vertical": [32, 36],
    "vowel_roundness": [36, 38],
}

# Indexes into the Phonetic Vector
PVIDX_BT_VOWEL = 0
PVIDX_BT_CONSONANT = 1
PVIDX_BT_NUKTA = 2
PVIDX_BT_HALANT = 3
PVIDX_BT_ANUSVAAR = 4
PVIDX_BT_MISC = 5
PVIDX_BT_S = PVIDX_BT_VOWEL
PVIDX_BT_E = PVIDX_BT_MISC + 1

PVIDX_VSTAT_DEP = 12


def get_invalid_vector(current_phonetic_vector_length):
    """
    Returns a zero vector of the specified length, representing an invalid phonetic vector.
    """
    return np.array([0] * current_phonetic_vector_length)
