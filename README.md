# classification_networkintrusiondetection
Classification model to detect network intrusion

### The dataset used : KDD Cup 1999 Dataset for Network Intrusion Detection
http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html

### Network Intrusion Detection Using KDD Cup 1999 Dataset

**Introduction**:
The KDD Cup 1999 dataset is used to build and evaluate machine learning models for detecting network intrusions. It includes both normal and attack traffic data.
Objective is to create and train model to classify if given network traffic is normal or it is an network attack.

**Dataset Details**:
  - Dataset is avaiable in AWS S3 bucket.
  - Contains around 5 million records with 41 features each.
  - Features include network connection details, such as duration, protocol type, and service type.

**Preprocessing**:
  - read s3 and downloaded the dataset in colab environment
  - Considering it is an demo project selected 1% of dataset ie 500K rows to create model
  - Balanced the dataset ot have equivalnt number of normal and attack type data so the model should be biased.
  - Used label encoding to convert categorical features to numerical values.
  - Selected important features to improve model performance.
  - 

 **Model Development**:
  - Built classfier using Decision Tree, Random forest and XGB  with default & hyperparmeter tuned models, to identify network intrusions.
  - Using F1 score compared the model output and picked up best performing model
  - This created a baseModel. Saved/pickled this model back to S3
  

 **Testing 1**:
  - Read and load the pickeled model and test file from S3
  - Preprocess the input
  - Inferecnce baseModel with preprocessed input
  - Evaluated the model using accuracy, precision, recall, and F1-score.
  - Used cross-validation to ensure the model's robustness.

  
 **Deployment**:
   - Deployed Model to Ngrock server using fastAPI.
