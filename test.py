# -*- coding: utf-8 -*-

import nemex
import collections


def test_nemex():
    E = [
        "kaushik ch",
        "chakrabarti",
        "chaudhuri",
        "venkatesh",
        "surajit ch"
    ]
    D = "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, dong xin, surauijt chadhurisigmod."

    # similarity selection
    similarity = "edit_dist"
    t = 2
    
    # tokenizer settings
    q = 2
    special_char = "_"
    char = True
    unique = False
    tokenizer = nemex.Tokenizer(char, q, special_char, unique).tokenize
    
    # create entities dictionary
    ents_dict = nemex.EntitiesDictionary.from_list(E, tokenizer)
    
    # setup faerie
    pruner = "batch_count"
    faerie = nemex.Faerie(ents_dict, similarity, t, q, pruner)
    
    # run on document to find approximate entities from dictionary
    doc_tokens = tokenizer(D)
    entity2candidates = collections.defaultdict(set)
    verified_only = True
    
    for e, (i, j) in faerie(doc_tokens):
        substring = doc_tokens[i:j+1]
        if char:
            substring = nemex.utils.qgrams_to_char(substring)
        else:
            substring = " ".join(substring)
        entity2candidates[e].add(substring)
    
    for e, candidates in entity2candidates.items():
        if len(candidates) == 0:
            continue
        print("Entity:", ents_dict[e].entity)
        print("----------------------------")
        if char:
            entity = nemex.utils.qgrams_to_char(ents_dict[e].tokens)
        else:
            entity = ents_dict[e].tokens
        for candidate in candidates:
            if not char:
                substring = tokenizer(candidate)
            else:
                substring = candidate
            valid, score = nemex.Verify.check(substring, entity, similarity, t)
            if verified_only:
                if not valid:
                    continue
            print("[{}] {} -- t_true={} {} {}=t_bounded".format(
                valid, candidate, score, "<=" if similarity == "edit_dist" else ">=", 
                t))
        print()


if __name__=="__main__":
    test_nemex()
