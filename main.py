import unittest
import read, copy
from logical_classes import *
from kb_classes import KnowledgeBase

class KBTest(unittest.TestCase):

    def setUp(self):
        # Assert starter facts
        file = 'facts_rules.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)
        
    def test1(self):
        # Produces confusion matrix fro Retina Face
        detect_face = read.parse_input("fact: (DetectFace ?x DeepFace)")
        answer_face = self.KB.kb_ask(detect_face)
        all_face = len(answer_face)
        detect_nonface = read.parse_input("fact: (DetectNonFace ?x DeepFace)")
        answer_nonface = self.KB.kb_ask(detect_nonface)
        all_nonface = len(answer_nonface)
        tp = 0
        fn = 0
        fp = 0
        tn = 0
        for i in range(all_face):
            if "nf" in str(answer_face[i]):
                fp += 1
            else:
                tp += 1
        for i in range(all_nonface):
            if "nf" in str(answer_nonface[i]):
                tn += 1
            else:
                fn += 1
        print("DEEPFACE")
        print("                           -Actual-   ")
        print("             __________________________________")
        print("           |          | Face", "| Non-Face ")
        print("           |  ________|______|_________________")
        print("-Predicted-|", "Face    ", "|  " + str(tp) + "  ", "|  " + str(fp))
        print("           |  ________|______|_________________")
        print("           |", "Non-Face", "|  " + str(fn) + "  ", "|  " + str(tn))

    def test2(self):
        # Produces confusion matrix fro Deep Face
        detect_face = read.parse_input("fact: (DetectFace ?x RetinaFace)")
        answer_face = self.KB.kb_ask(detect_face)
        all_face = len(answer_face)
        detect_nonface = read.parse_input("fact: (DetectNonFace ?x RetinaFace)")
        answer_nonface = self.KB.kb_ask(detect_nonface)
        all_nonface = len(answer_nonface)
        tp = 0
        fn = 0
        fp = 0
        tn = 0
        for i in range(all_face):
            if "nf" in str(answer_face[i]):
                fp += 1
            else:
                tp += 1
        for i in range(all_nonface):
            if "nf" in str(answer_nonface[i]):
                tn += 1
            else:
                fn += 1
        print("RETINAFACE")
        print("                           -Actual-   ")
        print("             __________________________________")
        print("           |          | Face", "| Non-Face ")
        print("           |  ________|______|_________________")
        print("-Predicted-|", "Face    ", "|  " + str(tp) + "  ", "|  " + str(fp))
        print("           |  ________|______|_________________")
        print("           |", "Non-Face", "|  " + str(fn) + "  ", "|  " + str(tn))
    
    def test3(self):
        detect_face = read.parse_input("fact: (ContainsFace ?image)")
        answer_face = self.KB.kb_ask(detect_face)
        all_face = len(answer_face)
        detect_nonface = read.parse_input("fact: (DetectNonFace ?x ?y)")
        answer_nonface = self.KB.kb_ask(detect_nonface)
        all_nonface = len(answer_nonface)
        tp = 0
        fn = 0
        fp = 0
        tn = 0
        for i in range(all_face):
            if "nf" in str(answer_face[i]):
                fp += 1
            else:
                tp += 1
        for i in range(all_nonface):
            if "nf" in str(answer_nonface[i]):
                tn += 1
            else:
                fn += 1
        print("ALL MODELS & KB INFERENCE")
        print("                           -Actual-   ")
        print("             __________________________________")
        print("           |          | Face", "| Non-Face ")
        print("           |  ________|______|_________________")
        print("-Predicted-|", "Face    ", "|  " + str(tp) + "  ", "|  " + str(fp))
        print("           |  ________|______|_________________")
        print("           |", "Non-Face", "|  " + str(fn) + " ", "|  " + str(tn))


def pprint_justification(answer):
    """Pretty prints (hence pprint) justifications for the answer.
    """
    if not answer: print('Answer is False, no justification')
    else:
        print('\nJustification:')
        for i in range(0,len(answer.list_of_bindings)):
            # print bindings
            print(answer.list_of_bindings[i][0])
            # print justifications
            for fact_rule in answer.list_of_bindings[i][1]:
                pprint_support(fact_rule,0)
        print

def pprint_support(fact_rule, indent):
    """Recursive pretty printer helper to nicely indent
    """
    if fact_rule:
        print(' '*indent, "Support for")

        if isinstance(fact_rule, Fact):
            print(fact_rule.statement)
        else:
            print(fact_rule.lhs, "->", fact_rule.rhs)

        if fact_rule.supported_by:
            for pair in fact_rule.supported_by:
                print(' '*(indent+1), "support option")
                for next in pair:
                    pprint_support(next, indent+2)



if __name__ == '__main__':
    unittest.main()
