from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.treatments.treatments import selected

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
