Data Structure & Architecture:

Cette section détaille l'organisation des données sources utilisées par Homie pour alimenter le moteur de décision. L'objectif est de fournir un "langage commun" entre les données brutes, les vecteurs d'IA et les filtres de recherche.

1. Format des Données (Mock Data):
   
Les données sont stockées au format JSON dans le fichier mock_data.json. Chaque établissement (restaurant, magasin, boutique, café) suit un schéma strict pour garantir la compatibilité avec Qdrant.

2. Dictionnaire des Payloads:
 
Chaque objet possède les champs suivants, utilisés pour le filtrage et la recommandation :

{
  "id": { "type": "int" },
  "name": { "type": "string", "Role":"Identité de l'établissement", "Possible values":"Ex:Pasta Express" },
  "description":{ "type": "string", "Role":"Base pour l'embedding (IA)", "Possible values":"Texte riche (mots-clés contextuels)"  },
  "price_range": { "type": "string", "Role":"Filtrage par budget", "Possible values":"low, medium, high" }",
  "has_student_promo":{ "type": "boolean", "Role":"Priorisation "Best Value"", "Possible values":"true , false" },
  "location_category": { "type": "string", "Role":"Classification thématique", "Possible values":"food, shop, clothes, cafe" }
}

3. Logique de Validation (Tests Unitaires):

Pour assurer la fiabilité des recommandations, un protocole de test manuel a été appliqué sur les 50 établissements :

*Validation des Promos : Vérification que chaque tag true est justifié par une mention explicite dans la description.

*Cohérence Sémantique : Alignement des descriptions avec le niveau de prix (price_range).

*Qualité Syntaxique : Validation via VS Code pour garantir l'absence d'erreurs d'ID ou de format JSON.


