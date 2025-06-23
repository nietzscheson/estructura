#### Most of the infrastructure code—such as Terraform modules, Cognito security configurations, and core web/API services—had already been developed and refined across previous projects. For Estructura, the focus was on designing and implementing the /documents and /structures endpoints, along with all the underlying logic and processing layers required to support them.

### While Amazon Textract had also been successfully used in several earlier projects, Estructura emerged from the need to abstract and centralize this logic into a reusable system. The goal was to create a foundation that could power multiple applications through a shared document processing and validation engine.



# Estructura

**Estructura** is a fully serverless document-processing platform built on AWS. It allows users to upload, structure, and validate documents with ease, leveraging modern cloud-native services for scalability and reliability.

![Estructura](./docs/estructura.png?raw=true "Graph of Estructura Project")  
[🎥 Watch Demo Video (Vimeo)](https://vimeo.com/1095638334)

---

## 🚀 Overview

Estructura simplifies structured document processing by offering:

- ✅ User registration and authentication via **AWS Cognito**
- 🔐 Secure APIs via **API Gateway** and **FastAPI**
- 🧾 Document ingestion and validation using **AWS Textract**
- ⚙️ Asynchronous processing with **Lambda** and **SQS**
- 💾 Persistent storage and retrieval via **S3** and **RDS**

---

## 🧱 Architecture

The platform is fully serverless and built entirely on AWS:

### 🧑‍💼 Authentication
- **Amazon Cognito**  
  - User pool management and federated identity
  - Lambda triggers: `PreSignUp` and `PostConfirmation`

### 🌐 API Layer
- **Amazon API Gateway + Lambda (FastAPI)**  
  - Single Lambda hosts the full FastAPI application
  - Routes: `/documents`, `/schemas`, `/structures`, etc.

### 🧾 Document Processing
- **Amazon Textract**  
  - Extracts text and form data from uploaded documents

- **Lambda: Worker Function**  
  - Triggered via **Amazon SQS**
  - Executes post-processing and structured data generation

- **Lambda: Application Layer**  
  - Exposes routes and handles business logic
  - Interacts with **S3**, **RDS**, and the queue

### 🔄 Asynchronous Messaging
- **Amazon SQS**  
  - Acts as a broker between upload and processing
  - Enables retries and scalable throughput

### 🗂️ Storage and Database
- **Amazon S3**: Stores uploaded and structured documents  
- **Amazon RDS (PostgreSQL)**: Stores metadata and schemas

---

## 🛠️ Technologies Used

- [x] FastAPI running on a single AWS Lambda (via API Gateway)
- [x] Docker for packaging Lambda functions
- [x] AWS Cognito, S3, RDS, SQS, Textract
- [x] Infrastructure-as-Code with Terraform
- [x] Pydantic V2 for data validation
- [x] PostgreSQL via Amazon RDS

---

## 📦 Folder Structure

- /core            # FastAPI routes and core logic. Business models and rules
  /infra           # AWS integrations, queues, triggers
  /web             # Webapp Resources.

## ✅ Deployment

Estructura is deployed entirely serverless using:

- AWS Lambda with Docker runtime

- API Gateway V2 for HTTP interface

- Terraform for provisioning resources

- S3 for static document storage

- RDS for transactional data

## 🔐 Security

- Cognito manages user authentication and user pool federation

- Each request is validated via JWT tokens

- Data stored in S3 and RDS is encrypted at rest and in transit

## 🧱 What's Next for Estructura?

We're planning to introduce:

- Multi-tenant support for organization-based access

- Versioned schemas for flexible data evolution

- Real-time validation feedback

- AI/ML-enhanced structure prediction

- Audit logs and activity tracking

## 🧑‍💻 Local Development

# 1. Clone the repo
git clone https://github.com/nietzscheson/estructura.git
cd estructura

# 2. Create a virtual environment
nix develop --impure --command zsh

# 3. Install dependencies
cd core && poetry install --no-root

# 4. Run tests
poetry run pytest -x

📢 Contact

For questions, issues, or collaboration, feel free to open an issue or contact the team at estructura@nietzscheson.dev.