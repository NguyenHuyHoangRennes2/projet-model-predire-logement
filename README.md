# Déterminants du loyer à Rennes

## 1. Introduction

L’accès au logement constitue aujourd’hui un enjeu socio-économique
majeur en France. Dans le cadre d'un contexte représentant une pression
croissante sur le marché de la location, notamment pour les villes ayant
une forte attractivité universitaire comme la ville de Rennes. Les
ménages sont ainsi confrontés à une hausse importante des loyers.

Afin de comprendre comment ceci est arrivé nous avons choisi d'analyser
les facteurs influençant le prix des logements. Ces facteurs sont
essentiels pour analyser les disparités territoriales et éclairer les
décisions prises par les pouvoirs publics.

Pour ce projet, nous chercherons à analyser empiriquement les
**déterminants du loyer charges comprises** des logements situés à
Rennes, en utilisant des données que nous avons collectées
automatiquement par web scraping sur le site *Ouest-France Immo*.
L’étude se concentre sur les logements répartis dans quatre grands
secteurs de Rennes : **Centre**, **Ouest**, **Nord-Est** et
**Nord-Ouest**.

### 1.1 Contexte et problématique

Le marché rennais est particulièrement dynamique en raison de sa
croissance démographique, de son attractivité étudiante et des limites
au sein de son offre locative. Nous nous demanderons donc :

**Quels facteurs structurels expliquent les variations de loyer à Rennes ?**

Cela conduit à examiner l’effet de la surface, du nombre de pièces, des
charges, de la performance énergétique et de la localisation
géographique.

### 1.2 Motivation et intérêt du sujet

Ce travail présente plusieurs intérêts :

- Illustrer une application réelle de la **régression linéaire** à
  partir de données collectées soi-même.
- Analyser les **disparités intra-urbaines** du marché locatif rennais.
- Évaluer l’influence de caractéristiques structurelles ou
  environnementales du logement.
- Proposer un exemple complet de démarche allant de la collecte de
  données au modèle final.

### 1.3 Questions de recherche et hypothèses

Les questions principales sont :

1. La surface influence-t-elle fortement le montant du loyer ?
2. Les charges intégrées modifient-elles significativement le niveau du
   loyer charges comprises ?
3. La performance énergétique joue-t-elle un rôle dans la détermination
   du prix ?
4. Le quartier exerce-t-il un effet propre sur les niveaux de loyer ?

Les hypothèses qui en découlent sont :

- **H1 :** une surface plus élevée entraîne un loyer plus élevé
- **H2 :** des charges plus importantes augmentent le loyer charges
  comprises
- **H3 :** une meilleure performance énergétique est associée à un
  loyer supérieur
- **H4 :** les logements du Centre sont plus chers que ceux des autres
  quartiers.

### 1.4 Objectifs du mémoire

Les objectifs de ce projet sont les suivants :

- Modéliser et expliquer le loyer mensuel charges comprises.
- Identifier les déterminants les plus significatifs.
- Analyser les différences selon les quartiers rennais.
- Proposer une interprétation économétrique rigoureuse.

### 1.5 Plan du document

Nous avons décidé de structurer notre projet de la manière suivante :

- **Section 1 : Introduction**
- **Section 2 : Cadre méthodologique**
- **Section 3 : Analyse descriptive des données**
- **Section 4 : Estimation et interprétation du modèle**
- **Section 5 : Conclusion**

---

## 2. Cadre méthodologique

Cette section présente le modèle économétrique utilisé et les choix
méthodologiques qui ont guidé notre estimation.

### 2.1 Choix méthodologiques : régression linéaire et MCO

Le modèle retenu est une **régression linéaire multiple**. Cette
régression linéaire multiple est estimée à l’aide de la méthode des
**Moindres Carrés Ordinaires (MCO)**. Cette approche permet d’étudier
comment une variable quantitative (dans notre cas de figure, le loyer
charges comprises) dépend de plusieurs caractéristiques propres au
logement.

La méthode MCO consiste à minimiser la somme des carrés des écarts entre
les valeurs observées et celles prédites par le modèle. Cette méthode
est privilégiée pour sa simplicité, son interprétabilité et les
propriétés de ses estimateurs.

### 2.2 Formulation du modèle

La variable expliquée est le **loyer mensuel charges comprises** (en
euros).

Les variables explicatives sont :

- la **surface** du logement (m²),
- les **charges comprises** (euros),
- le **nombre de pièces**,
- la **classe énergétique** (A, B, C, …),
- la **consommation énergétique annuelle** (kWh/an),
- les **émissions de CO₂** (kg/an),
- le **quartier** (Centre, Ouest, Nord-Est, Nord-Ouest).

Le modèle général s’écrit :

```math
\begin{aligned}
\text{Loyer}_i
&= \beta_0
+ \beta_1 \text{Surface}_i
+ \beta_2 \text{Charges}_i\\
&\quad
+ \beta_3 \text{Pièces}_i
+ \beta_4 \text{ClasseÉnergie}_i
+ \beta_5 \text{Consommation}_i
+ \beta_6 \text{ÉmissionsCO2}_i\\
&\quad
+ \sum_q \gamma_q \text{Quartier}_{qi}
+ \varepsilon_i
\end{aligned}
```

où :

- $\beta_0$ est la constante
- $\beta_j$ mesure l’effet marginal de chaque caractéristique
- $\gamma_q$ capture l’effet des quartiers par rapport à un quartier
  de référence
- $\varepsilon_i$ est le terme d’erreur

### 2.3 Justification des choix techniques

Plusieurs éléments motivent ces choix :

- La régression linéaire est un outil adapté pour analyser les
  facteurs influençant une variable économique.
- La méthode MCO fournit des estimateurs robustes et facilement
  interprétables.
- L’utilisation de **variables indicatrices** pour les quartiers
  permet de mettre en évidence les différences géographiques de prix.
- L’intégration des variables énergétiques répond aux enjeux actuels
  de performance environnementale.
- Le modèle permet de mesurer l’effet propre de chaque variable tout
  en contrôlant les autres.

---

## 3. Cadre des données

Les données proviennent du site **Ouest-France Immo**, collectées à
l’aide d’un script de web scraping. Elles décrivent des logements mis en
location au sein de la **ville de Rennes**.

L’étude porte sur **quatre secteurs géographiques** :

- Quartiers Centre
- Quartiers Ouest
- Quartiers Nord-Est
- Quartiers Nord-Ouest

Chaque ligne du jeu de données correspond à **une annonce unique**.
Les variables collectées décrivent :

- Les caractéristiques du logement (surface, nombre de pièces,
  charges)
- Sa performance énergétique (classe, consommation, émissions)
- Sa localisation.
