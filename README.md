# 🪣 AWS S3 File Uploader using python

A lightweight Python library to upload versioned files to Amazon S3 with progress tracking and pre-signed URL generation, built for managing assistant microservice assets efficiently.

---

## 🚀 Features

- Upload files to Amazon S3 under structured versioned paths
- Validate version format and service name
- Generate pre-signed download links
- Track file upload progress with real-time percentage updates

---

## 📁 Folder Structure on S3

Files are stored in the following hierarchy:

assistant_versions/
└── {assistant_version}/
└── {service_name}/
└── {service_version}/
└── {file_name}



---

## 🔧 Setup

### 1. Clone the Repository


`git clone https://github.com/yourusername/aws-s3-file-uploader.git`
`cd aws-s3-file-uploader `


### 2. Install Dependencies
Make sure you have boto3 and botocore installed:


`pip install boto3 botocore`



### 3. Configure AWS Credentials
Edit the AwsS3 class to include your AWS credentials:

`self.session = boto3.Session(
    aws_access_key_id="your-access-key-id",
    aws_secret_access_key="your-secret-access-key",
)`


Update the S3 bucket name and region if needed:

`self.s3_bucket_name = "your-bucket-name"`
`region_name = "your-region"`



### 🛠️ Usage
#### Upload a File


`s3 = AwsS3()
s3.upload_file(
    file_path="/local/path/to/file",
    assistant_version="1.0.0",
    service_name="assistant",
    service_version="1.0.0"
)`


#### Generate a Pre-signed Download URL
`url = s3.generate_download_link(
    assistant_version="1.0.0",
    service_name="assistant",
    service_version="1.0.0"
)
print(url)`


### 📌 Services Supported
[
    "asr_wav2vec2",
    "chat_gpt_turbo",
    "face_and_emotion_recognizer",
    "jobs",
    "hologram",
    "nlp_bert",
    "noise_suppression",
    "translation",
    "websocket_car_server",
    "question_answering",
]


###  Progress Tracking
When uploading, a percentage progress bar is displayed in the console to show upload status in real-time.

### 🧪 Example Execution
This will attempt to upload files for all supported services under the 1.0.0 version.
`python s3_uploader.py`

### 🛡️ Error Handling
#### FileNotFoundError if the file does not exist locally

#### FileExistsError if the file already exists on S3

#### RuntimeError for invalid version formats or unsupported service names








