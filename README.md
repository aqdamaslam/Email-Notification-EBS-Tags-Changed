### **Monitoring EBS Tag Changes with AWS CloudWatch, Lambda, and SNS**

This document outlines the steps to monitor Amazon Elastic Block Store (EBS) tag changes using AWS CloudWatch, Lambda, and SNS. It includes step-by-step instructions, use cases, and the benefits of implementing this solution.

---

## **1. Overview**

Amazon EBS is a scalable storage service for EC2 instances. Tracking changes to EBS tags is essential for maintaining compliance, auditing changes, and ensuring proper resource management. To monitor EBS tag changes, we can use **AWS CloudTrail** to log API calls, **AWS EventBridge** (formerly CloudWatch Events) to detect changes, and **AWS Lambda** to trigger notifications through **SNS (Simple Notification Service)**.

---

## **2. Use Case**

### **Scenario:**
An organization wants to receive email notifications when EBS tags are modified, created, or deleted. This could be useful for:
- **Security Audits:** Ensure that changes to EBS tags (which may reflect sensitive information or resource categorization) are logged.
- **Compliance Monitoring:** Monitor the usage and changes of EBS tags to stay compliant with internal or regulatory standards.
- **Resource Management:** Keep track of changes to tags used for billing, resource categorization, or ownership.

### **Benefits:**
- **Security & Compliance:** Ensures that any unauthorized or untracked changes to EBS tags are detected.
- **Automation:** Automatically send notifications without manual monitoring.
- **Auditing:** Provides a record of who made changes to tags and when they were made.

---

## **3. Architecture Overview**

### **Components:**
- **AWS CloudTrail:** Tracks the API calls related to EBS tag changes.
- **AWS EventBridge (CloudWatch Events):** Detects the changes based on CloudTrail logs.
- **AWS Lambda:** Processes the event and sends notifications.
- **SNS (Simple Notification Service):** Sends email alerts to specified recipients.

---

## **4. Detailed Steps**

### **Step 1: Enable CloudTrail to Capture EBS Events**

Before proceeding with the notification setup, you must ensure that **CloudTrail** is enabled to capture the necessary events, such as creating, modifying, or deleting EBS tags.

1. Go to the **CloudTrail** service in the AWS Management Console.
2. If you don’t already have a trail set up, create a new trail.
3. Under the **Management Events** section, ensure that **Read/Write Events** is set to capture **All Events** or at least **Write-only Events**.
4. CloudTrail will log API calls such as `CreateTags`, `DeleteTags`, and `ModifyTags` related to EBS volumes.

---

### **Step 2: Create an EventBridge Rule**

Next, you'll set up an EventBridge rule to listen for tag changes on EBS volumes.

1. Go to **Amazon EventBridge** in the AWS Management Console.
2. Click on **Create Rule**.
3. Define the event pattern to capture specific API calls related to tag changes:
   - Select **Event Source**: `AWS API Call via CloudTrail`.
   - Set **Service Name** as `EC2`.
   - Choose **Event Name** as `CreateTags`, `DeleteTags`, or `ModifyTags`.
4. Example event pattern (this pattern captures changes to tags on EBS resources):

5. For the target, select **Lambda Function** and choose the Lambda function you will create in the next step.

---

### **Step 3: Create a Lambda Function**

Now, you need to create a Lambda function that will process the event and send notifications.

1. Go to **AWS Lambda** in the AWS Management Console and click **Create function**.
2. Select **Author from scratch** and choose a runtime (Python or Node.js).
3. In the function code editor, paste the following code:

#### **Explanation:**
- **Logging the event**: `print(f"Received event: {json.dumps(event)}")` logs the event for debugging.
- **Extracting data**: The code uses `event.get('detail', {})` to extract the event details safely. If the key doesn't exist, it defaults to an empty dictionary.
- **Message formatting**: The code prepares a message using details like `resources`, `eventName`, and `userIdentity`.
- **Sending notification**: The `sns_client.publish` function sends the formatted message to the SNS topic.

4. Replace the `TopicArn` with the ARN of your SNS topic (explained in the next step).

---

### **Step 4: Create an SNS Topic**

Next, you'll create an SNS topic and subscribe to it.

1. Go to **Amazon SNS** in the AWS Management Console.
2. Click on **Create topic**, choose **Standard** as the type, and give it a name like `EBS-Tag-Change-Notifications`.
3. After the topic is created, click on **Create subscription**.
4. Choose **Email** as the protocol and provide your email address to receive notifications.
5. Check your email inbox and confirm the subscription by clicking the confirmation link.

---

### **Step 5: Attach Permissions to Lambda**

Ensure that your Lambda function has permission to publish to the SNS topic. To do this:

1. Go to the **IAM** role that Lambda uses (which is created automatically when you create the Lambda function).
2. Attach the policy `AmazonSNSFullAccess` or create a custom policy allowing `sns:Publish` to your SNS topic ARN.

---

### **Step 6: Testing the Setup**

1. Modify or delete a tag on an EBS volume. You can do this through the **EC2 Console** by selecting an EBS volume, going to the **Tags** tab, and adding/removing tags.
2. This will trigger the EventBridge rule and the Lambda function will be executed.
3. Check your email for the notification about the tag change.

---

### **Summary of Key Benefits:**
- **Enhanced Security and Auditing**: Monitoring EBS tag changes helps you track who made modifications, which can be crucial for security audits and compliance.
- **Automation**: This solution removes the need for manual monitoring and ensures automatic notifications when tag changes occur.
- **Improved Resource Management**: By tracking tag modifications, you can ensure that your resources are correctly categorized, and that any changes to billing or ownership tags are promptly reviewed.
- **Scalability**: You can apply this monitoring solution to any number of EBS volumes in your AWS environment, making it scalable for large infrastructures.
