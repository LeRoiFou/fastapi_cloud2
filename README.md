# 2ème test de partage avec la librairie fastapi

Date : 15/06/25 <br>
Editeur : Eluan T.

---

**Déploiement sur docker**

### Etape 1 - Test local sur docker

Construction du docker sur le local : <br>
`docker build -t fastapi-cloud2 .`

Puis saisir ceci dans le terminal : <br>
`docker run -p 10000:10000 fastapi-cloud2` <br>
et saisir ceci dans l'URL d'une page @ pour tester la validité de l'application : <br>
`http://localhost:10000`
