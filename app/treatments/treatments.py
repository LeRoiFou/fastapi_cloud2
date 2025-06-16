def selected(option1, option2):
    """
    Réponse en type str selon le choix sélectionné par l'utilsateur
    
        :param option1: choix 1 sélectionné par l'utilisateur
        :param option2: choix 2 sélectionné par l'utilisateur
        :return: texte à afficher selon le choix sélectionné par l'utilisateur
    """
    
    if option1:
        return "✅ Correct ! "
    if option2:
        return "❌ Faux !"
    else:
        return "⚠️ Veuillez faire votre choix !"