# 2ème test de partage avec la librairie fastapi

Date : 15/06/25

---

## Déploiement sur docker

### Etape 1 - Fichier requirements.txt et autres fichiers

- Dans le répertoire app où se trouve le fichier principal python, créer également un fichier vice init.py
- Dans le répertoire principal, il doit y avoir :

  - le fichier requirements.txt (saisir dans le terminal : pip freeze > requirements.txt)
  - le fichier README.md (et pourquoi pas ?!?)

- Vérifier qu'il n'y a pas de conflit de librairie en saisissant l'instruction suviante dans le terminal : <br>
  `pip install -r requirements.txt`

### Etape 2 - Test local sur docker

Création du fichier Dockerfile et du fichier .dockerignore dans le répertoire principal :

- Construction du docker sur le local (fastapi-cloud2 -> nom de l'image): <br>
  `docker build -t fastapi-cloud2 .`

- Puis saisir ceci dans le terminal : <br>
  `docker run -p 10000:10000 fastapi-cloud2` <br>
  et saisir ceci dans l'URL d'une page @ pour tester la validité de l'application : <br>
  `http://localhost:10000`

Le dossier .dockerignore évite de d'alimenter l'image docker avec des fichiers "superflux"

### Etape 3 - Déploiement sur Render (avec Docker)

- Se connecter sur [Render](https://render.com/)
- Cliquer "New" → "Web Service"
- Sélectionner le repo GitHub ciblé
- A l'étape config :
  - Langue : Auto détecté (Dockerfile)
  - Plan : Free (gratuit)

### Pour mettre à jour Docker / Render :

- Pour Docker, rebuild à nouveau l'image : <br>
  `docker build -t fastapi-cloud2 .`
- Pour render :
  - Commit à nouveau sur Github le projet modifié
  - Sur render cliquer sur "Manual Deploy" → puis "Deploy latest commit"
