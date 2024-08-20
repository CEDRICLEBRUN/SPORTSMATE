# Utiliser une image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY myproject/requirements.txt .
RUN pip install --no-cache-dir -r myproject/requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port sur lequel l'application va fonctionner
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
