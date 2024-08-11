# imports
import os.path
import json

class Config:
	"""	
	classe pour gérer le fichier de config
	"""

	json_file = ""

	def __init__(self, fichier_config):
    # =================================

		Config.json_file = fichier_config		

	def json_file_exist(self):
    # ========================

		return os.path.isfile(Config.json_file)
			
	def init(self, config_file):
    # ==========================

		with open(Config.json_file, 'w') as f:
			json.dump(config_file, f)
	
	def load(self, cle):
    # ==================

		config_file = {}
		with open(Config.json_file, 'r') as f:
			config_file = json.load(f)
		return config_file[cle]
		
	def save(self, cle, valeur):
	# ==========================

		config_file = {}
		with open(Config.json_file, 'r') as f:
			config_file = json.load(f)
		config_file[cle] = valeur
		with open(Config.json_file, 'w') as f:
			json.dump(config_file, f)
