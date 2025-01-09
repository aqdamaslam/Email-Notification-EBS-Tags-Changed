## Setting up Email Notifications for EBS Tag Changes

### **Objective:**
The goal of this setup is to notify administrators via email whenever tags are added, modified, or deleted on Amazon Elastic Block Store (EBS) volumes using AWS CloudWatch Events, Lambda, and SNS.

### **Use Case:**
An organization needs to monitor changes to the tags of its EBS volumes to ensure accurate resource management, cost tracking, and compliance. The administrators want to receive immediate email alerts whenever a tag is created, modified, or deleted on EBS volumes in the AWS environment.

---

### **Overview of the Solution:**

1. **CloudWatch Events (EventBridge)** will be used to capture the API calls related to EBS tag changes (`CreateTags`, `DeleteTags`, `ModifyTags`).
2. **AWS Lambda** will process the event and publish the information to an **SNS topic**.
3. **Amazon SNS (Simple Notification Service)** will send email notifications to subscribed users.

---

### **Step 1: Setting up CloudWatch Events (EventBridge)**

1. **Go to EventBridge:**
   - In the AWS Management Console, navigate to **Amazon EventBridge**.
   - Click on **Rules** in the left sidebar, then click **Create rule**.

2. **Create Event Pattern:**
   - In the **Create Rule** screen, under **Define pattern**, select **Event source** as **AWS events or EventBridge default event bus**.
   - In **Event Pattern**, select the **AWS service** as the event source, and set it to **EC2**.
   - Set the **Event Type** to **AWS API Call via CloudTrail**. This will allow us to capture API calls such as tag modifications.

3. **Configure Event Pattern:**
   - Select **Specific event(s)** and configure the event pattern to look for the EBS tag-related events.
   - The event names you’re interested in are `CreateTags`, `DeleteTags`, and `ModifyTags`:


4. **Select Target for the Rule:**
   - Under **Select targets**, choose **Lambda function**. You’ll later specify the Lambda function that will handle the event and trigger the email notification.

---

### **Step 2: Create an SNS Topic**

1. **Go to Amazon SNS:**
   - In the AWS Management Console, navigate to **Simple Notification Service (SNS)**.
   - Click **Create topic**.

2. **Create Topic:**
   - Choose **Standard** as the topic type.
   - Enter a **Topic Name** (e.g., `EBS-Tag-Change-Notifications`).
   - Click **Create topic**.

3. **Subscribe to Topic:**
   - Once the topic is created, click on the topic ARN (Amazon Resource Name).
   - In the **Subscriptions** section, click **Create subscription**.
   - For **Protocol**, select **Email**.
   - Enter the email address to receive notifications and click **Create subscription**.
   - A confirmation email will be sent to the specified email address. Click the confirmation link to subscribe.

---

### **Step 3: Create a Lambda Function**

1. **Go to AWS Lambda:**
   - In the AWS Management Console, navigate to **Lambda**.
   - Click **Create function**.

2. **Create Lambda Function:**
   - Choose **Author from scratch**.
   - Enter a function name, such as `EBSTagChangeNotificationFunction`.
   - Choose a runtime (Python, Node.js, etc.). Here, we use Python 3.x.
   - Set the **Execution role** to **Create a new role with basic Lambda permissions**.

3. **Write Lambda Function Code:**
   - Below is the Python code to process the event, extract information, and publish it to the SNS topic.

4. **Deploy the Lambda Function:**
   - After writing the code, click **Deploy**.

---

### **Step 4: Set Lambda Permissions**

- Make sure the Lambda function has the necessary permissions to publish messages to the SNS topic.
- Attach the following **IAM policy** to the Lambda execution role (or use a managed policy like `SNSPublish`):

---

### **Step 5: Link Lambda Function to EventBridge Rule**

1. **Go back to the EventBridge Rule** (the rule you created in Step 1).
2. **Add the Lambda Function as the Target**:
   - In the **Target** section, choose **Lambda function** and select the Lambda function created earlier.
   - Save the rule.

---

### **Step 6: Test the Setup**

1. **Modify Tags on EBS Volumes:**
   - To test, modify, create, or delete tags on any EBS volume in your AWS environment.
   
2. **Check the Email:**
   - The Lambda function should trigger when the tags are modified, and the SNS topic will send an email notification to the subscribed email address.

3. **Verify Logs and Notification:**
   - Check the CloudWatch logs for the Lambda function to verify that it’s being triggered and handling the event correctly.
   - Confirm that you received the email notification with the correct information about the EBS tag change.

