# Toxic-Language-Detection-in-Online-Content
This project attempts to detect and classify toxic content on Twitter. I have used Machine Learning and Natural Language Processing techniques for this purpose. The final classifier is able to classify a tweet on Twitter into three classes -- Hate Speech, Offensive Language and Clean Speech -- with 95.6% accuracy.

## Installation
### Add the src directory to `$PYTHONPATH`

### Install the requirements
- Install the requirements using `pip install -r requirements.txt`
  - Make sure you use Python 3
  - You may want to use a virtual environment for this.
  
## Usage
- Train the model using the `train_model.py` file.
- The model can be evaluated using the `evaluate_model.py` file.
- To classify user input, run the `predict_model.py` file.

## Data files
- The train data is located in the `data/final/train.csv` file.
- The test data is located in the `data/final/test.csv` file.
- Both the training and the testing datasets consists of two columns, `text` and `output_class`.
- The `text` column contains the tweets fetched from Twitter.
- The `output_class` column contains the output class -- 0-hateful, 1-offensive, and 2-clean -- for the corresponding tweet.
