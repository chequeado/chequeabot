# -*- coding: utf-8 -*-
from expresions import temporal_regex, measure_regex
import re
def tag(text, regexes):
    current_tokens = []
    #para cada regex busco los tokens y los agrego
    for regex in regexes:
        reg = re.compile(regex, re.IGNORECASE | re.UNICODE )
        tokens_found = []
        for m in reg.finditer(text):
            tokens_found.append(m.groupdict())
        
        if tokens_found:
            current_tokens += tokens_found   

    max_count = 0
    max_dict = {}
    for token in current_tokens:
        if(len(token.keys()) > max_count):
            max_dict = token

    return max_dict