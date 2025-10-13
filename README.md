# 🧠 Task Management Flask API

A simple task management REST API built with Flask, containerized using Docker, and automated with Jenkins CI/CD.

---

## 🚀 Getting Started

### 📦 Prerequisites

Make sure the following are installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)
- (Optional) Python 3.11+ if running locally without Docker

---

Before Run these Project into Docker you need to run below command First

1) docker build -t jenkins-dind-custom -f infra/Dockerfile.jenkins .

2) docker run -d \
  --name jenkins-dind \
  -p 8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins-dind-custom

## 📁 Project Structure

