# imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from pathlib import Path
from glade import Glade, UI
from systeme import Systeme
from handler import Handler
from config import Config
import json

class Scrom:
	"""	
	classe principale
	"""

	def __init__(self):
    # =================
		"""
		Initialise une nouvelle instance de la classe Scrom
		"""
		
		# on determine les chemins vers le fichier glade,
		# le fichier json et le fichier de base de données
		self.dossier_projet = Path.cwd()
		self.fichier_glade = self.dossier_projet.joinpath("scrom.glade")
		self.fichier_db = self.dossier_projet.joinpath("scrom.db")
		self.fichier_config = self.dossier_projet.joinpath("scrom.json")		
		self.dossier_telechargement = Path.home().joinpath("Games")

		# on cree les instances de la classe Glade, Systeme, Handler et Config
		Glade(self.fichier_glade)
		Systeme(self.fichier_db)
		self.handler = Handler(self.fichier_config, self.fichier_db)
		self.config = Config(self.fichier_config)
  
		# on initialise le fichier de config json si il n'existe pas
		# avec des valeurs par defaut
		if self.config.json_file_exist() == False:
			config_file = {\
				"repertoire_telechargement": f"{self.dossier_telechargement}",\
				"repertoire_telechargement_systeme_etat": False,\
				"nombre_connexion": "2"}
			self.config.init(config_file)

	def run(self):
    # ============
		"""
		Exécute l'application
		"""
		# on positionne la fenêtre au centre
		UI.window_scrom.set_position(Gtk.WindowPosition.CENTER)
  
		# on connecte les signaux avec la classe Handler
		UI.builder.connect_signals(self.handler)
  
		# on affiche la fenêtre
		UI.window_scrom.show_all()

		# on centre la colonne de l'etat des jeux
		UI.cell_renderer_telechargements.set_alignment(0.5, 0)
  
		# on recupere depuis le fichier json les valeurs
		# de quelques widgets de la fenêtre
		UI.entry_repertoire_telechargement.set_text(self.config.load("repertoire_telechargement"))
		if self.config.load("repertoire_telechargement_systeme_etat") == True:
			UI.entry_repertoire_telechargement_systeme.set_text(f"/{UI.label_info_machine.get_text()}")
			UI.check_button_ajouter_repertoire_machine.set_active(True)
		UI.entry_commande_telechargement.set_text(self.config.load("nombre_connexion"))
    
		# on donne la main a Gtk
		Gtk.main()
			
# main		
if __name__ == "__main__":
    
	# on initialise l'application
	app = Scrom()
 
	# on execute l'application
	app.run()
