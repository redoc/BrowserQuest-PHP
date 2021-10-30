FROM composer:2.1.9 AS build 
COPY . /zero
RUN cd /zero \
    && composer install

FROM php:7.4-cli
RUN docker-php-ext-configure pcntl --enable-pcntl \
    && docker-php-ext-install pcntl
COPY --from=build /zero /zero
WORKDIR /zero
CMD [ "php", "./start.php", "start"]
