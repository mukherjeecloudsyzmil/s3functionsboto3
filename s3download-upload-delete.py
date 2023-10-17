from flask import Flask, request, render_template, send_file, redirect, url_for
import boto3

app = Flask(__name__)

# AWS credentials and S3 bucket name
AWS_ACCESS_KEY = 'AKIASXBPOSPPXNK6VMFP'
AWS_SECRET_KEY = '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'
S3_BUCKET = 'sandip-upload-downlaod'

@app.route('/')
def index():
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    # List objects in the S3 bucket
    objects = s3.list_objects(Bucket=S3_BUCKET)

    # Extract the list of filenames
    filenames = [obj['Key'] for obj in objects.get('Contents', [])]

    return render_template('index.html', filenames=filenames)

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

@app.route('/download/<filename>')
def download(filename):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=filename)
        return send_file(response['Body'], as_attachment=True, download_name=filename)
    except Exception as e:
        return str(e)

@app.route('/delete/<filename>')
def delete(filename):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=filename)
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
