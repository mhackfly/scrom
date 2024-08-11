# imports    
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import sqlite3
import multiprocessing
import subprocess
import os.path
from glade import UI

class Download:
	"""
	classe pour gérer le telechargement
	"""
    
	def __init__(self, id_selection_telechargement, fichier_db):
    # ==========================================================
		"""
		Initialise une nouvelle instance de la classe Download
		"""

		# on recupère le fichier de la base de données
		self.fichier_db = fichier_db
	
		# on recupère le dictionnaire de l'état des jeux
		self.id_selection_telechargement = id_selection_telechargement
		
		# buffer du text view en global
		self.text_buffer = UI.text_view_infos.get_buffer()
		
		# on vérifie avant de démarrer des vérifications si le jeu
		# sélectionné n'est pas déjà marqué comme téléchargé par 'X'
		if self.verifier_etat_telechargement('X'):
			self.text_buffer.insert_markup(self.text_view_get_end(),\
				"<i><small>Game marked downloaded\n</small></i>", -1)
			return
		
		# le telechargement va demarrer, on desactive le bouton
		# de telechargement et on active le bouton stop
		UI.button_telecharger.set_sensitive(False)
		UI.button_arreter_telechargement.set_sensitive(True)

		# on affiche des infos concernant la vérification du téléchargement,
  		# on détache le nom du jeu du lien pour pouvoir l'affichager dans le text view
		self.text_buffer.insert_markup(self.text_view_get_end(), "<b>Check download :\n</b>", -1)
		self.text_buffer.insert_markup(self.text_view_get_end(),\
			f"<small>{UI.entry_lien_telechargement.get_text().rsplit('/', 1)[0]}\n</small>", -1)
		self.text_buffer.insert_markup(self.text_view_get_end(),\
			f"<small><b><u>{UI.entry_lien_telechargement.get_text().rsplit('/', 1)[1]}\n</u></b></small>", -1)
		self.text_buffer.insert_markup(self.text_view_get_end(), "<small><i>Wait...\n</i></small>", -1)
    

		# on compose le répertoire destination avec
		# 'UI.entry_repertoire_telechargement.get_text()' et si
		# 'UI.check_button_ajouter_repertoire_machine.get_active()' est actif
		# on rajoute 'UI.entry_repertoire_telechargement_systeme.get_text()'
		# le répertoire correspondant au système
		repertoire_telechargement = UI.entry_repertoire_telechargement.get_text()
		if UI.check_button_ajouter_repertoire_machine.get_active():
			repertoire_telechargement += UI.entry_repertoire_telechargement_systeme.get_text()

		# on verifie si le répertoire ou enregistrer le jeu existe
		if os.path.exists(repertoire_telechargement):

			# on démarre la surveillance à intervalles régulières
			# en appelant la fonction 'recuperer_sortie_telechargement()', de la sortie du
			# script bash de téléchargement pour récupèrer la progression
			# du téléchargement du programme 'axel'
			self.flag = multiprocessing.Value('i', 0) # démarrage 'recuperer_sortie_telechargement()'
			self.timeout_id = GLib.timeout_add(50, self.recuperer_sortie_telechargement, None)
			
			# On convertit les chaines de caractères en types de données 'bytes'
			# pour pouvoir les partager avec un processus fils.
			# On utilise la méthode 'encode()' pour convertir les chaines en 'bytes'.
			# On crée des 'multiprocessing.Array' pour stocker les 'bytes' dans la mémoire partagée
			# des processus.
			# On crée également des 'multiprocessing.Value' pour stocker des valeurs numériques
			# (ici la fraction du téléchargement) dans la mémoire partagée.
			str_commande_as_bytes = str.encode(UI.entry_commande_telechargement.get_text())
			str_lien_as_bytes = str.encode(UI.entry_lien_telechargement.get_text())
			str_repertoire_as_bytes = str.encode(repertoire_telechargement)
			str_text_info_as_bytes = str.encode(' '*255)
			self.commande = multiprocessing.Array('c', str_commande_as_bytes)
			self.lien = multiprocessing.Array('c', str_lien_as_bytes)
			self.repertoire = multiprocessing.Array('c', str_repertoire_as_bytes)
			self.infos = multiprocessing.Array('c', str_text_info_as_bytes)
			self.fraction = multiprocessing.Value('f', 0.0)
			
			# on démarre le process qui va lancé le script de téléchagement
			# 'download.sh'
			process = multiprocessing.Process(target=self.telechargement,\
				args=(self.flag, self.commande, self.lien, self.repertoire, self.infos, self.fraction), daemon=True)
			process.start() # démarrage 'téléchargement()'

			# le telechargement du jeu demarre, on peut marquer l'état du jeux
			# comme étant en cours de téléchargement avec le caractère '='
			# en appelant la fonction de mise à jour 'update_etat_telechargement()'
			self.update_etat_telechargement('=')
			
		else:

			# le repertoire de destination n'existe pas, on informe
			# et on inverse la sensibilite des boutons
			self.text_buffer.insert_markup(self.text_view_get_end(), "<i><small>Destination directory does not exist\n</small></i>", -1)
			UI.button_arreter_telechargement.set_sensitive(False)
			UI.button_telecharger.set_sensitive(True)

	def recuperer_sortie_telechargement(self, user_data):
    # ===================================================
		"""
		recuperation de la sortie du processus 'axel'
		cette fonction est appelée par 'GLib.timeout_add()'
		par intervalles de 50 millisecondes
		cette fonction est a l'ecoute de 'flag.value' qui est modifié
  		par la fonction 'téléchargement()' qui lance le script bash 'download.sh'
		qui lance le processus 'axel' qui permet de telecharger le jeu
		"""

		# fonction telechargement() -> self.flag.value == 1 :
  		# demarrage du script download.sh
		if self.flag.value == 1:

			self.text_buffer.insert_markup(self.text_view_get_end(), f"<small>{(self.infos.value).decode('utf-8')}</small>", -1)
			self.text_buffer.insert_markup(self.text_view_get_end(), "<b>Starting download :\n</b>", -1)
			self.text_buffer.insert_markup(self.text_view_get_end(), "<small><i>In progress...\n</i></small>", -1)
   
			# on fixe le 'flag' à 2 pour passer directement
			# a l'etape suivante et mettre a jour le progressbar
			self.flag.value = 2

		# fonction téléchargement() -> self.flag.value == 2 :
		# on met à jour le progressbar
		if self.flag.value == 2:

			UI.progress_bar_telechargement.set_fraction(self.fraction.value)

		# fonction telechargement() -> self.flag.value == 3 :
		# le telechargement est terminé
		if self.flag.value == 3:

			# on fixe le progressbar à 1 (100%)
			UI.progress_bar_telechargement.set_fraction(1)
   
			# on affiche les infos sur le temps du telechargement et le debit
			self.text_buffer.insert_markup(self.text_view_get_end(),\
				f"<small>{(self.infos.value).decode('utf-8').rsplit(' in', 1)[0]}\n</small>", -1)
			self.text_buffer.insert_markup(self.text_view_get_end(),\
				f"<small>in {(self.infos.value).decode('utf-8').rsplit(' in', 1)[1]}</small>", -1)

			# on affiche le message de fin de telechargement
			self.text_buffer.insert_markup(self.text_view_get_end(), "Download completed 100%\n", -1)

			# on met à jour l'etat du jeu (X : telechargé)
			self.update_etat_telechargement('X')

			# on inverse la sensibilite des boutons
			UI.button_arreter_telechargement.set_sensitive(False)
			UI.button_telecharger.set_sensitive(True)

			# on informe par une boite de dialogue
			# que le telechargement est terminé
			self.dialog()
   
			# on fixe le progressbar à 0
			UI.progress_bar_telechargement.set_fraction(0)

			# return False pour arreter le 'GLib.timeout_add()' !!!!
			return False

		# fonction telechargement() -> self.flag.value == 4 :
		# le telechargement est interrompu par le bouton stop
		if self.flag.value == 4:

			# on informe telechargement arreter par le bouton stop
			self.text_buffer.insert(self.text_view_get_end(), f"Download stopped :  {int(self.fraction.value*100) + 1}%\n")

			# on met à jour l'etat du jeu (= : en cours)
			self.update_etat_telechargement('=')

			# on inverse la sensibilite des boutons
			UI.button_arreter_telechargement.set_sensitive(False)
			UI.button_telecharger.set_sensitive(True)

			# on fixe le progressbar à 0
			UI.progress_bar_telechargement.set_fraction(0)

			# return False pour arreter le 'GLib.timeout_add()' !!!!
			return False

		# fonction telechargement() -> self.flag.value == 5 :
		# le programme 'axel' informe que le fichier de sortie existe
		if self.flag.value == 5:

			# on informe que le fichier de sortie existe deja
			self.text_buffer.insert_markup(self.text_view_get_end(), "<i><small>The file already exists\n</small></i>", -1)

			# on met à jour l'etat du jeu (X : telechargé)
			self.update_etat_telechargement('X')

			# on inverse la sensibilite des boutons
			UI.button_arreter_telechargement.set_sensitive(False)
			UI.button_telecharger.set_sensitive(True)

			# on fixe le progressbar à 0
			UI.progress_bar_telechargement.set_fraction(0)

			# return False pour arreter le 'GLib.timeout_add()' !!!!
			return False

		# fonction telechargement() -> self.flag.value == 6 :
		# le programme 'axel' interromp le telechargement
		if self.flag.value == 6:

			# on informe que le telechargement a echoué
			self.text_buffer.insert_markup(self.text_view_get_end(), "<i><small>download error !?\n</small></i>", -1)

			# on met à jour l'etat du jeu (! : erreur)
			self.update_etat_telechargement('!')

			# on inverse la sensibilite des boutons
			UI.button_arreter_telechargement.set_sensitive(False)
			UI.button_telecharger.set_sensitive(True)

			# on fixe le progressbar à 0
			UI.progress_bar_telechargement.set_fraction(0)

			# return False pour arreter le 'GLib.timeout_add()' !!!!
			return False

		# fin
		return True

	def telechargement(self, flag, commande, lien, repertoire, infos, fraction):
    # ==========================================================================
		"""
		on demarre le processus de telechargement en lancant le script bash download.sh
		"""
     
		# convertir les arguments de bytes vers string
		# les variables flag, commande, lien, repertoire, infos et fraction
		# sont en mémoire partagée, cette fonction 'telechargement()' et
		# un process lancé dans la classe
		# > process = multiprocessing.Process(target=self.telechargement,\
		# args=(self.flag, self.commande, self.lien, self.repertoire, self.infos, self.fraction), daemon=True)
		# > process.start()
		str_commande = (commande.value).decode("utf-8")
		str_repertoire = (repertoire.value).decode("utf-8")
		str_lien = (lien.value).decode("utf-8")

		# on démarre 'download.sh', le script bash qui va
		# téléchargé le jeu et on récupère l'affichage de sortie
		myPopen = subprocess.Popen(['./download.sh',\
			f"\"{str_commande}\"",\
			f"\"{str_repertoire}\"",\
			f"\"{str_lien}\""],\
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,\
			stderr = subprocess.PIPE, encoding = 'utf8')

		# boucle sur la sortie de 'download.sh'
		# on récupère les infos en sortie du script 'download.sh'
		for line in myPopen.stdout:
			
			# sortie 'axel' : le fichier a été telechargé
			if line.startswith('Downloaded'):
				infos.value = str.encode(line)
				flag.value = 3
				break

			# sortie 'axel' : taille du fichier
			if line.startswith('File size: '):
				infos.value = str.encode(line)
				flag.value = 1

			# sortie 'axel' : le fichier existe deja
			if "already there" in line:
				infos.value = str.encode(line)
				flag.value = 5
				break

			# la sortie d'axel est inferieure a 4 caractères
			# ce qui correspondent au pourcentage
			if len(line) > 1 and len(line) < 4:

				# flag.value = 4 : action du bouton 'stop'
				# on arret le sousprocess 'axel' et on sort
				if flag.value == 4:
					myPopen.terminate()
					break
 
				# on convertit le pourcentage pour le progressbar
				pourcentage = float(line)   
				fraction.value = pourcentage / 100

		# on attend que myPopen se termine avec
		# 'myPopen.poll()' qui renvoie le statut de
		# retour si le programme appelé a terminé,
		# sinon None s'il n'est pas fini.
		while True:
			status = myPopen.poll()
			if status is not None:
				break

		# le sous process 'axel' c'est interrompu sans avoir
		# ete traite, le flag.value est vide
  		# on positionne le flag a 6 pour erreur survenue
		if flag.value == 0:
			flag.value = 6

	def terminate(self):
    # ==================
		"""
		action du bouton 'stop'
		"""

		self.flag.value = 4

	def dialog(self):
    # ===============
		"""
		affiche un message de fin de telechargement
		"""	
		dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
			Gtk.ButtonsType.OK, "Download complete.")
		dialog.run()
		dialog.destroy()

	def update_etat_telechargement(self, etat_symbole):
    # =================================================
		"""
  		on met à jour dans la base de données l'état du
		téléchargement, ('X','-','=','!') du jeu en
		cours de téléchargement
		"""
  
		# on execute une requete de mise a jour de
		# l'état du jeu en cours de telechargement
		db_connect = sqlite3.connect(self.fichier_db)
		db_cursor = db_connect.cursor()
		db_cursor.execute('''UPDATE jeux SET telechargement = ? WHERE id = ?''', (etat_symbole,\
			self.id_selection_telechargement))
		db_connect.commit()
		db_connect.close()

		# on vérifie si l'état du jeu qui vient d'être inséré dans la base
		# de donnée doit aussi être mis à jour visuellement dans le treeview_menu
		iter_child = UI.list_store_tree_view_liste_jeux.get_iter_first()
		tree_path = None
		while iter_child:
		
			# on itère sur la 'list store' contenu dans le 'tree view'
			if (UI.list_store_tree_view_liste_jeux.get_value(iter_child, 0) == self.id_selection_telechargement):

				# si l'identifiant de la sélection en cours est présent 'à l'affichage'
				# on l'affiche directement dans le 'tree view' et on
				# positionne la sélection sur 'l'id_selection_telechargement'
				UI.list_store_tree_view_liste_jeux.set_value(iter_child, 1, (etat_symbole if etat_symbole != "-" else ""))
				tree_path = UI.list_store_tree_view_liste_jeux.get_path(iter_child)
				UI.tree_view_liste_jeux.row_activated(tree_path, UI.tree_view_liste_jeux.get_column(0))
				UI.tree_view_liste_jeux.set_cursor(tree_path, UI.tree_view_liste_jeux.get_column(0), True)		
				break
				
			# on avance le curseur de la 'list store' sur la ligne suivante
			iter_child = UI.list_store_tree_view_liste_jeux.iter_next(iter_child)

	def verifier_etat_telechargement(self, symbole):
    # ==============================================
		"""
		on verifie l'etat du jeu dont on demande le telechargement
		on va rechercher son etat directement dans le tree view
		"""

		# on itère sur la 'list store' contenu dans le 'tree view'
		# pour trouver l'identifiant du jeu
		iter_child = UI.list_store_tree_view_liste_jeux.get_iter_first()		
		while iter_child:
      
			# si la ligne correspond à l'identifiant et au symbole on retourne True
			if (UI.list_store_tree_view_liste_jeux.get_value(iter_child, 0) == self.id_selection_telechargement):
				if (UI.list_store_tree_view_liste_jeux.get_value(iter_child, 1) == symbole):
					return True
 
			# on avance le curseur de la 'list store' sur la ligne suivante
			iter_child = UI.list_store_tree_view_liste_jeux.iter_next(iter_child)
   
		# False si l'etat du jeu ne correspond pas au symbole
		return False

	def text_view_get_end(self):
	# ==========================
		"""
		renvoie l'iter de fin du buffer du text_view
		"""
  
		text_iter_end = self.text_buffer.get_end_iter()
		text_mark_end = self.text_buffer.create_mark("", text_iter_end, False)
		UI.text_view_infos.scroll_to_mark(text_mark_end, 0, False, 0, 0)
		return text_iter_end
