from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse,HTMLResponse
import uvicorn
import pandas as pd
import pickle
import boto3
import botocore
import os
from pyngrok import ngrok
import nest_asyncio
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

BUCKET_NAME = os.getenv('bucketName')
ACCESS_KEY = os.getenv('accessKey')
SECRET_KEY = os.getenv('secretKey')
NGROK_AUTHTOKEN = os.getenv('ngrockToken')


#Creatig s3 is object, which is getting authrosied through  access keys & secret key to  access the S3 bucket in AWS
s3 = boto3.resource('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key= SECRET_KEY)

# save the filename in KEY variable, which will be downloadd from S3
KEY = 'capstoneClassification.pkl' 

try:
  # we are trying to download file from s3 with name `capstoneClassification.pkl` stored in varaible KEY
  # to colab dir with name `capstoneClassification.pkl`
  s3.Bucket(BUCKET_NAME).download_file(KEY,'capstoneClassification.pkl')

except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise


# Load the model and preprocessing objects
with open('capstoneClassification.pkl', 'rb') as f:
    trained_model = pickle.load(f)
    le = pickle.load(f)
    feature_selected = pickle.load(f)

#preprocessing Encoding function
def encoding(df,le):
    for col in df.columns:
        if df[col].dtypes == 'object':
            name = 'num' + col  # creating heading for that column
            df[name] = le.fit_transform(df[col])  # Column with encoded label is added
            df.drop(col, axis=1, inplace=True)  # column with object type will be removed
    return df

#Prediction function
def prediction_function(xtest):
    ypred = trained_model.predict(xtest)
    return ypred

# Initialize FastAPI app
app = FastAPI()


@app.get("/")
async def read_root():
    homepage=HTMLResponse(content="""
        <html>
            <head>
                <title>Welcome to Network Traffic Classifier</title>
            </head>
            <body>
                <h1>This is a Network Traffic Classifier</h1>
                <form action="/upload/" method="post" enctype="multipart/form-data">
                    <input name="file" type="file">
                    <input type="submit" value="Upload file and Predict">
                </form>
            </body>
        </html>
    """)
    return homepage



@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    
    try:
        input_file = pd.read_csv(file.file)
        #input_file.drop('class', axis=1, inplace=True)
        input_df = input_file.copy()
        
        input_df = encoding(input_df, le)
        input_df_selectedCols = input_df[feature_selected]
        
        # Predict using the trained model
        ypred = trained_model.predict(input_df_selectedCols)
        input_file['IsMalicious'] = ypred
        output_mapping = {0: 'Normal', 1: 'Attack'}
        input_file['class'] = input_file['IsMalicious'].map(output_mapping)

          
        # Save the results to a CSV file
        input_file.to_csv('Prediction.csv', index=False)
    
        # Upload the file to S3
        push_to_s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        push_to_s3.upload_file('Prediction.csv', BUCKET_NAME, 'Prediction.csv')
    
        predictionresponse=HTMLResponse(content=f"""
            <html>
                <head>
                    <title>Network Traffic Classifier</title>
                </head>
                <body>
                    <h2>File Upload and Prediction Result</h2>
                    <p>File "{file.filename}" uploaded and predicted successfully.</p>
                    <p>Top 5 rows of predictions:</p>
                    {input_file.head().to_html()}
                    <p>For complete report, refer to your AWS S3 storage.</p>
                </body>
            </html>
        """)
    
        # Return the predictions in the response
        return predictionresponse
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
    
    
if __name__ == "__main__":

    # Start ngrok and get the public URL
    public_url = ngrok.connect(8000)
    
    print(f"Public URL: {public_url}")

    # Run FastAPI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    


