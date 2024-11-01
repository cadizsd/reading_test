# reading_test
# EC2 Instance Setup and Web App Deployment

This README outlines the steps to manually create an EC2 instance, launch the application using a user data script, update the S3 bucket with the latest public IP, and access the web app.

## Steps to Deploy the Web App

### 1. Create EC2 Instance

1. **Log in to the AWS Management Console** and navigate to the EC2 Dashboard.
2. Click on **"Launch Instance."**
3. Choose an **Amazon Machine Image (AMI)**:
   - Select `Amazon Linux 2 AMI (HVM), SSD Volume Type`.
4. Choose an **Instance Type**:
   - Select `t2.micro`.
5. Configure Instance Details:
   - Ensure your VPC and subnet settings are correct.
   - Optionally, enable Auto-assign Public IP.
6. **Add Storage**:
   - Use the default settings or adjust as needed.
7. **Add Tags**:
   - Tag your instance with a name, e.g., `reading_script`.
8. **Configure Security Group**:
   - Create or select a security group that includes rules for:
     - SSH (port 22) from your IP
     - HTTP (port 80) and HTTPS (port 443) for the web application.
     - Include an additional rule for the `readingtracker-http` security group.
9. **Review and Launch**:
   - Review your settings and click on **"Launch."**
   - Select or create a new key pair (e.g., `vockey`) and download the key.

### 2. Use User Data to Launch Application

1. In the **"Configure Instance"** section during launch, find the **"User Data"** field.
2. Paste the contents of your `userdata.sh` script. This script will:
   - Install Git and clone the repository.
   - Set up a Python virtual environment.
   - Install necessary dependencies.
   - Start the Flask application service.

### 3. Retrieve the EC2 Public IP Address

1. Once the instance is running, go to the **Instances** section of the EC2 Dashboard.
2. Select your instance and find the **Public IPv4 address** listed in the instance details.

### 4. Update `index.html` in the S3 Bucket Using Cloud9

1. **Open AWS Cloud9**:
   - Navigate to the Cloud9 service in the AWS Management Console and open your existing environment.
2. **Clone the Repository**:
   - In the Cloud9 terminal, clone your repository with the following command:
     ```bash
     git clone https://github.com/cadizsd/reading_test.git
     ```
3. **Navigate to the Project Directory**:
   - Change to the directory where the repository was cloned:
     ```bash
     cd reading_test
     ```
4. **Edit the `index.html` File**:
   - Open the `index.html` file in the Cloud9 editor and update the relevant line to include the latest public IP address:
     ```html
     <script>
         const server = 'http://<YOUR_PUBLIC_IP>:8080';
     </script>
     ```
   - Replace `<YOUR_PUBLIC_IP>` with the actual public IP you retrieved from the EC2 instance.
5. **Copy the Updated `index.html` to the S3 Bucket**:
   - Use the following command in the Cloud9 terminal to copy the updated file to your S3 bucket:
     ```bash
     aws s3 cp index.html s3://readingtracker-cadiz --acl public-read
     ```

### 5. Access the Web App

You can access the web app using the S3 bucket URL. The URL will typically be in the format:

