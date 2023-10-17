from flask import Flask, request, render_template
import boto3

app = Flask(__name__)

# AWS credentials and S3 bucket name
AWS_ACCESS_KEY = 'AKIASXBPOSPPXNK6VMFP'
AWS_SECRET_KEY = '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'
S3_BUCKET = 'sandip-upload-downlaod'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    s3.upload_fileobj(file, S3_BUCKET, file.filename)

    return "File uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)
