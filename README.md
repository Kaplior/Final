И так. Это мануал по тому как надо запускать всю эту систему. 
Для начала у вас должно быть 2 ec2 инстанции с Amazon linux.
Далее, на одном из них установить nginx и ansible. Эта инстанция будет играть роль как веб сервера, так и основного для ansible.
После чего настраиваем nginx. С помощью команды "nano /etc/nginx/conf.d/flask_app.conf" создаёи файл для конфигурации работы nginx.
Вот что надо прописать внутри этого файла:
server {
    listen 80;
    server_name 13.60.162.154; # поменяёте на ip адрес сервера с nginx

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    location /api/ {
        proxy_pass http://16.171.44.0:5000/; # замените ip адрес, адресом на котором будет контейнер
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        rewrite /api(/.*) /$1 break;  
    }
}

Далее, нам нужно будет настроить наш GitHub Action и Ansible playbook. 
Переходим в директорию /.github/ и мы увидем там две папки: workflows и ansible.
В workflows у нас находится deploy.yml
Он ответчает за все действия которые должны происходить, когда происходит push на ветку main.
В нём мы можем обнаружить несколько важных моментов:
1) Здесь есть строка "run: docker build -t kaplior/final_container:latest ./Docker". Здесь надо заменить kaplior на свой действующий username в Docker hub.
2) Так же у нас есть 5 переменных: DOCKERHUB_USERNAME - ваше имя пользователя в Docker hub, DOCKERHUB_ACCESS_TOKEN - пароль от аккаунта, ANSIBLE_HOST - ip адрес инстанции где находится ansible, ANSIBLE_USER - для Amazon linux это обычно ec2-user, ANSIBLE_PRIVATE_KEY - ваш ключ от этой инстанции.

Далее мы перейдём к папке .github/ansible
Здесь у нас есть 3 файла: db.pem - замените на ключ второй инстанции где будет разворачиваться контейнер, flask_app.yml - это playbook, hosts - а это inventory.

И так, после того как произойдёт push к ветку main, запустится workflow. Он соберёт все файлы из папки Docker в контейнер и после запушит его на Docker hub. После чего все файлы из ansible будут скопированы в папку /home/ec2-user/ansible и после чего будет автоматически запущен.
И перед тем как начать работу, мы должны немного изменить файлы ansible. Внутри hosts измените ip адрес вашего второго хоста [ansible_host], где всё будет разворачиваться:
[amazon_servers]
db_server ansible_host=16.171.44.0 ansible_ssh_private_key_file=/home/ec2-user/ansible/db.pem #так же измените название ключа на ваш.

И теперь можете попробовать запушить изменения внутрь репозитория и для проверки работы всего приложения откройте в браузере ip адрес вашей первой инстанции.
