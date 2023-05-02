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
        # Prints confusion matix for Deep Face face recognition model
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
        # Accuracy = (TP+TN)/(TP+TN+FP+FN)
        accuracy = (tp+tn)/(tp+tn+fp+fn)
        # Precision = TP/(TP+FP)
        precision = tp/(tp+fp)
        # Recall = TP/(TP+FN)
        recall = tp/(tp+fn)
        # F1 Score = 2 * ((Prec * Rec) / (Prec + Rec))
        f1 = 2 * ((precision * recall) / (precision + recall))
        print("DEEPFACE")
        print("                           -Actual-   ")
        print("             __________________________________")
        print("           |          | Face", "| Non-Face ")
        print("           |  ________|______|_________________")
        print("-Predicted-|", "Face    ", "|  " + str(tp) + "  ", "|  " + str(fp))
        print("           |  ________|______|_________________")
        print("           |", "Non-Face", "|  " + str(fn) + "  ", "|  " + str(tn))
        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)
        


    def test2(self):
        # Prints confusion matix for Retina Face face recognition model
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
        accuracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        f1 = 2 * ((precision * recall) / (precision + recall))
        print("RETINAFACE")
        print("                           -Actual-   ")
        print("             __________________________________")
        print("           |          | Face", "| Non-Face ")
        print("           |  ________|______|_________________")
        print("-Predicted-|", "Face    ", "|  " + str(tp) + "  ", "|  " + str(fp))
        print("           |  ________|______|_________________")
        print("           |", "Non-Face", "|  " + str(fn) + "  ", "|  " + str(tn))
        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)

    def test3(self):
        # Prints confusion matix for CLIP classification model
        detect_object = read.parse_input("fact: (DetectObject ?x CLIP ?y)")
        answer_object = self.KB.kb_ask(detect_object)
        all_object = len(answer_object)
        tp = 0
        fn = 0
        fp = 0
        tn = 0
        for i in range(all_object):
            if "nf" in str(answer_object[i]) and "human" in str(answer_object[i]):
                fp += 1
            elif " f" in str(answer_object[i]) and "human" in str(answer_object[i]):
                tp += 1
            elif "nf" in str(answer_object[i]) and "human" not in str(answer_object[i]):
                tn += 1
            else:
                fn += 1
        accuracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        f1 = 2 * ((precision * recall) / (precision + recall))
        print("CLIP")
        print("                           -Actual-   ")
        print("             __________________________________")
        print("           |          | Face", "| Non-Face ")
        print("           |  ________|______|_________________")
        print("-Predicted-|", "Face    ", "|  " + str(tp) + "  ", "|  " + str(fp))
        print("           |  ________|______|_________________")
        print("           |", "Non-Face", "|  " + str(fn) + "  ", "|  " + str(tn))
        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)
    
    def test4(self):
        # Prints confusion matix for face recognition using 3 models and KB inference engine
        detect_face = read.parse_input("fact: (ContainsFace ?image)")
        answer_face = self.KB.kb_ask(detect_face)
        all_face = len(answer_face)
        tp = 0
        fn = 0
        fp = 0
        tn = 0
        face = []
        for i in range(all_face):
            curr = str(answer_face[i]).split(" ")[2]
            face.append(curr)
            if "nf" in curr:
                fp += 1
            else:
                tp += 1
        all = ['f1', 'f2','f3', 'f4','f5', 'f6','f7', 'f8','f9', 'f10',
               'nf1', 'nf2','nf3', 'nf4','nf5', 'nf6','nf7', 'nf8','nf9', 'nf10']
        non_face = []
        for item in all:
            if item not in face:
                non_face.append(item)
        for i in range(len(non_face)):
            if "nf" in non_face[i]:
                tn += 1
            else:
                fn += 1
        accuracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        f1 = 2 * ((precision * recall) / (precision + recall))
        print("ALL MODELS & KB INFERENCE")
        print("                           -Actual-   ")
        print("             __________________________________")
        print("           |          | Face", "| Non-Face ")
        print("           |  ________|______|_________________")
        print("-Predicted-|", "Face    ", "|  " + str(tp) + "  ", "|  " + str(fp))
        print("           |  ________|______|_________________")
        print("           |", "Non-Face", "|  " + str(fn) + " ", "|  " + str(tn))
        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)




if __name__ == '__main__':
    unittest.main()
