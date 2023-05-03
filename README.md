# Face_Recognition
## Face Recognition using Logical reasoning
This is our final project for our Artifical Intelligence course (CPS367). Our project involves incorporating an Inference Engine and the Knowledge Base from our earlier Homework assignments into a multi-modal system of object recognition models in order to improve the system’s ability to recognize a human face accurately. Our approach involves inputting the same picture of an object into different pre-trained object recognition models to get predicted labels for that object. Then we will use those ‘labels’ to build our Knowledge Base containing rules indicating if the object is a human face or not.
## Dataset
We created a dataset using the following criteria:
1. Face - faces of humans, all genders, different ages, glasses, masks
2. Non-face - cat, dog, incomplete face (i.e. just a  nose or eye… etc. ), edited images morphing human faces with animal faces
* There are 10 images in each class.
## Recognition Models
Our project utilizes the following object recognition models:
1. CLIP (from OpenAI): Out of a list of classes, this model outputs the top classifications for a given image.
2. RetinaFace: This classifier returns the coordinates of eyes, nose, mouth, and the confidence score.
3. DeepFace: This library performs facial recognition as well as facial attribute analysis (same person?, age, gender, emotion, etc.).
## Components
Recognition Models:
* CLIP: https://colab.research.google.com/drive/1-oraUeUHtXJbXNLI7SuIAXS2t6AZ3teC?usp=sharing 
* RetnaFace: https://colab.research.google.com/drive/1YKyvq6uzP7xiMcX5SiU-gOlSR4xwmzc-?usp=sharing 
* DeepFace: https://colab.research.google.com/drive/1aRN3zi2Zm06efJhbBRvKZpiB2lzS9NIQ?usp=sharing
Fact Genorator:
* fact_generator.py - Produces facts from the output from the recognition models.
Here is an example command to generate facts from the retina_face data:
```
python3 fact_generator.py retina_face.csv RetinaFace facts_rules.txt
```
Facts & Rules:
* facts_rules.txt - File produced by fact_generator.py. Rules used for the inference engine are encluded at the bottom of the file.

Knowldge Base & Inference Engine:
* kb_classes.py
* logical_classes.py
* util.py
* read.py

Testing:
* main.py - Prints the confusion matix for each model and then for the whole multi-modal system.
```
python3 main.py
```


