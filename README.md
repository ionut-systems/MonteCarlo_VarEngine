# Beezeweb - Monte Carlo VaR Engine (Value-at-Risk Simulator)

Moteur de gestion des risques financiers permettant d'estimer la **Value-at-Risk (VaR)** d'un portefeuille d'investissement par simulations stochastiques de **Monte Carlo**.

## Architecture & Fonctionnalités
* **Génération Stochastique (Mouvement Brownien Géométrique) :** Simulation de milliers de trajectoires de prix aléatoires basées sur la dérive (*drift*) et la volatilité historique de l'actif.
* **Calcul de la Value-at-Risk (95% / 99%) :** Estimation statistique de la perte maximale potentielle d'un capital sur un horizon temporel donné.
* **Conception Orientée Institutionnelle :** Moteur compilé robuste, pensé pour l'audit de risque, le stress-testing de portefeuille et le contrôle d'exposition (Actions, Matières Premières, Devises).

## Exécution
Exécutable autonome sous Windows ou appelable en sous-processus via un cockpit de gestion de portefeuille.

---
*Développé par **Beezeweb** — Ingénierie Quantitative & Automatisation Logicielle.*