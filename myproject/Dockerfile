# Utiliser une image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port sur lequel l'application va fonctionner
EXPOSE 8080

# Commande pour démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "myproject.wsgi:application"]
