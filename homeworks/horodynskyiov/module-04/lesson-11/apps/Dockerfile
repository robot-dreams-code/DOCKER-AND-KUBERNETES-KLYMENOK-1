# Базовий образ Node.js
FROM node:20-alpine

# Робоча директорія
WORKDIR /app

# Копіюємо файли
COPY package*.json ./
COPY index.js ./

# Встановлюємо залежності
RUN npm install

# Відкриваємо порт
EXPOSE 8080

# Команда запуску
CMD ["npm", "start"]
