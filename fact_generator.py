import sys


def get_data(data_file, model_name):
    facts = []
    data_file.readline()
    if model_name == "RetinaFace":
        for line in data_file:
            content = line.split(",")
            image = content[0]
            if content[1].strip() == "0":
                fact = "(DetectNonFace " + image + " "+ model_name + ")"
            else:
                fact = "(DetectFace " + image + " "+ model_name + ")"
            facts.append(fact)
    
    if model_name == "CLIP":
        # image, percent, class
        for line in data_file:
            content = line.split(",")
            image = content[0]
            if float(content[1]) > 0.5:
                fact1 = "(GreaterThan50Percent " + image + " " + model_name+ " " + content[2].strip("\n") + ")"
            else:
                fact1 = "(LessThan50Percent " + image + " "+ model_name + " " + content[2].strip("\n") + ")"
            fact2 = "(DetectObject " + image + " "+ model_name + " " + content[2].strip("\n") + ")"
            facts.append(fact1)
            facts.append(fact2)

    data_file.close()

    return facts

def genOutput(data, output_file):
    for item in data:
        output_file.write("fact: " + item + "\n")
    output_file.close()
        

def main():
    # python3 fact_generator.py retina_face.csv RetinaFace facts.txt
    # python3 fact_generator.py CLIP.csv CLIP facts.txt
    intput_file = open(sys.argv[1], 'r',)
    model_name = sys.argv[2]
    output_file = open(sys.argv[3], 'a',)
    data = get_data(intput_file, model_name)
    genOutput(data, output_file)

main()