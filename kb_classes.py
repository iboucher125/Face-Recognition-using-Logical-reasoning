import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Two types of retract --> from test or recursive call
        # Retract from test --> asserted fact must be false
        if isinstance(fact_or_rule, Fact):
            if fact_or_rule in self.facts:
                curr_fact = self._get_fact(fact_or_rule)
                # Only retract asserted facts
                if curr_fact.asserted:
                    curr_fact.asserted = False
                    # Retract fact if not supported
                    if curr_fact.supported_by == []:
                        self.kb_retract_recursive(curr_fact)

    def kb_retract_recursive(self, fact_or_rule):
        # FACT
        if isinstance(fact_or_rule, Fact):
            if fact_or_rule in self.facts:
                curr_fact = self._get_fact(fact_or_rule)
                # Check if fact supports other facts
                if curr_fact.supports_facts != []:
                    # Loop through each fact that current fact supports
                    for f in curr_fact.supports_facts:
                        # Check if fact is supported by multiple pairs --> just retract pair with matching fact
                        if f.supported_by != []:
                            for pair in f.supported_by:
                                if pair[0] == curr_fact:
                                    f.supported_by.remove(pair)
                                    if f.supported_by == [] and not f.asserted:
                                        # Recursively retract inferred facts (so not asserted facts)
                                        self.kb_retract_recursive(f)
                
                # Check if fact supports other rules
                if curr_fact.supports_rules != 0:
                    # Loop through each rules that current fact supports
                    for r in curr_fact.supports_rules:
                        # Check if rule is supported by multiple pairs --> just retract pair with matching fact
                        if r.supported_by != []:
                            for pair in r.supported_by:
                                if pair[0] == curr_fact:
                                    r.supported_by.remove(pair)
                                    if r.supported_by == [] and not r.asserted:
                                        # Recursively retract inferred facts (so not asserted facts)
                                        self.kb_retract_recursive(r)
                self.facts.remove(curr_fact)

        # RULE
        if isinstance(fact_or_rule, Rule):
            if fact_or_rule in self.rules:
                curr_rule = self._get_rule(fact_or_rule)
                # Check if rule supports other facts
                if curr_rule.supports_facts != []:
                    # Loop through each fact that current rul supports
                    for f in curr_rule.supports_facts:
                        # Check if fact is supported by multiple pairs --> just retract pair with matching fact
                        if f.supported_by != []:
                            for pair in f.supported_by:
                                if pair[1] == curr_rule:
                                    f.supported_by.remove(pair)
                                    if f.supported_by == [] and not f.asserted:
                                        # Recursively retract inferred facts (so not asserted facts)
                                        self.kb_retract_recursive(f)
                
                # Check if rule supports other rules
                if curr_rule.supports_rules != []:
                    # Loop through each rule that current rule supports
                    for r in curr_rule.supports_rules:
                        # Check if rule is supported by multiple pairs --> just retract pair with matching fact
                        if r.supported_by != []:
                            for pair in r.supported_by:
                                if pair[1] == curr_rule:
                                    r.supported_by.remove(pair)
                                    if r.supported_by == [] and not r.asserted:
                                        # Recursively retract inferred facts (so not asserted facts)
                                        self.kb_retract_recursive(r)
                self.rules.remove(curr_rule)


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        self.forward_chain_fact(fact, kb) # Infer fact
        self.forward_chain_rule(rule, kb) # Infer rule

    def forward_chain_fact(self, fact, kb):
        # For each rule in the KB
        for r in kb.rules:
            # Get first statement in lhs of rule
            first_statement = r.lhs[0]
            # Unify fact with first statment in lhs of rule and create possible bindings
            result_bindings = match(fact.statement, first_statement)
            # If substitution found
            if result_bindings != False:
                # If lhs is only one statement
                if len(r.lhs) == 1:
                    # Create new fact using the substiution on rhs
                    new_rhs = instantiate(r.rhs, result_bindings)
                    new_fact = Fact(new_rhs, [[fact, r]])
                    # Add new fact to kb
                    kb.kb_add(new_fact)
                    # Setup support
                    new_fact_from_kb = kb._get_fact(new_fact)
                    fact.supports_facts.append(new_fact_from_kb)
                    r.supports_facts.append(new_fact_from_kb)
                else:
                    # Create new rule with rest of lhs and rhs
                    new_rhs = instantiate(r.rhs, result_bindings)
                    new_lhs = []
                    # Loop through elements on lhs except for first statement
                    for i in range(1, len(r.lhs)):
                        # Instantiate each lhs statement with bindings
                        new_statement = instantiate(r.lhs[i], result_bindings)
                        new_lhs.append(new_statement)
                    
                    # Create new rule
                    new_rule = Rule([new_lhs, new_rhs], [[fact, r]])
                    # Add new rule to the KB
                    kb.kb_add(new_rule)
                    # Setup support
                    new_rule_from_kb = kb._get_rule(new_rule)
                    fact.supports_rules.append(new_rule_from_kb)
                    r.supports_rules.append(new_rule_from_kb)
    
    def forward_chain_rule(self, rule, kb):
        # For each fact in the KB
        for f in kb.facts:
            # Get first statement in lhs of rule
            first_statement = rule.lhs[0]
            # Unify fact with first statment in lhs of rule
            result_bindings = match(f.statement, first_statement)
            # If substitution found
            if result_bindings != False:
                # If lhs is only one statement
                if len(rule.lhs) == 1:
                    # Create new fact using the substiution on rhs
                    new_rhs = instantiate(rule.rhs, result_bindings)
                    new_fact = Fact(new_rhs, [[f, rule]])
                    # Add new fact to kb
                    kb.kb_add(new_fact)
                    # Setup support
                    new_fact_from_kb = kb._get_fact(new_fact)
                    f.supports_facts.append(new_fact_from_kb)
                    rule.supports_facts.append(new_fact_from_kb)
                else:
                    # Create new rule with rest of lhs and rhs
                    new_lhs = []
                    # Loop through elements on lhs except for first
                    for i in range(1, len(rule.lhs)):
                        # Instantiate each lhs statement with bindings
                        new_statement = instantiate(rule.lhs[i], result_bindings)
                        new_lhs.append(new_statement)
                    # Instantiate new rhs
                    new_rhs = instantiate(rule.rhs, result_bindings)
                    # Create new rule
                    new_rule = Rule([new_lhs, new_rhs], [[f, rule]])
                    # Add new rule to the KB
                    kb.kb_add(new_rule)
                    # Setup support
                    new_rule_from_kb = kb._get_rule(new_rule)
                    f.supports_rules.append(new_rule_from_kb)
                    rule.supports_rules.append(new_rule_from_kb)
                    


