# imports    
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sqlite3
import re
from glade import UI
from systeme import ST
from download import Download
from config import Config

class Handler:
	"""
	classe pour gérer l'interface utilisateur
	"""

	def __init__(self, fichier_config, fichier_db):
    # =============================================
		"""	
		Initialise une nouvelle instance de la classe Handler
		"""
  
		# chemin vers les fichiers de config et de base de données
		self.fichier_config = fichier_config
		self.fichier_db = fichier_db

		# on fixe les variables de pagination
		self.pagination_numero_page = 0
		self.pagination_nombre_page = 0
		self.pagination_lignes_par_page = 500
	
		# on conserve l'ID de la base de données correspondant
		# au jeu sélectionné pour pouvoir mettre a jour l'état du
		# jeu si on demande le téléchargement
		self.id_selection_telechargement = 0

		# reference au processus de telechargement
		self.download_process = None		

		# on conserve les variables de la sélection en cours,
		# valeurs attribuées dans 'on_tree_selection_liste_jeux_changed()'
		self.selection_jeux_model = 0
		self.selection_jeux_treeiter = 0
		self.selection_liste_jeux_changed_en_cours = ''

		# dictionnaire des sections de jeux
		self.dict_sections_jeux = {
			'All games': 'all',		# Tous les jeux
			'Numbers': 'nombres',	# Nombres
			'A': 'a','B': 'b','C': 'c','D': 'd','E': 'e','F': 'f','G': 'g','H': 'h','I': 'i','J': 'j',
			'K': 'k','L': 'l','M': 'm','N': 'n','O': 'o','P': 'p','Q': 'q','R': 'r','S': 's','T': 't',
			'U': 'u','V': 'v','W': 'w','X': 'x','Y': 'y','Z': 'z'
		}
  
		# on fixe la combo box avec les sections de jeu
		for cle in self.dict_sections_jeux:			
			myiter = UI.list_store_combo_box_sections_jeux.insert_before(None, None)
			UI.list_store_combo_box_sections_jeux.set_value(myiter, 0, cle)
		UI.combo_box_sections_jeux.set_active(0)

		# dictionnaire des doublons
		self.selection_doublons = "all"
		self.dict_doublons = {
			'Full list': 'all',						# Liste complète
			'without duplicates': 'doublons off',	# liste sans doublons
			'show duplicates': 'doublons on'		# Afficher les doublons
		}
  
		# on fixe la combo box avec les doublons
		for cle in self.dict_doublons:			
			myiter = UI.list_store_combo_box_doublons.insert_before(None, None)
			UI.list_store_combo_box_doublons.set_value(myiter, 0, cle)
		UI.combo_box_doublons.set_active(0)

		# dictionnaire des etats de jeu
		self.dict_etats_jeux = {
			'All games': '', 				# Tous les jeux
			'Downloaded': 'X',				# Téléchargé
			'Not downloaded': '-',			# Non téléchargé
			'Download in progress': '=', 	# Téléchargement en cours
			'Download error': '!'			# Erreur téléchargement
		}
  
		# on fixe la combo box avec les etats de jeu
		for cle in self.dict_etats_jeux:			
			myiter = UI.list_store_combo_box_etats_jeux.insert_before(None, None)
			UI.list_store_combo_box_etats_jeux.set_value(myiter, 0, cle)
		UI.combo_box_etats_jeux.set_active(0)

	def update_tree_view_liste_jeux(self):
    # ====================================
		""" 		
		Cette fonction est utilisée pour mettre à jour le 'tree view'
		contenant la liste des jeux.
  		"""

		# on ouvre la base de données	
		db_connect = sqlite3.connect(self.fichier_db)
		db_connect.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)
		db_cursor = db_connect.cursor()
		
		# requête de base
		requete = f"{ST.requete_base_systemes} "+\
			f"{ST.requete_add_sections_jeux} "+\
			f"{ST.requete_add_etats_jeux} "+\
			f"{ST.requete_add_recherches} "+\
			"ORDER BY nom ASC "

		# listes
		liste_complete = []
		liste_sans_doublons = []
		liste_doublons = []

		# on effectue un trie de la liste
		# avec ou sans doublons
		ligne_precedente = ""
		for row in db_cursor.execute(requete):
		
			liste_complete.append(row)
			if row[2] != ligne_precedente:
				liste_sans_doublons.append(row)
			else:
				liste_doublons.append(row)
			ligne_precedente = row[2]

		# on choisit la liste à utilisé pour alimenter
		# la 'list store' a allé chercher depuis 'on_combo_box_doublons_changed()'
		liste_selectionnee = liste_complete		
		match self.selection_doublons:
			case 'doublons off':
				liste_selectionnee = liste_sans_doublons			
			case 'doublons on':
				liste_selectionnee = liste_doublons

		# on récupère le nombre de jeux par machine
		# depuis la classe 'Systeme' 'ST.dict_count_from_machine[ST.cle_requete_jeux_en_cours]'
		# le nombre de jeux de chaques machines, systèmes sont récuperés au moment
		# de l'initialisation de la classe et sont stockés dans un dictionnaire avec comme
		# clés les clés systèmes '[0], [0, 0], [1], [0,0]...'
		nombre_de_jeux_par_machine = ST.dict_count_from_machine[ST.cle_requete_jeux_en_cours]
  
		# on met en place la pagination et on met à jour dans l'interface
		# le nombre de jeux dans les labels infos
		nombre_total_ligne = len(liste_selectionnee)
		UI.label_info_jeux.set_markup(f"<b>{nombre_total_ligne} / {nombre_de_jeux_par_machine} Games</b>")		
		self.pagination_nombre_page = int( nombre_total_ligne / self.pagination_lignes_par_page )		
		UI.label_info_page.set_markup(f"<b><big>{self.pagination_numero_page + 1} / {self.pagination_nombre_page + 1}</big></b>")
		
		# on met en place la limite et l'offset
		# pour gerer le multi pages
		limit = self.pagination_lignes_par_page
		offset = ( self.pagination_lignes_par_page * self.pagination_numero_page )		
		UI.list_store_tree_view_liste_jeux.clear() # on vide la 'list store'

		# on insère dans la liste selectionnee
		for i in range(limit):

			if offset + i>= nombre_total_ligne: break
			myiter = UI.list_store_tree_view_liste_jeux.insert_before(None, None)
			UI.list_store_tree_view_liste_jeux.set_value(myiter, 0, liste_selectionnee[offset + i][0])
			UI.list_store_tree_view_liste_jeux.set_value(myiter, 1, (liste_selectionnee[offset + i][1] if liste_selectionnee[offset + i][1] != "-" else ""))
			UI.list_store_tree_view_liste_jeux.set_value(myiter, 2, liste_selectionnee[offset + i][2])
			UI.list_store_tree_view_liste_jeux.set_value(myiter, 3, liste_selectionnee[offset + i][3])			
			
		# on met à jour la sélection de la nouvelle liste
		# et on ferme la base de données
		self.selection_liste_jeux_changed_en_cours = ''
		UI.tree_view_liste_jeux.set_cursor(0)
		db_connect.close()

	def on_window_scrom_destroy(self, *args):
    # =======================================
		"""
  		fermer la fenêtre
    	"""
     
		Gtk.main_quit()

	def on_button_quitter_clicked(self, button):
    # ==========================================
		"""
  		bouton 'quitter'
    	"""
     	
		Gtk.main_quit()

	def	on_tree_selection_liste_jeux_changed(self, selection):
    # ========================================================
		"""
		selection d'un jeu dans la liste, on recherche le lien
		de telechargement du jeu dans la base de données et on
		on l'affiche dans le widget 'UI.entry_lien_telechargement'
		la récupération du lien s'éffectue avec l'ID de l'entrée,
		colonne ( cachée ), dans base de données 'db_cursor.fetchone()[0]'
		"""

		# on conserve les indices de la selection		
		self.selection_jeux_model, self.selection_jeux_treeiter = selection.get_selected()
		
		# on teste la valite de la selection		
		if self.selection_jeux_treeiter is not None:
		
			# on récupère l'indice de la selection			
			treepath = self.selection_jeux_model.get_path(self.selection_jeux_treeiter)

			# si l'indice est différent de la sélection en cours
			# on se connecte à la base de données pour récupérer le lien
			# de téléchargement du jeu et on affiche le lien dans
			# 'UI.entry_lien_telechargement' """			
			if treepath.get_indices() != self.selection_liste_jeux_changed_en_cours:
				
				# on se connecte à la base de données
				db_connect = sqlite3.connect(self.fichier_db)
				db_cursor = db_connect.cursor()

				# on récupère l'ID du jeu depuis la colonne cachée du treeview
				# '[self.selection_jeux_treeiter][0]' correspond à la colonne 'ID' """				
				self.id_selection_telechargement = self.selection_jeux_model[self.selection_jeux_treeiter][0]

				# on compose la requête et on l'exécute				
				requete = f"SELECT lien FROM jeux WHERE id='{self.id_selection_telechargement}'"
				db_cursor.execute(requete)
				db_connect.commit()
				
				# on insère le lien de téléchargement du jeu dans
				# 'UI.entry_lien_telechargement'				
				UI.entry_lien_telechargement.set_text(db_cursor.fetchone()[0])

				# on conserve l'indice				
				self.selection_liste_jeux_changed_en_cours = treepath.get_indices()

				# on ferme la base				
				db_connect.close()

	def	on_tree_selection_systemes_changed(self, selection):
    # ======================================================
		"""	
		selection d'un systeme dans la liste
		"""
  
		# récupérer la clé requête correspondant à la sélection		
		model, treeiter = selection.get_selected()
		treepath = model.get_path(treeiter)
		cle_requete_jeux = str(treepath.get_indices())

		# on conserve la cle requete en cours
		# pour l'affichage du nombre total de jeux disponibles
		# dans 'update_tree_view_liste_jeux()'
		ST.cle_requete_jeux_en_cours = cle_requete_jeux
		
		# si le clé est supèrieure à 4 il s'agit de la sélection
		# d'un téléverseur, on rend visible la colonne 'téléverseur'		
		if len(cle_requete_jeux) > 4:
			UI.tree_view_column_televerseurs.set_visible(False)
		else:
			UI.tree_view_column_televerseurs.set_visible(True)

		# on conserve la requete systeme de base en cours
		ST.requete_base_systemes = ST.dict_requetes[cle_requete_jeux]
		
		# afficher le nom du systeme dans 'UI.label_info_machine' et dans
		# 'UI.entry_repertoire_telechargement_systeme'		
		machine = (ST.requete_base_systemes.split('C.machine = ')[1].split(' ')[0]).replace("'", "")
		UI.label_info_machine.set_text(f"{machine}")
		
		# afficher le nom de la machine si 'check_button_ajouter_repertoire_systeme' est 'True'		
		if UI.check_button_ajouter_repertoire_machine.get_active():
			UI.entry_repertoire_telechargement_systeme.set_text(f"/{machine}")		

		# mettre à jour le liste des jeux a 0 pour la nouvelle liste
		self.pagination_numero_page = 0
		self.pagination_nombre_page = 0
		self.update_tree_view_liste_jeux()
		
	def on_entry_recherches_activate(self, entry):
    # ============================================
		"""
		on effectue une action de recherche avec la valeur de 'entry'
		dans la liste de jeux en cours et on met a jour la liste
  		"""
		
		ST.requete_add_recherches = ""
		search_text = entry.get_text()
		if search_text != "":
			ST.requete_add_recherches = f"AND A.nom LIKE '%{search_text}%'"
   
		# on remet la pagination a 0
		self.pagination_numero_page = 0
		self.pagination_nombre_page = 0
  
		# on met à jour la liste
		self.update_tree_view_liste_jeux()

	def on_entry_recherches_icon_release(self, start_pos, end_pos, user_data):
	# ========================================================================
		"""
		action sur l'icone pour effacer la recherche en cours
  		"""
	
		ST.requete_add_recherches = ""
  
		# on remet la pagination a 0
		self.pagination_numero_page = 0
		self.pagination_nombre_page = 0
  
		# on met à jour la liste
		self.update_tree_view_liste_jeux()

	def on_combo_box_sections_jeux_changed(self, combo):
    # ==================================================
		"""
		action sur la selection d'une nouvelle section qui
		correspond a : liste complete, number, A, B, C, etc
  		"""

		# on recupere la section choisie depuis le combobox
		tree_iter = combo.get_active_iter()
		model = combo.get_model()
		combo_value = model[tree_iter][0]
		section = self.dict_sections_jeux[combo_value]	
		
		# on met à jour la requête
		ST.requete_add_sections_jeux = f"AND A.nom regexp '^(?i:{section})'"
		match section:
			case 'all':
				ST.requete_add_sections_jeux = ""
			case 'nombres':
				ST.requete_add_sections_jeux = "AND A.nom regexp \"^[0-9-']\""

		# on remet la pagination a 0				
		self.pagination_numero_page = 0
		self.pagination_nombre_page = 0
  
		# on met à jour la liste
		self.update_tree_view_liste_jeux()

	def on_combo_box_etats_jeux_changed(self, combo):
	# ===============================================
		"""
		action sur la selection d'un nouvel etat des jeux qui
		correspond a : Telecharge, Non Telecharge, etc
		"""
  
		# on recupere un des etats depuis le combobox
		tree_iter = combo.get_active_iter()
		model = combo.get_model()
		combo_value = model[tree_iter][0]
		
		# on met à jour la requête
		symbole_etat = self.dict_etats_jeux[combo_value]	
		if symbole_etat == "": ST.requete_add_etats_jeux = ""
		else: ST.requete_add_etats_jeux =f"AND A.telechargement = '{symbole_etat}'"
		
		# on remet la pagination a 0				
		self.pagination_numero_page = 0
		self.pagination_nombre_page = 0
  
		# on met à jour la liste
		self.update_tree_view_liste_jeux()

	def on_combo_box_doublons_changed(self, combo):
	# =============================================
		"""
		action sur la selection d'un affichage de la liste
		avec ou sans doublons
  		"""
	
		# on recupere un des etats depuis le combobox
		tree_iter = combo.get_active_iter()
		model = combo.get_model()
		combo_value = model[tree_iter][0]
		
		# on met à jour la requête
		self.selection_doublons = self.dict_doublons[combo_value]
		
		# on remet la pagination a 0				
		self.pagination_numero_page = 0
		self.pagination_nombre_page = 0
  
		# on met à jour la liste
		self.update_tree_view_liste_jeux()

	def on_button_page_suivante_clicked(self, button):
    # ================================================
		"""
		action sur le bouton 'page suivante'
		si le numero de page est correct on
		passe a la page suivante et on met a jour la liste des jeux
		"""
		
		if self.pagination_numero_page < self.pagination_nombre_page:		
			self.pagination_numero_page += 1
			self.update_tree_view_liste_jeux()

	def on_button_page_precedente_clicked(self, button):
    # ==================================================
		"""
		action sur le bouton 'page precedente'
		si le numero de page est correct on
		passe a la page precedente et on met a jour la liste des jeux
		"""

		if self.pagination_numero_page > 0:		
			self.pagination_numero_page -= 1
			self.update_tree_view_liste_jeux()

	def on_button_telecharger_clicked(self, button):
	# ==============================================
		"""
		action sur le bouton 'telecharger'
		"""
		
		# on conserve la reference au processus de telechargement
		# pour pouvoir l'arreter
		self.download_process = Download(self.id_selection_telechargement, self.fichier_db)

	def on_button_arreter_telechargement_clicked(self, button):
	# =========================================================
		"""
		action sur le bouton 'arreter telechargement'
  		"""

		# arret du processus de telechargement
		self.download_process.terminate()

	def on_check_button_ajouter_repertoire_machine_toggled(self, button):
    # ===================================================================
		"""
		action sur le toggle button pour ajouter ou non
		le repertoire de la machine lors du telechargement
		"""
	
		# on inverse l'etat du toggle button
		# si c'est true on affiche le nom de la machine	
		# sinon on efface la zone
		check_repertoire_systeme = False
		if UI.check_button_ajouter_repertoire_machine.get_active():
			check_repertoire_systeme = True
			UI.entry_repertoire_telechargement_systeme.set_text(f"/{UI.label_info_machine.get_text()}")
		else:
			UI.entry_repertoire_telechargement_systeme.set_text('')

		# on sauvegarde l'etat du toggle button
		Config.save(self, 'repertoire_telechargement_systeme_etat', check_repertoire_systeme)	

	def on_entry_repertoire_telechargement_activate(self, entry):
    # ===========================================================
		"""
		la zone de saisie du repertoire de telechargement est activee
		"""
		
		# on sauvegarde le nouveau chemin de telechargement
		Config.save(self, 'repertoire_telechargement', f"{UI.entry_repertoire_telechargement.get_text()}")
  
		# on deplace le focus de la zone de saisie du chemin de telechargement
		# vers le toggle button
		UI.check_button_ajouter_repertoire_machine.grab_focus()
	
	def on_entry_commande_telechargement_activate(self, entry):
    # =========================================================
		"""
		action sur le nombre de connexion, a la base entry_commande_telechargement
		devait contenir une commande de telechargement style : axel -c -n 5
		"""
		
		# on sauvegarde le nouveau nombre de connexion
		Config.save(self, 'nombre_connexion', f"{UI.entry_commande_telechargement.get_text()}")	
  
		# on deplace le focus de la zone de saisie du nombre de connexion
		# vers le bouton 'telecharger'
		UI.button_telecharger.grab_focus()

	def on_tree_view_liste_jeux_button_press_event(self, tv, event):
	# ==============================================================
		"""
		afficher un menu avec la souris, bouton de droite pour
		modifier l'état d'une sélection de jeu, 'Téléchargé', 'Non téléchargé'
		'Téléchargement en cours'
		"""
		
		# si il y a une action du bouton de droite de la souris
		# et si un jeu est selectonne
		if event.button == 3 and self.selection_liste_jeux_changed_en_cours != "":
			
			# creation du menu
			treeview_menu = Gtk.Menu()
			
			# creation des items du menu
			for key in self.dict_etats_jeux:
				
				if self.dict_etats_jeux[key] != '':
					menu_item = Gtk.MenuItem(key)
					menu_item.connect("activate", self.pop_menu)
					treeview_menu.append(menu_item)
				else:
					menu_item = Gtk.MenuItem("")
					treeview_menu.append(menu_item)
					
			menu_item = Gtk.MenuItem("")
   
			# on ajoute le menu au treeview
			treeview_menu.append(menu_item)
			
			# on affiche le menu
			treeview_menu.popup(None, None, None, None, 1, 0)
			treeview_menu.show_all()

	def pop_menu(self, menu):
    # =======================
		"""
		creation de la fenetre du menu avec les differents etats
		"""
		
		# si le label du menu n'est pas '-'
		# on met a jour l'état de téléchargement dans la base de données
		if self.dict_etats_jeux[menu.get_label()] != '-':
			self.selection_jeux_model[self.selection_jeux_treeiter][1] =\
				self.dict_etats_jeux[menu.get_label()]
		else:
			self.selection_jeux_model[self.selection_jeux_treeiter][1] = " "

		# on récupère l'identifiant et l'état du jeu
		id = self.selection_jeux_model[self.selection_jeux_treeiter][0]
		etat = self.dict_etats_jeux[menu.get_label()]

		# on ouvre la base de données
		db_connect = sqlite3.connect(self.fichier_db)
		db_cursor = db_connect.cursor()

		# on met a jour l'état du jeu dans la base de données
		db_cursor.execute('''UPDATE jeux SET telechargement = ? WHERE id = ?''', (etat, id))
		db_connect.commit()
		db_connect.close()
			