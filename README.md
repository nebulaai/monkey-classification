# Image Classification

image_classification.ipynb consists of transfer learning with ResNet50

tensorflow 1.13.1 is required (1.13.1 is the default package version on nbai.io as of Dec 2, 2020)



## Dataset

10 Monkey Species: https://www.kaggle.com/slothkong/10-monkey-species

### Install Lib
Install M1 Tensofolow
https://developer.apple.com/metal/tensorflow-plugin/

Install Jupyter Notebook & Pandas
```
conda install -c conda-forge -y pandas jupyter
```



Install M1 opencv
https://blog.roboflow.com/m1-opencv/

`
conda install -c conda-forge opencv
`

Install Python lib

`
pip install matplotlib
pip install pillow
pip install scipy
`

Let’s open a Jupyter Notebook and do the benchmark. In your terminal run

```
jupyter notebook
```

## Running ipynb

Open notebook after login to https://nbai.io

Create folder with name "monkey" in the same directory and unzip the dataset to have the following schema

```
.
├── image_classification.ipynb
└── monkey
    ├── monkey_labels.txt
    ├── training
    │   └── training
    │       ├── n0
    │       ├── n1
    │       ├── n2
    │       ├── n3
    │       ├── n4
    │       ├── n5
    │       ├── n6
    │       ├── n7
    │       ├── n8
    │       └── n9
    └── validation
        └── validation
            ├── n0
            ├── n1
            ├── n2
            ├── n3
            ├── n4
            ├── n5
            ├── n6
            ├── n7
            ├── n8
            └── n9
```


Run the following cell to install pygate_grpc and opencv and restart kernel

```
!pip install pygate_grpc==0.0.14
!pip install opencv-contrib-python==4.1.0.25
```


Tensorflow uses GPU by default if GPU is enabled