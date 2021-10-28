FROM composer:2.1.9 AS build 
# 抄自 https://getcomposer.org/download/
# RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
# RUN php -r "if (hash_file('sha384', 'composer-setup.php') === '906a84df04cea2aa72f40b5f787e49f22d4c2f19492ac310e8cba5b96ac8b64115ac402c8cd292b8a03482574915d1a8') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
# RUN php composer-setup.php
# RUN php -r "unlink('composer-setup.php');"
# RUN mv composer.phar /usr/local/bin/composer
COPY . /zero
RUN cd /zero \
    && composer install

FROM php:7.4-cli
RUN docker-php-ext-configure pcntl --enable-pcntl \
    && docker-php-ext-install pcntl
COPY --from=build /zero /zero
WORKDIR /zero
EXPOSE 8787
EXPOSE 8000
CMD [ "php", "./start.php", "start"]
