FROM ubuntu:12.04
ADD https://archive.apache.org/dist/tomcat/tomcat-6/v6.0.30/bin/apache-tomcat-6.0.30.zip /home/
RUN apt-get update && apt-get install -y unzip default-jre wget htop
ADD environment /etc/environment
WORKDIR /home
RUN unzip apache-tomcat-6.0.30.zip
RUN chmod +x apache-tomcat-6.0.30/bin/*.sh
EXPOSE 8080
CMD bash /home/apache-tomcat-6.0.30/bin/startup.sh && htop
