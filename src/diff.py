from difflib import SequenceMatcher
import os
import fnmatch

MIN_PATTERN_LENGTH=14

def findPattern(fullname1,fullname2):
    filename1,_ = os.path.splitext(fullname1)
    filename2,_ = os.path.splitext(fullname2)

    file_extension=".pdf"

    match = SequenceMatcher(None, filename1, filename2).find_longest_match(0, len(filename1), 0, len(filename2))
    pattern_cont= filename1[match.a: match.a + match.size] 
    pattern_final= '*' + pattern_cont + '*' + file_extension
    print(len(pattern_final))
    if fnmatch.fnmatch(fullname1, pattern_final) & fnmatch.fnmatch(fullname2, pattern_final) & (len(pattern_final) >= MIN_PATTERN_LENGTH) :
        return pattern_final
    else:
        return None


fullname1='JAN2021_AA02793693_TXN.pdf'
fullname2='FEB2021_AA02793693_TXN.pdf'
findPattern(fullname1,fullname2)