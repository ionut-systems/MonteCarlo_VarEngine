# 📈 Monte Carlo VaR Engine | Application de Bureau Professionnelle d'Analyse des Risques Quantitatifs
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![C++](https://img.shields.io/badge/C++-Standard%20Modern-orange.svg)](https://isocpp.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <img src="images/carlo_var.png" alt="Monte Carlo VaR Engine - Aperçu de l'interface et des rapports" width="100%">
</p>

## 🚀 Vue d'ensemble
**Monte Carlo VaR Engine** est une application de bureau de niveau institutionnel conçue pour les analystes quantitatifs, les gestionnaires de risques et les traders professionnels. Elle combine des calculs mathématiques stochastiques ultra-rapides (**cœur binaire en C++**) avec une interface graphique asynchrone moderne et ergonomique (**frontend Python/Tkinter**).

Pensée pour un déploiement opérationnel immédiat, l'application calcule la **Value at Risk (VaR)** via des simulations avancées de Monte Carlo, normalise dynamiquement les horizons temporels, trace les trajectoires de risque en temps réel et génère instantanément des rapports exécutifs au format **Excel (`openpyxl`)** et **PDF (`reportlab`)**.


#Vidéo explicative du logiciel en fonctionnement:

<p align="center">
  <video src="Monte_carlo_var.mp4" width="100%" controls autoplay muted loop></video>
</p>

---

## 🛠️ Architecture & Stack Technique

```text
┌─────────────────────────┐          Subprocess CLI         ┌─────────────────────────┐
│   Python/Tkinter GUI    │ ──────────────────────────────> │    MonteCarloEngine.exe  │
│   (Multithreaded UI)    │ <────────────────────────────── │   (High-Speed C++ Core) │
└─────────────────────────┘      Stochastic P&L Output      └─────────────────────────┘
             │
             ├─> Matplotlib (Rendu de la distribution des risques en temps réel)
             ├─> Pandas & Openpyxl (États financiers automatisés sous Excel)
             └─> ReportLab (Génération de rapports PDF exécutifs)
