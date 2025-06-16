import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from itsdangerous import TimestampSigner, BadSignature
from fastapi.responses import RedirectResponse
import uuid
from app.treatments.treatments import selected

#region enregistrement du cookie de l'utilisateur accédant à l'application

# Constante pour sauvegarder les cookies déjà utilisés
USED_TOKENS_FILE = "used_tokens.json"

# Chargement des tokens utilisés depuis le fichier
if os.path.exists(USED_TOKENS_FILE):
    try:
        with open(USED_TOKENS_FILE, "r") as f:
            used_tokens = set(json.load(f))
    # Si le fichier JSON est vide...
    except (json.JSONDecodeError, ValueError):
        used_tokens = set()
else:
    used_tokens = set()

# Sauvegarde automatique
def save_token(token: str):
    if isinstance(token, bytes):
        token = token.decode()
    used_tokens.add(token)
    with open(USED_TOKENS_FILE, "w") as f:
        json.dump(list(used_tokens), f)
        
#endregion enregistrement du cookie de l'utilisateur accédant à l'application

# Instanciation de la sous-librairie FastAPI
app = FastAPI()

# Instanciation du répertoire et fichiers HTML récupérés
templates = Jinja2Templates(directory='app/templates')

# Récupération du répertoire et des fichiers CSS
app.mount('/static', StaticFiles(directory='app/static'), name='static')

@app.get('/', # URL page par défaut
         response_class = HTMLResponse, # affichage en page HTML
         summary = 'Page par défaut',
         description = """
         Retour page par défaut
         
         param request : requêtes à opérer directement sur le fichier HTML
         """,
         )
async def get_home(request: Request):
    return templates.TemplateResponse(
        'index.html', 
        {'request': request}
        )
    
@app.post('/homer', # URL de la page avec intervention de l'utilisateur
         response_class = HTMLResponse, # affichage en page HTML
         summary = "Affichage de la page avec la réponse selon l'option choisie",
         description = """
         Réponse affichée
         
         param request : requêtes à opérer directement sur le fichier HTML
         arg donuts : choix 1 sélectionné par l'utilisateur
         arg paris : choix 2 sélectionné par l'utilisateur
         """,
         )
async def post_homer(
    request: Request, donuts: bool=Form(False), paris: bool=Form(False)):
    
    # Réponse selon la réponse choisie par l'utilisateur
    response = selected(option1=donuts, option2=paris)
    
    return templates.TemplateResponse(
        'index.html', # Accès au fichier HTML
        {
            'request': request, # requêtes à saisir directement dans le fichier HTML
            'message': response, # message à restituer
        }
        )

#region enregistrement du cookie de l'utilisateur accédant à l'application

# Utilisé pour signer les cookies de façon sécurisée
signatory = TimestampSigner("votre_clé_secrète_changez_moi")

# Stocke les identifiants des utilisateurs déjà vus
used_tokens = set()

@app.middleware("http",)
async def unique_cookie_middleware(request: Request, call_next):
    """
    Permet de créer un cookie unique lorsque l'utilisateur visite pour la
    1ère fois l'application et si le cookie est déjà présent, il bloque l'accès
    à l'utilisateur s'il veut retourner dans l'application et accès limité 24 H
    """
    cookie_token = request.cookies.get("access_token")
    
    if cookie_token:
        try:
            token = signatory.unsign(
                cookie_token, max_age=60*60*24).decode()  # 1 jour de validité
            if token in used_tokens:
                return RedirectResponse(url="/access-denied")
        except BadSignature:
            return RedirectResponse(url="/access-denied")
    else:
        # Création d’un token unique
        token = str(uuid.uuid4())
        signed_token = signatory.sign(token).decode()
        response = await call_next(request)
        response.set_cookie(key="access_token", value=signed_token, httponly=True)
        return response
    
    # Cookie correct mais jamais utilisé → on le marque utilisé en le sauvegardant
    save_token(token)
    response = await call_next(request)
    return response

@app.get("/access-denied", # URL de la page de refus d'accès
         response_class=HTMLResponse, # affichage en page HTML
         )
async def access_denied(request: Request):
    return templates.TemplateResponse("access_denied.html", {"request": request})

#endregion enregistrement du cookie de l'utilisateur accédant à l'application