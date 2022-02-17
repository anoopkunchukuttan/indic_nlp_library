import itertools
import logging

from util import get_character_set_for_lang, is_ABFN_rule_defined_for_lang
from util import  detect_language
class ABFN :
	"""
	ref :  https://www.unicode.org/L2/L2016/16161-indic-text-seg.pdf
	"""
	
	def is_valid_label(self, text):
		"""
		returns true if text is valid under ABFN rule else false
		"""
		if len(text) == 0:
			logging.debug("text length is zero")
			return False
		
		state =0
		valid = True
		
		lang = detect_language(text)
		character_sets = get_character_set_for_lang(lang)
		
		logging.debug("language : {}  text : {}".format(lang, text))
		
		logging.debug("characters sets: {}".format(str(character_sets)))
		
		if character_sets is None:
			logging.debug("characters set is not defined for the language of text. will return label as invalid label")
			return False
		
		m, v, V, C, symbols, H = character_sets
		
		for ch in list(text):
			
			if not (ch in list(itertools.chain.from_iterable(character_sets))):
				# return false if char not defined in character_set
				logging.debug("character :{} not defined in character set".format(ch) )
				return False
			
			if ch in symbols:
				state = 0
				continue
			
			if ch in C:
				state = 2
				continue
			
			if ch in V:
				state = 1
				continue
			
			if state == 0:
				if ch in v or ch in m or ch in H:
					valid = False
					break
			
			if state == 1:
				if ch in v or ch in H:
					valid = False
					break
				
				if ch in m:
					state = 0
					continue
			
			if state == 2:
				if ch in v:
					state = 3
					continue
				
				if ch in m:
					state = 0
					continue
				
				if ch in H:
					state = 4
					continue
			
			if state == 3:
				if ch in m:
					state = 0
					continue
				
				if ch in v or ch in H:
					valid = False
					break
			
			if state == 4:
				if ch in C:
					state = 2
					continue
				else:
					valid = False
					break
		
		return valid
	
	def tokenize(self, text):
		
		"""
		:param text:
		:return: list of tokens and boolean status if text is valid or not
		"""
		
		if len(text) == 0:
			logging.debug("empty text")
			return []
		
		current_str = ""
		tokens = []
		state = 0
		valid = self.is_valid_label(text)
		
		if not valid:
			logging.debug("not a valid text label")
			raise("invalid text label:{}".format(text))
		
		
		lang = detect_language(text)
		character_sets = get_character_set_for_lang(lang)
		
		logging.debug("language : {}  text : {}".format(lang, text))
		logging.debug("characters sets: {}".format(str(character_sets)))
		
		if character_sets is None:
			logging.debug("characters set is not defined for the language of text. will not tokenize the text")
			raise("characters set is not defined for the language of text:{}".format(text))
		
		m, v, V, C, symbols, H = character_sets
		
		text = list(text)
		for k in range(len(text)):
			
			ch = text[k]
		
			if state != 0 and state != 4 and (ch in C or ch in V or ch in symbols):
				state = 0
			
			if state == 0:
				if len(current_str) > 0:
					tokens.append(current_str)
					current_str = ""
			
			current_str += ch
			
			if state == 0:
				if ch in C:
					state = 2
					continue
			
				if ch in V:
					state = 1
					continue
				
				if ch in symbols:
					state = 0
					continue
			
			if state == 4:
				if ch in C:
					state = 2
					continue
			
			if state == 1:
				
				if ch in m:
					state = 0
					continue
			
			if state == 2:
				if ch in v:
					state = 3
					continue
				
				if ch in m:
					state = 0
					continue
				
				if ch in H:
					state = 4
					continue
			
			if state == 3:
				if ch in m:
					state = 0
					continue
		
		if current_str != "":
			tokens.append(current_str)
			
		logging.debug("tokens : {}".format(tokens))
		return tokens


if __name__ == "__main__":
	s="स्मृतिचिन्ह"
	a= ABFN()
	print(a.tokenize(s))
	
