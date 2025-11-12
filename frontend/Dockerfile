FROM node:20-alpine

WORKDIR /app

# Copia o package.json e o package-lock.json (ou yarn.lock)
COPY package.json ./
COPY package-lock.json ./

# Instala todas as dependências do projeto
RUN npm install

RUN npm install -g react-scripts

# Copia o resto do código da aplicação
COPY . .

# Expõe a porta 3000, padrão do create-react-app
EXPOSE 3000

# Comando padrão para iniciar o servidor de desenvolvimento
CMD ["npm", "start"]