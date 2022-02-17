from character_set import symbols
import logging

import character_set

def detect_language(text):
	"""
	simple language identifier. If word contains character from multiple languages. 
	function returns language type of first non symbol character. if character is not defined then return None.
	"""
	symbol_present = False
	for c in list(text):
		if c in symbols:
			symbol_present=True
			continue
		else:
			if "ऀ" <= c <= "ॿ":
				return "HI"
			
			if "ঀ" <= c <= "৾":
				return "BN"
			
			if "ઁ" <= c <= "૿":
				return "GU"
			
			if "ਁ" <= c <= "੶":
				return "GUR"
			
			if "ஂ" <= c <= "௺":
				return "TA"
			
			if "ఀ" <= c <= "౿":
				return "TE"
			
			if "ಀ" <= c <= "೯":
				return "KN"
			
			if "ഀ" <= c <= "ൿ":
				return "ML"
			
			if "ଁ" <= c <= "୷":
				return "OR"
			
			if "؀" <= c <= "ۿ":
				return "AR"
			
			if "!" <= c <= "~":
				return "EN"
	
	if symbol_present:
		logging.debug("only symbols present in text:{}. returning language type as english".format(text))
		return "EN"
	
	if len(text) ==0 :
		logging.debug("text length is zero will return None value")
		return None
	
	logging.debug("Language not defined for text:{}".format(text))
	return None

def is_ABFN_rule_defined_for_lang(lang):
	return get_character_set_for_lang(lang) is not None

def get_character_set_for_lang(lang):

	if lang == "HI":
		return (character_set.HI_m, character_set.HI_v, character_set.HI_V, character_set.HI_C, \
		        character_set.HI_symbols, character_set.HI_H)
	
	if lang == "GUR":
		return (character_set.GUR_m, character_set.GUR_v, character_set.GUR_V, character_set.GUR_C, \
		        character_set.GUR_symbols, character_set.GUR_H)
	if lang == "GU":
		return (character_set.GU_m, character_set.GU_v, character_set.GU_V, character_set.GU_C, \
		        character_set.GU_symbols, character_set.GU_H)
	
	if lang == "BN":
		return (character_set.BN_m, character_set.BN_v, character_set.BN_V, character_set.BN_C, \
		        character_set.BN_symbols, character_set.BN_H)
	
	if lang == "TE":
		return (character_set.TE_m, character_set.TE_v, character_set.TE_V, character_set.TE_C, \
		        character_set.TE_symbols, character_set.TE_H)
	
	if lang == "TA":
		return (character_set.TA_m, character_set.TA_v, character_set.TA_V, character_set.TA_C, \
		        character_set.TA_symbols, character_set.TA_H)
	
	if lang == "ML":
		return (character_set.ML_m, character_set.ML_v, character_set.ML_V, character_set.ML_C, \
		        character_set.ML_symbols, character_set.ML_H)
	
	if lang == "KN":
		return (character_set.KN_m, character_set.KN_v, character_set.KN_V, character_set.KN_C, \
		        character_set.KN_symbols, character_set.KN_H)
	
	if lang == "OR":
		return (character_set.OR_m, character_set.OR_v, character_set.OR_V, character_set.OR_C, \
		        character_set.OR_symbols, character_set.OR_H)
	
	logging.debug("ABFN rules not defined for language: {}. function will return None value".format(lang))
	return None



#Next 3 functions are used to convert character range to character set.
def print_unicode_characters_in_range(a, b):
	s = ""
	ch = a
	while (ch <= b):
		s += ch
		s += " "
		# print(ch, end=" ")
		ch = chr(ord(ch) + 1)
	
	return s
def get_unicode_value(ch):
	return ord(ch)
def print_in_range(xx):
	str = ""
	for x in xx:
		if "." in x:
			s = x.replace(".", "")
			s = [s[:4], s[4:]]
			s[0] = chr(int(s[0], 16))
			s[1] = chr(int(s[1], 16))
		else:
			s = []
			s.append(chr(int(x, 16)))
			s.append(chr(int(x, 16)))
		
		str += print_unicode_characters_in_range(s[0], s[1])
	print("")
	print(str)

# print charcters not defined in abfn character set. e.g : unicode values for which character is not defined.
def print_unused_char(a, b , lang):
	m , v, V, C, symbols , H = get_character_set_for_lang(lang)
	ch = a
	while (ch <= b):
		if ch not in (m + v+ V+ C+ symbols + H):
			print(ch, end=" ")
		ch = chr(ord(ch) + 1)
