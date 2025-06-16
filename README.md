# 2ème test de partage avec la librairie fastapi

Date : 15/06/25

---

## Déploiement sur docker

### Etape 1 - Test local sur docker

Construction du docker sur le local (fastapi-cloud2 -> nom de l'image): <br>
`docker build -t fastapi-cloud2 .`

Puis saisir ceci dans le terminal : <br>
`docker run -p 10000:10000 fastapi-cloud2` <br>
et saisir ceci dans l'URL d'une page @ pour tester la validité de l'application : <br>
`http://localhost:10000`

### Etape 2 - Déploiement sur Render (avec Docker)

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
