# voiceClassifier
A module for classifying voice samples. The layout/Class diagram of package is as follows.

![Package Layout](/images/layout.JPG)

## Installation:
Run this command in terminal
```
pip install voiceclassifier
```
This package has dependancy on librosa and other audio related packages. Please check the requirement.txt for further details.

**Please note that this package is extensively tested on Linux enviourment(Ubuntu.)**

## Examples:
Let's have a look at some examples to gain more understanding.

### 1. Trainning on your own data :

* For this you can simply run evaluate.py file from the package if you downloaded zip from github. For this please keep your voice_samples ready. The name of the voice file will be considerd as a class label.Pass list of all your voice_samples path when asked.
![Train Samples](/images/train.png)


* If you have downloaded the package using pip, then you can train as follow...
```
from voiceClassifier import evaluate
evaluate.train(
               ["/home/rshinde/Desktop/data/Shekhar.m4a","/home/rshinde/Desktop/data/Shubham.m4a",
                "/home/rshinde/Desktop/data/Dhruvesh.m4a","/home/rshinde/Desktop/data/Rohit.m4a"]
```

### 2. classifying the voice sample
Herewith the code...

```
from voiceClassifier.voiceClassify import VoiceClassify

vc = VoiceClassify()
# to get classes
print(vc.classes_())

# pass voice_samples for actual prediciton...
prediciton,probabilities,classes_ = vc.predict("/home/rshinde/Desktop/Dhruvesh.wav")
```

Output

```
Audio preprocessed..
(array(['Dhruvesh'], dtype=object),
 array([[0.55461039, 0.05390575, 0.03683959, 0.35464427]]),
 array(['Dhruvesh', 'Rohit', 'Shekhar', 'Shubham'], dtype=object))
 
```



