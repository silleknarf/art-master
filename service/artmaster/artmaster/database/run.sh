docker stop artmaster-database
docker rm artmaster-database
docker run --name artmaster-database -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql --default-authentication-plugin=mysql_native_password
