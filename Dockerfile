# Utilise une image officielle Python
FROM python:3.12-bookworm

ENV TZ=Europe/Paris
ENV PYTHONUNBUFFERED=1

# Définit le répertoire de travail dans le conteneur
WORKDIR /srv/Essaie_Webhook

RUN apt-get update \
 && apt-get install -y vim \
 && rm -rf /var/lib/apt/lists/*

# Copie le fichier requirements.txt AVANT de passer utilisateur non-root
COPY requirements.txt .

# Installe les dépendances avec l'utilisateur root
RUN python -m venv /srv/venv \
 && /srv/venv/bin/pip install --upgrade pip \
 && /srv/venv/bin/pip install -r requirements.txt

 # Crée un utilisateur 'endpoint'
RUN useradd -ms /bin/bash base \
&& mkdir -p /srv/Essaie_Webhook \
&& chown -R base:base /srv

# Passe à l'utilisateur endpoint pour la suite
USER base

# Active le virtualenv dans le bash interactif
RUN echo 'source /srv/venv/bin/activate' >> ~/.bashrc

# Copie le reste du code
COPY . /srv/Essaie_Webhook/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
