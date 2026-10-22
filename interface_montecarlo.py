import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import threading
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def quitter_application():
    """ Fonction pour quitter l'application proprement """
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?"):
        root.destroy()

def exporter_rapport_bancaire():
    try:
        data = {
            "Indicateur / Paramètre": [
                "Capital Initial (€)", 
                "Volatilité Annuelle (%)", 
                "Horizon de Temps", 
                "Nombre de Simulations", 
                "Résultat - Value at Risk (VaR)"
            ],
            "Valeur": [
                entry_capital.get(),
                entry_volat.get(),
                f"{entry_horizon.get()} {combo_unite.get()}",
                entry_sim.get(),
                label_resultat.cget("text")
            ]
        }
        
        df = pd.DataFrame(data)
        
        fichier = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")],
            title="Exporter le Rapport Excel"
        )
        
        if fichier:
            df.to_excel(fichier, index=False, engine='openpyxl')
            messagebox.showinfo("Export Réussi", f"Le relevé financier Excel a été généré avec succès :\n{fichier}")
            
    except Exception as e:
        messagebox.showerror("Erreur d'export Excel", f"Impossible de générer le fichier : {e}")

def exporter_rapport_pdf():
    try:
        fichier = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")],
            title="Exporter le Rapport PDF Institutionnel"
        )
        
        if fichier:
            doc = SimpleDocTemplate(fichier, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1B4F72'),
                spaceAfter=15,
                alignment=1
            )
            
            story.append(Paragraph("RAPPORT DE RISQUE - MONTE CARLO VaR", title_style))
            story.append(Spacer(1, 10))
            
            details = [
                f"<b>Capital Initial :</b> {entry_capital.get()} €",
                f"<b>Volatilité Annuelle :</b> {entry_volat.get()} %",
                f"<b>Horizon de Temps :</b> {entry_horizon.get()} {combo_unite.get()}",
                f"<b>Nombre de Simulations :</b> {entry_sim.get()}",
                f"<b>Résultat Clé :</b> {label_resultat.cget('text')}"
            ]
            
            for line in details:
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 8))
                
            doc.build(story)
            messagebox.showinfo("Export Réussi", f"Le rapport PDF institutionnel a été généré avec succès :\n{fichier}")
            
    except Exception as e:
        messagebox.showerror("Erreur d'export PDF", f"Impossible de générer le PDF : {e}")

def afficher_resultat(resultat_brut, capital, horizon_jours):
    """ Met à jour l'interface graphique et le tracé avec les résultats du calcul """
    label_resultat.config(
        text=resultat_brut, 
        fg="#1B4F72",
        bg="#EBF5FB",
        font=("Arial", 10, "bold"),
        relief="groove",
        bd=2,
    )

    ax.clear()
    ax.set_title("Distribution des P&L & Trajectoires VaR (99%)", fontsize=8, color="#1B4F72", fontweight='bold')
    ax.plot([0, horizon_jours*0.25, horizon_jours*0.5, horizon_jours], [float(capital), float(capital)*1.02, float(capital)*0.98, float(capital)*0.95], color="#D32F2F", linewidth=2, label="Trajectoire type")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc="upper right", fontsize=7)
    canvas.draw()

    # Affichage du bloc contenant les deux boutons distincts (Excel & PDF)
    frame_exports.pack(pady=5)

def lancer_simulation():
    """ Exécute la simulation stochastique en arrière-plan (Multithreading) """
    btn_run.config(state=tk.DISABLED)  
    label_resultat.config(text="Calcul stochastique en cours...", fg="#D35400", bg="#F4F6F9", font=("Arial", 10, "bold"), relief="flat")

    try:
        valeur_horizon = float(entry_horizon.get())
        unite = combo_unite.get()

        if unite == "Mois":
            horizon_jours = int(valeur_horizon * 30)
        elif unite == "Années":
            horizon_jours = int(valeur_horizon * 365)
        else:
            horizon_jours = int(valeur_horizon)
    except ValueError:
        messagebox.showerror("Erreur de saisie", "Veuillez entrer une valeur numérique valide pour l'horizon.")
        btn_run.config(state=tk.NORMAL)
        return

    def worker():
        try:
            capital = entry_capital.get()
            volatilité = entry_volat.get()
            simulations = entry_sim.get()
            chemin_exe = "./MonteCarloEngine.exe" 
        
            resultat_brut = subprocess.check_output(
                [chemin_exe, capital, volatilité, str(horizon_jours), simulations], 
                text=True
            )
            
            root.after(0, lambda: afficher_resultat(resultat_brut, capital, horizon_jours))

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Erreur Moteur", f"Vérifiez que le fichier MonteCarloEngine.exe est présent.\nDétail : {e}"))
        finally:
            root.after(0, lambda: btn_run.config(state=tk.NORMAL))  

    threading.Thread(target=worker, daemon=True).start()

# --- Configuration de la fenêtre principale ---
root = tk.Tk()
root.title("Monte Carlo VaR Engine - Simulateur de Risque")
root.geometry("450x680")
root.configure(bg="#F4F6F9")

style = ttk.Style()
style.configure("TLabel", background="#F4F6F9", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10, "bold"))

# --- Titre ---
titre = tk.Label(root, text="Value at Risk (Monte Carlo)", font=("Arial", 14, "bold"), bg="#F4F6F9", fg="#2C3E50")
titre.pack(pady=10)

# --- Cadre des saisies ---
frame_inputs = tk.Frame(root, bg="#F4F6F9")
frame_inputs.pack(pady=5)

ttk.Label(frame_inputs, text="Capital Initial (€) :").grid(row=0, column=0, padx=10, pady=3, sticky="e")
entry_capital = ttk.Entry(frame_inputs)
entry_capital.insert(0, "10000")
entry_capital.grid(row=0, column=1, pady=3, sticky="w")

ttk.Label(frame_inputs, text="Volatilité Annuelle (%) :").grid(row=1, column=0, padx=10, pady=3, sticky="e")
entry_volat = ttk.Entry(frame_inputs)
entry_volat.insert(0, "15")
entry_volat.grid(row=1, column=1, pady=3, sticky="w")

# --- Horizon de temps avec sélecteur d'unité ---
ttk.Label(frame_inputs, text="Horizon de temps :").grid(row=2, column=0, padx=10, pady=3, sticky="e")

frame_horizon = tk.Frame(frame_inputs, bg="#F4F6F9")
frame_horizon.grid(row=2, column=1, pady=3, sticky="w")

entry_horizon = ttk.Entry(frame_horizon, width=10)
entry_horizon.insert(0, "1")
entry_horizon.pack(side=tk.LEFT, padx=(0, 5))

combo_unite = ttk.Combobox(frame_horizon, values=["Jours", "Mois", "Années"], width=8, state="readonly")
combo_unite.set("Années")
combo_unite.pack(side=tk.LEFT)

ttk.Label(frame_inputs, text="Nombre de simulations :").grid(row=3, column=0, padx=10, pady=3, sticky="e")
entry_sim = ttk.Entry(frame_inputs)
entry_sim.insert(0, "10000")
entry_sim.grid(row=3, column=1, pady=3, sticky="w")

# --- Barre d'actions principales ---
frame_actions = tk.Frame(root, bg="#F4F6F9")
frame_actions.pack(pady=10)

btn_run = tk.Button(frame_actions, text="LANCER L'ANALYSE", bg="#2980B9", fg="white", font=("Arial", 10, "bold"), command=lancer_simulation)
btn_run.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

btn_quitter = tk.Button(frame_actions, text="Quitter", command=quitter_application, bg="#E74C3C", fg="white", font=("Arial", 10, "bold"))
btn_quitter.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

# --- Zone de résultat ---
label_resultat = tk.Label(root, text="En attente des paramètres...", font=("Arial", 10, "bold"), bg="#F4F6F9", fg="#7F8C8D")
label_resultat.pack(pady=5)

# --- Cadre des deux boutons d'export distincts (Excel & PDF) ---
frame_exports = tk.Frame(root, bg="#F4F6F9")

btn_excel = tk.Button(frame_exports, text="📥 EXCEL (.XLSX)", bg="#27AE60", fg="white", font=("Arial", 9, "bold"), command=exporter_rapport_bancaire)
btn_excel.pack(side=tk.LEFT, padx=5, ipadx=8, ipady=4)

btn_pdf = tk.Button(frame_exports, text="📄 RAPPORT PDF", bg="#C0392B", fg="white", font=("Arial", 9, "bold"), command=exporter_rapport_pdf)
btn_pdf.pack(side=tk.LEFT, padx=5, ipadx=8, ipady=4)

# --- Intégration du Graphique Matplotlib ---
fig, ax = plt.subplots(figsize=(4.5, 2))
fig.patch.set_facecolor('#F4F6F9') 
ax.set_facecolor('#FFFFFF') 
ax.set_title("Simulation Monte Carlo - Trajectoire de risque", fontsize=8, color="#1B4F72", fontweight='bold')
ax.tick_params(colors='#333333', labelsize=7)
ax.grid(True, linestyle='--', alpha=0.5)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(pady=5, fill=tk.BOTH, expand=True)

root.mainloop()