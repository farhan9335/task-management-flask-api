FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install -y kubectl

USER jenkins
