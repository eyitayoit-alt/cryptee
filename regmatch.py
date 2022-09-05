"""
module for regular expression 
public fuction matchFull(),searchPattern(),searchList()
"""
import re

def matchFull(pat,string):
	#function match a pattern with a string return matched string else return none
	return re.fullmatch(pattern,string)
	
def searchPattern(pat,string):
	#function search a pattern in a string return first matched  else return none
	return re.search(pat,string)

def searchListPat(pat:[ ],string:str):
	#function search a list of pattern in a string return valid for matched pattern in the string  else return invalid
	for i in pat:
		matc=re.search(i,string)
		if matc==None:
			return False
	return True

