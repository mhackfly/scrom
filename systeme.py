# imports    
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sqlite3
from glade import UI

class ST:
	"""
 	namespace de la classe Systeme pour stocker des variables
	"""

class Systeme:
	"""	
	classe pour gérer la base de donnees
	"""

	def __init__(self, db_file):
    # ==========================
		"""
		Initialise une nouvelle instance de la classe Systeme
		"""
	
		# on fixe les requêtes de base
		ST.requete_base_systemes = ""
		ST.requete_add_sections_jeux = ""
		ST.requete_add_etats_jeux = ""
		ST.requete_add_recherches = ""

		# on fixe le dictionnaire des requêtes
		ST.dict_requetes = {}
		ST.cle_requete_jeux_en_cours = ""
		ST.dict_count_from_machine = {}

		# connexion à la base de données
		db_connect = sqlite3.connect(db_file)
		db_cursor = db_connect.cursor()

		# on récupère dans une liste le nom des machines
		# en supprimant les doublons
		db_cursor.execute("SELECT machine,televerseur FROM systemes")
		db_connect.commit()
		self.machines = []
		for item in db_cursor:
			if item[0] not in self.machines:
				self.machines.append(item[0])

		# on boucle sur le nom des machines
		i0 = -1
		for machine in self.machines:

			# on insère dans le tree_view_systeme le nom de la machine.
			i0 += 1 ; i1 = -1
			iter_level_1 = UI.tree_store_tree_view_systemes.insert_before(None, None)
			UI.tree_store_tree_view_systemes.set_value(iter_level_1, 0, machine)
			db_cursor.execute(f"SELECT televerseur FROM systemes WHERE machine='{machine}'")
			db_connect.commit()
			ST.dict_requetes[f"[{i0}]"] = self.requete_machine(machine)
			ST.dict_count_from_machine[f"[{i0}]"] = [machine]
   
			# on boucle sur les nom des téléverseurs à partir du nom
			# de la machine. liste établis depuis une requête.
			for televerseur in db_cursor:

				# on insère dans le tree_view_systeme le nom du téléverseur
				i1 += 1
				iter_level_2 = UI.tree_store_tree_view_systemes.insert_before(iter_level_1, None)
				UI.tree_store_tree_view_systemes.set_value(iter_level_2, 0, televerseur[0])
				ST.dict_requetes[f"[{i0}, {i1}]"] = self.requete_machine_televerseur(machine, televerseur)

				ST.dict_count_from_machine[f"[{i0}, {i1}]"] = televerseur
		
		# on ferme la connexion à la base de données				
		db_connect.close()

		# on appel la fonction 'get_counts_from_machines()'
		# pour compter le nombre de jeux dans chaque machine
		self.get_counts_from_machines(db_file)

	def get_counts_from_machines(self, db_file):
    # ========================================== 
		"""
		Retourne le nombre de jeux contenus dans chaque machine de la base de données.
		"""
  
		# on fixe la variable 'total_games' à 0
		total_games = 0
  
		# on crée la requête pour compter le nombre de jeux
		requete_base = "SELECT COUNT(*) "+\
			"FROM jeux A, pages B, systemes C "+\
			"WHERE A.lien_page = B.lien "+\
			"AND B.identifiant_systeme = C.identifiant "

		current_machine = ""
  
		# on boucle sur la liste des noms de machines
		for cle in ST.dict_count_from_machine:

			# si la clé est inférieure à 5, il s'agit d'une machine
			if len(cle) < 5:
       
				# on insère dans le dictionnaire le nom de la machine
				machine = ST.dict_count_from_machine[cle][0]
				requete = requete_base + f"AND C.machine = '{machine}'"
				ST.dict_count_from_machine[cle] = self.select_count_from_machine(db_file, requete)
    
				# on additionne le nombre de jeux de la machine
				print(f"{machine:<20}", f":{ST.dict_count_from_machine[cle]:>8}")
				total_games += ST.dict_count_from_machine[cle]
    
			else:
       
				# on insère dans le dictionnaire le nom du televerseur
				televerseur = ST.dict_count_from_machine[cle][0]
				requete = requete_base + f"AND C.machine = '{current_machine}'" + f"AND C.televerseur = '{televerseur}'"
				ST.dict_count_from_machine[cle] = self.select_count_from_machine(db_file, requete)
 
			# on conserve le nom de la machine
			current_machine = machine

		# on affiche le nombre total de jeux
		label="TOTAL"
		print(f"{label:<20}", f":{total_games:>8} games")
  
	def select_count_from_machine(self, db_file, requete):
	# ====================================================
		"""
		Compte le nombre d'enregistrements, de jeux contenus dans un système, machine, en
		exécutant une requête avec la commande 'COUNT(*)'
		"""

		db_connect = sqlite3.connect(db_file)
		db_cursor = db_connect.cursor()
		db_cursor.execute(requete)
		db_connect.commit()
		count = db_cursor.fetchone()[0]
		db_connect.close()

		return count

	def requete_machine(self, machine):
    # =================================
		"""
		Crée une requête SQL pour obtenir tous les jeux d'une machine donnée.
		"""

		return ("SELECT A.id, telechargement, nom, televerseur "+\
		"FROM jeux A, pages B, systemes C "+\
		"WHERE A.lien_page = B.lien "+\
		"AND B.identifiant_systeme = C.identifiant "+\
		f"AND C.machine = '{machine}'")

	def requete_machine_televerseur(self, machine, televerseur):
    # ==========================================================
		"""
		Crée une requête SQL pour obtenir tous les jeux d'une machine et d'un téléverseur donnés.
		"""

		return ("SELECT A.id, telechargement, nom, televerseur "+\
		"FROM jeux A, pages B, systemes C "+\
		"WHERE A.lien_page = B.lien "+\
		"AND B.identifiant_systeme = C.identifiant "+\
		f"AND C.machine = '{machine}' "+\
		f"AND C.televerseur = '{televerseur[0]}'")
