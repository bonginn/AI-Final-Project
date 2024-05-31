# AI-FInal-Project
## Introduction
This is the final project of Introduction to Artificial Intelligence in National Yang Ming Chiao Tung University. </br>
In these days, there are more and more complex types of news, such as crime, politics, sport, etc. Sometimes we only want to read some news that can let us feel relax, like entertainment, and sometimes, we want to care about some social issues. So, our group decided to develop a "Multi-Label" news classification system.
## Progress
1. Dataset Selection and Preparation. </br>
We select dataset from this [page](https://www.kaggle.com/datasets/timilsinabimal/newsarticlecategories). But this dataset is "Single-Label", so we need to "Re-Label" it. </br>
Some information about this dataset. </br>
![dataset](./Picture/data.png)
2. Training the first BERT model to "Re-Label" our dataset. </br>
3. Training the second BERT model to predict the given description of news. 
## Train Model
You can run file "MultiLabelModel.ipynb" to train the BERT model. It may take a long time for training. After this, you can save .pt file in 'Model'. Or, you can directly download the trained model from [HERE](https://drive.google.com/file/d/15CcUbjFIZtIBTVe6X2kuVq63n4-XgDtA/view?usp=sharing).
## Run
1. Clone our repository to your local machine.
```cpp=
git clone https://github.com/bonginn/AI-FInal-Project
```
2. Install some packages we need.
```cpp=
pip install -r requirements.txt
```
3. Run the demo code.
```cpp=
python3 demo.py
```

