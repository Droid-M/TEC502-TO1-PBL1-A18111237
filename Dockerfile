# Use uma imagem oficial do PHP com a versão 8.1.17
FROM php:8.1.17-fpm

# Instale extensões do PHP que seu projeto precisa
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Defina o diretório de trabalho no container
WORKDIR /var/www/html

# Defina as permissões corretas para os arquivos
RUN chown -R www-data:www-data /var/www/html

# Copie os arquivos do seu projeto para o diretório de trabalho no container
COPY . /var/www/html
COPY ./php /var/www/html
COPY ./php .

# Exponha a porta 9000 para o PHP-FPM
EXPOSE 9000

# Comando para iniciar o PHP-FPM
CMD ["php-fpm"]
