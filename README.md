# credit-risk-analysis
Machine learning project for credit risk classification and financial dashboard analysis
# 🏦 Tableau de Bord BI — Gestion Financière & Modélisation des Risques de Crédit

<div align="center">

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Talend](https://img.shields.io/badge/Talend-FF6D70?style=for-the-badge&logo=talend&logoColor=white)

**Projet Business Intelligence — Prédiction des Risques de Crédit**

*Analyse financière complète avec modèle Machine Learning intégré dans Power BI*

</div>

---

## 📋 Table des matières

- [Aperçu du projet](#-aperçu-du-projet)
- [Objectifs](#-objectifs)
- [Architecture technique](#-architecture-technique)
- [Structure des données](#-structure-des-données)
- [Modélisation Power BI](#-modélisation-power-bi)
- [Mesures DAX](#-mesures-dax)
- [Modèle Machine Learning](#-modèle-machine-learning)
- [Structure du tableau de bord](#-structure-du-tableau-de-bord)
- [Installation et configuration](#-installation-et-configuration)
- [Résultats](#-résultats)
- [Technologies utilisées](#-technologies-utilisées)

---

## 🎯 Aperçu du projet

Ce projet implémente un **tableau de bord de gestion financière et de modélisation des risques de crédit** pour une institution bancaire. Il combine l'analyse visuelle avancée dans Power BI avec un modèle de Machine Learning (Random Forest) pour classifier les clients selon leur niveau de risque.

Le pipeline complet va de la base de données MySQL jusqu'aux prédictions en temps réel, en passant par un traitement ETL avec Talend et une modélisation DAX avancée.

### Chiffres clés

| Métrique | Valeur |
|----------|--------|
| Clients analysés | 3 000 |
| Transactions | 2 949 |
| Précision du modèle | 71.83% |
| Pages du dashboard | 6 |
| Mesures DAX | 20+ |
| Algorithme ML | Random Forest |

---

## 🎯 Objectifs

### Objectifs principaux

1. **Analyser les transactions** des clients en fonction de plusieurs critères — produit, région, période — et afficher les performances par rapport aux objectifs fixés

2. **Construire un modèle de prédiction** pour classifier les clients en fonction du risque de crédit (Faible / Modéré / Élevé)

### Indicateurs clés de performance

- Chiffre d'affaires total, nombre de dépôts, retraits, taux de prêt
- Taux de remboursement, variables socio-économiques
- Score de risque composite, probabilité de risque élevé

### Approches analytiques

- Prétraitement des données avec gestion des valeurs manquantes et encodage des variables
- Algorithme Random Forest pour la classification du risque
- Analyse de la précision et visualisation avec matrice de confusion
- Prévisions de transactions basées sur les données historiques

---

## 🏗 Architecture technique

```
┌─────────────────┐     ┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Base MySQL    │────▶│   Talend    │────▶│  Power Query (M) │────▶│    Power BI     │
│   risk_data     │     │   ETL/ELT   │     │  Transformation  │     │  Dashboard +    │
│                 │     │             │     │  + Script Python │     │  Modèle ML      │
└─────────────────┘     └─────────────┘     └──────────────────┘     └─────────────────┘
         │                                           │                        │
         │                                           ▼                        ▼
         │                                   ┌──────────────┐        ┌──────────────┐
         │                                   │ Random Forest│        │ ML_Predictions│
         └──────────────────────────────────▶│  Classifier  │───────▶│  Table Power │
                                             │  scikit-learn│        │     BI       │
                                             └──────────────┘        └──────────────┘
```

### Flux de données

1. **MySQL** → données brutes (clients, transactions, dimensions)
2. **Talend** → ETL initial, nettoyage, chargement
3. **Power Query (M)** → transformations supplémentaires, script Python ML
4. **Power BI** → modélisation DAX, visualisations, dashboard interactif
5. **Actualisation** → toute modification MySQL se propage automatiquement via `Ctrl+Alt+F5`

---

## 🗄 Structure des données

### Schéma de la base de données (Flocon de neige)

```
banking_relationship (1) ──────────────────────┐
         │                                      │
gender (1) ──────────────────────────────────── clients_banking (*) ──── transactions_bank (*)
         │                                      │                                │
investment_advisor (1) ────────────────────────┘                         dim_date (1) ──────┘
                                                │
                                        ML_Predictions (1:1)
```

### Tables

| Table | Lignes | Description | Clé primaire |
|-------|--------|-------------|--------------|
| `clients_banking` | ~3 000 | Profils clients avec données financières complètes | `id_client` |
| `transactions_bank` | ~2 949 | Historique de toutes les transactions | `transactionID` |
| `banking_relationship` | 4 | Types de relation bancaire (Retail, Institutional, Private, Commercial) | `BRId` |
| `gender` | 2 | Référentiel genres | `GenderId` |
| `investment_advisor` | 22 | Conseillers en investissement | `IAId` |
| `dim_date` | Calculée | Table de dates DAX pour Time Intelligence | `Date` |
| `ML_Predictions` | ~3 000 | Prédictions Random Forest par client | `id_client` |

### Colonnes calculées créées

```dax
-- Segmentation démographique
Age_Band = SWITCH(TRUE(), Age<=30, "18-30 ans", Age<=45, "31-45 ans", Age<=60, "46-60 ans", "60+ ans")

-- Catégorie de risque
Risk_Category = SWITCH(TRUE(), Risk_Weighting<=2, "🟢 Faible", Risk_Weighting=3, "🟡 Modéré", "🔴 Élevé")

-- Niveau d'endettement
Niveau_Endettement = 
VAR ratio = DIVIDE(Bank_Loans_Num, Estimated_Income_Num)
RETURN SWITCH(TRUE(), ratio<=1, "Sain", ratio<=3, "Modéré", ratio<=6, "Tendu", "Critique")

-- Score de risque composite
Score_Risque_Composite = 
(Risk_Weighting * 0.4) + (Amount_of_Credit_Cards * 0.1) +
(IF(ratio_dette > 5, 3, IF(ratio_dette > 2, 2, 1)) * 0.3) +
(IF(Properties_Owned = 0, 2, IF(Properties_Owned = 1, 1, 0)) * 0.2)
```

---

## 📊 Modélisation Power BI

### Relations du modèle

| Relation | Cardinalité | Direction filtre |
|----------|-------------|-----------------|
| `banking_relationship` → `clients_banking` | 1 : * | Unique |
| `gender` → `clients_banking` | 1 : * | Unique |
| `investment_advisor` → `clients_banking` | 1 : * | Unique |
| `clients_banking` → `transactions_bank` | 1 : * | Unique |
| `dim_date` → `transactions_bank` | 1 : * | Unique |
| `clients_banking` → `ML_Predictions` | 1 : 1 | Unique |

### Table de dates

```dax
dim_date = 
ADDCOLUMNS(
    CALENDAR(DATE(2013,1,1), DATE(2025,12,31)),
    "Année",        YEAR([Date]),
    "Mois_Num",     MONTH([Date]),
    "Mois_Nom",     FORMAT([Date], "MMMM"),
    "Trimestre",    "T" & QUARTER([Date]),
    "Année_Mois",   FORMAT([Date], "YYYY-MM"),
    "Est_Weekend",  IF(WEEKDAY([Date],2) >= 6, TRUE, FALSE)
)
```

---

## 📐 Mesures DAX

### Mesures financières

```dax
-- Chiffre d'affaires
CA Total = SUMX(clients_banking, clients_banking[Bank_Deposits_Num] + clients_banking[Business_Lending_Num])

-- Transactions
Total Income = CALCULATE(SUM(transactions_bank[Amount_Num]), transactions_bank[Type] = "Income")
Total Expenses = CALCULATE(SUM(transactions_bank[Amount_Num]), transactions_bank[Type] = "Expense")
Net Balance = [Total Income] - [Total Expenses]
Saving Rate % = DIVIDE([Net Balance], [Total Income], 0) * 100

-- Moyennes mensuelles
Avg Monthly Income = 
VAR _ActiveMonths = CALCULATE(DISTINCTCOUNT(dim_date[Année_Mois]), FILTER(transactions_bank, transactions_bank[Amount_Num] > 0))
RETURN DIVIDE([Total Income], _ActiveMonths, 0)
```

### Mesures de risque

```dax
-- Risque
Risque Moyen = AVERAGE(clients_banking[Risk_Weighting])
Taux Risque Élevé = DIVIDE([Clients Risque Élevé], [Nbre Clients], 0)
Taux Remboursement = DIVIDE(SUM(clients_banking[Bank_Deposits_Num]), SUM(clients_banking[Bank_Loans_Num]), 0)

-- Endettement
Clients Endettement Critique = CALCULATE(COUNTROWS(clients_banking), clients_banking[Niveau_Endettement] = "Critique")
Clients Risque Critique = CALCULATE(COUNTROWS(ML_Predictions), ML_Predictions[Probabilité_Risque_Élevé] >= 0.7)
```

### Time Intelligence

```dax
-- Cumuls temporels
Transactions YTD = TOTALYTD(SUM(transactions_bank[Amount_Num]), dim_date[Date])
Transactions MTD = TOTALMTD(SUM(transactions_bank[Amount_Num]), dim_date[Date])

-- Comparaison annuelle
Transactions Année Précédente = CALCULATE(SUM(transactions_bank[Amount_Num]), SAMEPERIODLASTYEAR(dim_date[Date]))
Croissance YoY = DIVIDE(SUM(transactions_bank[Amount_Num]) - [Transactions Année Précédente], [Transactions Année Précédente], 0)
```

---

## 🤖 Modèle Machine Learning

### Algorithme

**Random Forest Classifier** (scikit-learn) exécuté via script Python dans Power Query.

### Paramètres

```python
model = RandomForestClassifier(
    n_estimators=300,      # 300 arbres pour la stabilité
    max_depth=10,          # Limite la profondeur pour éviter le surapprentissage
    random_state=42,       # Reproductibilité
    class_weight='balanced' # Corrige le déséquilibre des classes
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,         # 80% entraînement / 20% test
    random_state=42,
    stratify=y             # Préserve la distribution des classes
)
```

### Variable cible — Risk_Class

| Classe | Code | Risk_Weighting source |
|--------|------|-----------------------|
| Faible | 0 | 1 et 2 |
| Modéré | 1 | 3 |
| Élevé | 2 | 4 et 5 |

### Features utilisées

- **Numériques** : Age, Amount_of_Credit_Cards, Properties_Owned, BRId, GenderId, IAId
- **Monétaires** : Estimated_Income_Num, Bank_Loans_Num, Bank_Deposits_Num, Checking_Accounts_Num, Saving_Accounts_Num, Business_Lending_Num, Credit_Card_Balance_Num, Superannuation_Savings_Num, Foreign_Currency_Num
- **Encodées** : Fee_Structure_enc, Loyalty_Classification_enc, Nationality_enc

### Résultats

| Métrique | Valeur |
|----------|--------|
| Précision globale | **71.83%** |
| Précision classe Faible | 88% |
| Précision classe Modéré | 83% |
| Précision classe Élevé | 83% |

### Matrice de confusion

```
                Prédit Faible  Prédit Modéré  Prédit Élevé
Réel Faible         1 823           210            25
Réel Modéré            51           384            25
Réel Élevé             33            46           403
```

> **Note méthodologique** : Un premier modèle affichait 76% de précision mais souffrait d'un biais de classe — il classifiait quasi systématiquement les clients en risque faible. Après correction avec `class_weight='balanced'` et `stratify=y`, le modèle prédit correctement les 3 niveaux de risque, ce qui est beaucoup plus pertinent pour la détection des clients à risque élevé.

---

## 📱 Structure du tableau de bord

### Pages

| Page | Question centrale | Visuels principaux |
|------|-------------------|-------------------|
| **Vue Exécutive** | Comment se porte la banque globalement ? | 5 KPIs, aires, anneau, barres, carte géo |
| **Transactions Financières** | Combien entre et sort, et comment ça évolue ? | Cartes totaux/moyennes, aires mensuel, YoY |
| **Analyse des Dépenses** | Où va l'argent et qui dépense le plus ? | Treemap, barres catégories, Top 10 clients |
| **Portefeuille Clients** | Qui sont nos clients et lesquels sont risqués ? | Scatter, heatmap, anneau, profils |
| **Risque ML** | Notre modèle est-il fiable et qui surveiller ? | Matrice confusion, importance variables, tableau prédictions |
| **Prévisions** | Que va-t-il se passer et comment réagir ? | Forecast 6 mois, What-If, cohortes, surveillance |

### Filtres disponibles

- Période (Année, Mois)
- Banking Relationship (Retail, Institutional, Private Bank, Commercial)
- Risk Category (Faible, Modéré, Élevé)
- Location (ville)
- Genre (Male, Female)
- Tranche d'âge
- Income Band
- Conseiller en investissement

---

## ⚙️ Installation et configuration

### Prérequis

- Power BI Desktop (version récente)
- Python 3.x via Anaconda
- MySQL Server 8.0+
- Talend Open Studio (pour ETL initial)

### Bibliothèques Python requises

```bash
pip install scikit-learn xgboost matplotlib seaborn pandas numpy
```

### Configuration Power BI

1. **Configurer Python** → Fichier → Options → Script Python → sélectionner le répertoire Anaconda

2. **Désactiver le pare-feu de confidentialité** → Fichier → Options → Confidentialité → Ignorer les niveaux de confidentialité

3. **Activer les cartes géographiques** → Fichier → Options → Sécurité → Utiliser les visuels cartographiques

4. **Connecter MySQL** → Obtenir des données → Base de données MySQL → `localhost` / `risk_data`

5. **Actualiser** → `Ctrl+Alt+F5` pour tout actualiser depuis MySQL

---

## 📈 Résultats

### Performance du modèle

Le modèle Random Forest atteint **71.83% de précision globale** avec une distribution équilibrée sur les 3 classes de risque. Cette précision est considérée comme bonne dans un contexte bancaire avec des données sans historique de paiement ni score de crédit externe.

### Insights métier identifiés

- Les clients avec `Risk_Weighting` 4-5 ont en moyenne **3x plus de prêts** que les clients faible risque
- Les clients avec ancienneté 10+ ans ont un score de risque **40% plus faible** en moyenne
- Le segment **Institutional** génère le CA le plus élevé mais présente un risque modéré
- **34%** du portefeuille présente un risque élevé (Risk_Weighting ≥ 4)

### Recommandations

1. Surveiller en priorité les **33 clients Élevé prédits Faible** (faux négatifs critiques)
2. Alertes automatiques pour clients avec probabilité risque élevé **> 70%**
3. Programme fidélité ciblé sur segment **Modeste Risqué** pour réduire le risque
4. Réviser les conditions de prêt pour les clients en endettement **Critique**

---

## 🛠 Technologies utilisées

| Technologie | Version | Rôle |
|-------------|---------|------|
| Power BI Desktop | Dernière | Modélisation, DAX, visualisation |
| Python (Anaconda) | 3.x | Script ML dans Power Query |
| scikit-learn | Latest | RandomForestClassifier |
| matplotlib / seaborn | Latest | Matrice de confusion |
| pandas / numpy | Latest | Manipulation données |
| MySQL | 8.0 | Base de données source |
| Talend Open Studio | ETL | Extraction et transformation |

---

## 👤 Marissa Ines DJOMO

Projet réalisé dans le cadre d'un cours de Business Intelligence.

---

<div align="center">

*Tableau de bord dynamique — toute modification dans MySQL se propage automatiquement via Power BI en un seul clic Actualiser*

</div>
