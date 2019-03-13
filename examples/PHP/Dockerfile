FROM ubuntu:12.04
RUN apt-get update && apt-get install -y build-essential apache2 apache2-dev libxml2 libxml2-dev htop
ADD http://museum.php.net/php5/php-5.3.8.tar.gz /home/
WORKDIR /home
RUN tar -xzf php-5.3.8.tar.gz
WORKDIR php-5.3.8
RUN ./configure --with-apxs2=/usr/bin/apxs2
RUN make
RUN make install
COPY post.php /var/www/post.php
RUN service apache2 restart
EXPOSE 80
CMD service apache2 restart && htop
