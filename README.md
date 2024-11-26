Taskmap - Application de Gestion de Tâches




Taskmap est une API Flask qui permet de gérer des utilisateurs et leurs tâches. L'application utilise MySQL comme base de données relationnelle et est entièrement containerisée avec Docker et Docker Compose.



  Fonctionnalités principales

-  Ajouter des utilisateurs à la base de données.
-  Créer, mettre à jour, supprimer et récupérer des tâches associées à un utilisateur.

  Connexion à la base de données via MySQL Connector.


Prérequis
-  Docker
-  Docker Compose



Instructions pour déployer l'application

Les identifiants de connexion et le nom de la base de données utilisés par l'API sont définis dans le fichier docker-compose.yml.


Pour démarrer les conteneurs

```bash
docker-compose up 

API Flask : accessible sur http://localhost:5000
MySQL : accessible sur le port 3306.
