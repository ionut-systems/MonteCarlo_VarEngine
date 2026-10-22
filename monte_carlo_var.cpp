#include <iostream>
#include <string>
#include <cstdlib>

int main(int argc, char* argv[]) {
    // Vérifier que Python a bien envoyé les 4 arguments (plus le nom du programme)
    if (argc < 5) {
        std::cerr << "Erreur: Paramètres manquants." << std::endl;
        return 1;
    }

    // Récupération des données envoyées par Tkinter
    double capital = std::stod(argv[1]);
    double volatilite = std::stod(argv[2]);
    int horizon = std::stoi(argv[3]);
    int simulations = std::stoi(argv[4]);

    // ... ICI TON MOTEUR DE CALCUL MONTE CARLO ...
    double var_resultat = capital * (volatilite / 100.0) * 1.645; // Exemple de calcul factice

    // Le std::cout est CRUCIAL : c'est ce texte précis que Python va capturer pour l'afficher !
    std::cout << "Simulation terminée (" << simulations << " itérations).\n";
    std::cout << "Value at Risk (99%) : - " << var_resultat << " EUR" << std::endl;

    return 0;
}