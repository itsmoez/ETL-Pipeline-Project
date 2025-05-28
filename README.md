# The Brews Brothers ETL Pipeline for SuperCafe

## Overview
The Brews Brothers ETL Pipeline is developed to support SuperCafe's growing demand for deeper, actionable analytics. This pipeline powers a data dashboard and storage solution that helps SuperCafe track customer behavior, define market trends, and improve customer satisfaction through data-driven insights.

---

## Team Members
- Winston Graham
- Guled Macallin
- Mackenzie Mealy  
- Zubed Chowdhury  
- Mohammed Abanur

---

## Problem Statement
SuperCafe needs to build a more refined data analytics model to:
- Define trends in their market.
- Retain both old and new customers.
- Track customer satisfaction.

---

## Solution
The Brews Brothers ETL Pipeline provides a full-cycle data solution that:
- **Extracts** customer transaction data from CSV files.
- **Cleans and transforms** the data through various transformation steps.
- **Loads** the data into a PostgreSQL database, with plans for future integration with an S3 bucket.
- Powers a centralized **Grafana dashboard** for real-time analytics and insights into customer behavior and market trends.

---

## Competitive Advantage
Compared to generic offerings from competitors like Costa and others, this solution:
- Builds a **custom, scalable data model** tailored specifically for SuperCafe.
- Focuses on **market-specific trends** and customer loyalty strategies.
- Leverages a **flexible ETL pipeline** that supports both local database use and future cloud integration.

---

## 🗂️ Project Sprints
The project follows an Agile methodology, organized into five sprints. Each sprint has a rotating Scrum Master to ensure shared ownership and collaboration.

### 🚀 Sprint 1: Project Kickoff
- Established team norms, meeting structure, and tools for collaboration.
- Agreed upon a shared **Definition of Done (DoD)**.
- Created and reviewed initial acceptance criteria for all Sprint 1 tickets.
- Outlined the architecture and scope for the ETL pipeline.
- Drafted Lucidchart diagrams and set up project folders.  
**Scrum Master:** Mackenzie Mealy

### 🛠️ Sprint 2: Schema & Infrastructure Setup
- Designed a custom database schema to model the client’s transactional data.
- Wrote an SQL script to generate the database schema in PostgreSQL.
- Partially transformed the raw CSV data to align with the new schema.
- Developed a script to orchestrate a network of containers (e.g., Docker/Docker Compose).
- Began implementing utility functions for loading transformed data into the database.  
**Scrum Master:** Guled Macallin

### 🏃 Sprint 3: Infrastructure & Dashboard Integration  
- **Set up EC2 instance via CloudFormation** to host Grafana.
  - Used `userdata` to install Docker and run Grafana as a container.
  - Port 80 mapped to 3000 for web access using HTTP (not HTTPS).
  - Default Grafana admin password changed and stored securely.
  - Created unique Grafana logins for all team members.
- **Connected Grafana to Redshift and CloudWatch** to enable visualization of application and system-level metrics.
  - Used Grafana web interface for configuration.
  - Dashboard configuration exported regularly and committed to the repository for version control.

> **Scrum Master:** Mohammed Abanur
> _Note: Some tasks in this sprint are in progress or partially complete. See “Challenges & Next Actions” for more details._

---

## ✅ Definition of Done (DoD)
The project follows a collaborative **Definition of Done (DoD)** based on group consensus and continuous feedback. A task is considered complete only when it meets the following criteria:

1. **Group Recognition:**  
   The work is reviewed and accepted by the team during a regular catch-up meeting. The team confirms that the task meets the agreed-upon standards and expectations.

2. **Repository Update:**  
   The completed task is committed and pushed to the project repository, ensuring that all changes are reflected in the shared codebase.

3. **Shift Focus:**  
   Once a task is completed, team members are free to shift focus onto the next ticket or task, updating the team on their progress via the team’s chat channel.

4. **Multiple Tickets:**  
   While multiple tickets can be in progress simultaneously, tasks must be finished and fully reviewed before the next one is picked up. This ensures steady progress and attention to detail.

*Note:* This DoD encourages open communication and regular updates to keep the team aligned on priorities and progress.

---

## 🛠️ Tech Stack
This project is built using the following technologies:
- **Python** – For scripting and ETL development.
- **PostgreSQL** – Relational database for storing transformed data.
- **Grafana** – For visualizing key metrics and trends on the dashboard.
- **Lucidchart** – Used to design and visualize the overall ETL pipeline architecture.
- **Docker** – For containerizing the ETL pipeline and database.

---

## 📊 Dashboard
A **Grafana dashboard** will be implemented to visualize key insights from the data, such as:
- Customer satisfaction trends
- Popular products or categories
- Repeat customer rates
- Sales over time  

*Note:* Grafana integration is planned but not yet part of this repository.

---

## 🗂️ Folder Structure
The agreed folder structure for the project is as follows:
- data
- notes
- src

---

## 🏗️ Challenges & Next Actions

### 1. **Queue-based Communication Between Lambdas**
- **Challenge:**  
  The project’s requirements specify using multiple Lambdas with queues between them (e.g., SQS) for decoupled communication. However, our team currently uses a single Lambda for the entire ETL process. This setup does not align with the project’s expected architecture, which leads to a more monolithic structure for the ETL pipeline.
  
- **Next Action:**  
  We need to modify our architecture to incorporate **multiple Lambdas**, each handling a specific stage of the ETL process (Extract, Transform, Load), with **queues (SQS or SNS)** between them for better decoupling. This change will align the project with best practices and make the pipeline more scalable and maintainable.

---

### 2. **SQS Integration Issues**
- **Challenge:**  
  Our team faced technical issues integrating **SQS** with the previous CloudFormation stack. Networking issues arose, preventing the Lambdas from communicating properly through SQS. This has delayed our progress in implementing a more modular ETL architecture.

- **Next Action:**  
  We need to revisit the **CloudFormation setup**, ensuring the correct permissions and networking configurations for **SQS**. If these issues persist, we might consider alternative communication mechanisms like storing Lambda outputs in separate **S3 buckets/folders**, which could trigger subsequent Lambdas.

---
