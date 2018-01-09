from infoExtract import infoExtract

class sentenceType(InfoExtract):


    def __init__(self,*args, **kwargs):
        super(sentenceType, self).__init__(*args, **kwargs)
        self.post_chunking_corrected = self.get_chunks_corrected()
        self.is_cohort = self.is_cohortative()
        self.is_imper = self.is_imperative()
        self.is_content = self.is_content_quest()
        self.is_yes_no_quest = self.is_yes_no_quest()
        self.is_suggest = self.is_suggestion()
        self.is_poli_cond = self.is_polite_cond()
        self.is_req = self.is_request()
        self.is_important = self.is_important()
        self.keys = self.get_keys()
    def is_cohortative(self):
        search_patts = ['^VP{(^let NP{us})},None',
                        '^ADVP VP{(^let NP{us})},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS VP{(^let NP{us})},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS ADVP? VP{(^let NP{us})},None',]
        return self._check_rules(search_patts)
    def is_imperative(self):
        valid_count = self._check_rule('^VP{^have|hope$},None')
        if valid_count > 0:
            return False

        search_patts = [	
                        '^VP{^VB^^VBG|VB$},None',
                        '^ADVP VP{^VB^^VBG|VB$},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS VP{^VB^^VBG|VB$},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS ADVP? VP{^VB^^VBG|VB$},None',
                        '^VP{^VB$},None',
                        '^ADVP VP{^VB$},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS VP{^VB$},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS ADVP? VP{^VB$},None',
                        '^NP{^NN$},None',
                        '^ADVP NP{^NN$},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS NP{^NN$},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS ADVP? NP{^NN$},None',]

        return self._check_rules(search_patts)

    def is_content_quest(self):

        search_patts = ['^WDT|WP|WPS|WRB|CooC_WRB|CooC_WDT|CooC_WPS|CooC_WP,None']
        return self._check_rules(search_patts)

    def is_yes_no_quest(self):

        search_patts = ['^EX|VP{^do|does|did|am|is|are|was|were|have|has|had},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS EX|VP{^do|does|did|am|is|are|was|were|have|has|had},None',
                        '^VP{^must|would},None',
                        '^ADVP NP? VP{^must|would},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS|ObjectS NP? VP{^must|would},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS|ObjectS ADVP? NP? VP{^must|would},None',]
        return self._check_rules(search_patts)

    def is_suggestion(self):

        search_patts = ['^NP{you|we|I|me|mine|my|us|our|your} VP{^MD},None',
                        'ObjectS NP{you|we|I|me|mine|my|us|our|your} VP{^MD},None',
                        '^VP{^should|shall|might},None',
                        '^ADVP NP? VP{^should|shall|might},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS|ObjectS NP? VP{^should|shall|might},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS|ObjectS ADVP? NP? VP{^should|shall|might},None',]

        return self._check_rules(search_patts)
    def is_polite_cond(self):
        search_patts = ['ConditionalS NP VP{^MD},None',
                        'VP{^MD} ADJP|NP ConditionalS,None']

        return self._check_rules(search_patts)

    def is_request(self):

        search_patts = ['^NP{you|we|I|me|mine|my|us|our|your} VP{want|wanted|wants$},None',
                        'ObjectS NP{you|we|I|me|mine|my|us|our|your} VP{want|wanted|wants$},None',
                        '^VP{^can|could|may},None',
                        '^ADVP VP{^can|could|may},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS VP{^can|could|may},None',
                        'CC|PUNCT|ConsecutiveS|CooC_ConsecutiveS ADVP? VP{^can|could|may},None',]
        return self._check_rules(search_patts)

    def is_important(self):

        bools = {'cohort':self.is_cohort, 'imper':self.is_imper, 'content':self.is_content, 'yes_no':self.is_yes_no_quest, 'suggest':self.is_suggest, 'poli_cond':self.is_poli_cond, 'is_req':self.is_req}

        if any(bools.values()):
            return True

        if self.time_tok_info:
            vals = self.time_tok_info[1].values()
            if len(vals) > 0:


                return True

        if len(self.string.split()) < 4:

            if len(self.role_labelled) == 0:
                self.get_roles()

            """shuttin down on assaf's orders
           tag_counts = _get_tag_count(self.role_labelled)
           if 'ACTION' in tag_counts.keys():
              return True
           """
        return False


    def get_keys(self):
        res = set()
        if self.is_important:
            res.add('important')
        if self.is_cohort:
            res.add('cohort')
        if self.is_imper:
            res.add('imper')
        if self.is_content:
            res.add('content')
        if self.is_yes_no_quest:
            res.add('yes_no')
        if self.is_suggest:
            res.add('suggest')
        if self.is_poli_cond:
            res.add('poli_cond')
        if self.is_req:
            res.add('req')
        return res


    def _check_rules(self,patts):
        for patt in patts:
            if self._check_rule(patt):
                return True
        return False
    def _check_rule(self, search_patt):
        try:
            search_patt = add_brackets(search_patt)
        except AssertionError:
            print "assertion error"
        parsed = parse_rule(search_patt)

        tree1 = TagmaniaTree(parsed)

        modifications, valid_count = validate_groups(tree1.search_patterns, tree1.global_delims,[], self.post_chunking_corrected, {})

        return valid_count
