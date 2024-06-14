Lien du site Web:
https://diabete-mellitus.onrender.com/

# Prédiction de la Prévalence du Diabète et de l'Obésité

Ce projet explore la relation entre le diabète, l'obésité et les habitudes de consommation à travers différents pays. En utilisant un modèle LSTM (Long Short-Term Memory), nous visons à estimer la prévalence future du diabète et de l'obésité en fonction des données historiques.

## Table des Matières

- [Introduction](#introduction)
- [Jeu de Données](#jeu-de-données)
- [Utilisation](#utilisation)
- [Fichiers](#fichiers)
- [Modèle](#modèle)
- [Résultats](#résultats)
- [Limites](#limites)

## Introduction

L'augmentation de la prévalence du diabète et de l'obésité est une préoccupation majeure de santé publique dans le monde entier. Ce projet vise à analyser la relation entre les habitudes de consommation alimentaire, les taux de diabète et d'obésité dans différents pays. En appliquant un modèle LSTM, nous prédisons les tendances futures pour aider à la planification et à la mise en œuvre de stratégies de santé publique efficaces.

## Jeu de Données

Le jeu de données comprend des données historiques sur la prévalence du diabète, les taux d'obésité et les habitudes de consommation de divers pays. Les sources de données incluent l'OMS,Our Word in Data, Word Bank Open Data.

## Utilisation

### Utilisation sur Site Web

Lien du site Web:
https://diabete-mellitus.onrender.com/

Site Web départagé entre carte et tableau
Cliquez sur les différents tabs pour avoir des vues différentes

La vue carte dispose de deux cartes, une carte plate et une carte sous forme de globe
Cliquer sur un pays donne un graphique en bas de page, indiquant l'évolution au cours des années
Cliquer sur les différentes années afin d'avoir les résultats pour cette année

### Collecte des Données

Utilisez le script `Scrapping.py` pour collecter et prétraiter les données provenant de diverses sources.

### Entraînement du Modèle

Entraînez le modèle LSTM en utilisant le script `LSTM.py`.

### Application

Exécutez l'application pour visualiser et interagir avec les résultats des prédictions en utilisant le script `app.py`.

## Fichiers

- `Scrapping.py`: Script pour collecter et prétraiter les données.
- `LSTM.py`: Script pour construire, entraîner et évaluer le modèle LSTM.
- `app.py`: Script pour éxecuter l'application de visualisation des prédictions.
- `Procfile`: Fichier pour éxecuter l'application avec Render, l'hébergeur
- `requirements.txt`: Fichier pour indiquer tous les packages à télécharger pour Render, l'hébergeur
- `tous_data.csv`: Le résultat de Scrapping.py, qui nous donne les données scrappées de 2000 à 2021
- `output.csv`: Le résultat de LSTM.py, qui nous donne les données prédites de 2022 à 2031 ajoutées aux données scrappées de 2000 à 2021

## Modèle

Le modèle LSTM est conçu pour gérer les données de séries temporelles et capturer les dépendances à long terme. Il utilise des données historiques sur la prévalence du diabète, les taux d'obésité et les habitudes de consommation pour prédire les tendances futures.


### Hyperparamètres

- Taille du lot: 32
- Époques: 500
-training set :0,8

## Résultats

La performance du modèle est évaluée en utilisant des métriques  telles que l'accuracy. Les résultats indiquent l'efficacité du modèle pour prédire les tendances futures.

## Limites
Le projet était intéressant d'un point de vu scrapping et design d'application, cependant le modèle de prédiction, au vu des résultats de prédictions de 2022 à 2031; n'était pas satisfaisant. Le problème vient sûrement du fait que nous n'avons pas pris en compte tous les facteurs de cause du diabète, nous ne nous sommes limitées qu'aux données simples de diabètes, obésité et surconsommation historique car nous savions que ces données auraient été disponibles en masse.
Ce modèle aurait été plus efficace aussi si nous ne nous concentrions que dans des régions spécifiques, par exemple les continents, nous aurions eu des résultats plus cohérents avec ce procédé.

Afin d'améliorer le projet, il faudrait utiliser plus de caractéristiques facteurs du diabètes, et se concentrer sur les continents ou plus petites régions.
Cependant la limite des données étant leur existence en ligne pour la majorité de pays, c'est pour cela que nous ne nous sommes concentrées que sur le diabète, l'obésité et la surconsommation car ce sont ces données que nous considérions les plus exploitables, accessibles.

