#!/bin/bash

BDD_NOM='scrom.db'
DIR_DAT='links'
NC='\033[0m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'

# -----------------------------------------
# creation des tables de la base de données
# -----------------------------------------
function create_tables() {

	# vérifier si la base de données existe
	if [ ! -f $BDD_NOM ]; then

		echo -e "${RED}database not found, create $BDD_NOM${NC}"

		# créer la base de données
		sqlite3 $BDD_NOM < /dev/null

		echo "create tables : systemes, pages, jeux"

		# créer la table systemes
		sqlite3 -batch $BDD_NOM "create table systemes (\
		id INTEGER PRIMARY KEY,\
		identifiant TEXT,\
		machine TEXT,\
		televerseur TEXT,\
		extension TEXT,\
		commentaire TEXT);" 2> /dev/null

		# créer la table pages
		sqlite3 -batch $BDD_NOM "create table pages (\
		id INTEGER PRIMARY KEY,\
		identifiant_systeme TEXT,\
		lien TEXT,\
		commentaire TEXT);" 2> /dev/null

		# créer la table jeux
		sqlite3 -batch $BDD_NOM "create table jeux (\
		id INTEGER PRIMARY KEY,\
		lien_page TEXT,\
		lien TEXT,\
		nom TEXT,\
		telechargement TEXT,\
		commentaire TEXT);" 2> /dev/null

	fi

}

# -------------------------------------------
# vérifier si toutes les URLs sont valides
# $1 = fichier .dat
# -------------------------------------------
function check_urls() {

	# toutes les URLs sont valides
    local urls=0

	# boucle sur toutes les URLs dans le fichier .dat
    while read -r url_page; do

		# vérifier si la ligne n'est pas vide
		if [ -z "$url_page" ]; then
			break
		fi

		# vérifier si l'URL est valide
		if [[ $url_page =~ ^https?://.*$ ]]; then
			
			echo -n "$url_page : "

			# obtenir le statut de l'URL avec curl			
			status="$(curl -Is "$url_page" | head -1)"
			validate=( $status )

			# vérifier si l'URL est valide
			if [ "${validate[-2]}" == "200" ]; then
				echo -e "${GREEN}valid${NC}"
			else
				echo -e "${RED}not valid${NC}"
				# pas valide
				urls=1
			fi

		else

			echo -e "${RED}$url_page : bad url${NC}"

			# mauvaise URL	
			urls=1

		fi

	# boucle sur toutes les URLs du fichier .dat
    done < <(tail -n +4 "$1")

	# si au moins une URL n'est pas valide, retourne 1 sinon 0
    return $urls

}

# ------------------------------------------------------------
# fonction pour ajouter des fichiers .dat à la base de données
# ------------------------------------------------------------
function files_to_database() {

	# vérifier si le répertoire existe
	if [ -d "$DIR_DAT" ]; then

		echo -e "${YELLOW}check if all .dat files have been added to the database...${NC}"

		# boucle sur tous les fichiers .dat
		for file in "$DIR_DAT"/*.dat; do

			# lire les 3 premières lignes, et obtenir machine, téléverseur et extension
			exec 6< $file
			read machine <&6
			read televerseur <&6
			read extension <&6
			exec 6<&-

			# créer l'identifiant
			identifiant=$(echo $machine\_$televerseur)

			echo -ne "dat file ${PURPLE}$machine - $televerseur${NC} in database : "

			# datas_file = 0 n'est pas ajouté à la base de données
			datas_file=0

			# vérifier si le fichier .dat a été ajouté à la base de données
			# obtenir tous les identifiants dans la base de données
			identifiants=(`sqlite3 -batch $BDD_NOM "select identifiant from systemes"`)

			# vérifier si l'identifiant est dans la base de données
			for idents in "${identifiants[@]}"; do

				# identifiant trouvé, data_file = 1
			   	if [ $idents == $identifiant ]; then
					datas_file=1
					echo -e "${GREEN}ok${NC}"
					break
				fi

			done

			# data_file = 0, le fichier .dat n'a pas été ajouté à la base de données,
			# vérifier si toutes les URLs sont valides
			if [ $datas_file == 0 ]; then
			
				echo -e "${RED}no found, checking urls :${NC}"

				# obtenir le nombre de lignes dans le fichier .dat
				lines=$(wc -l < "$file")

				# vérifier si le fichier contient des liens
				if [ "$lines" -le 3 ]; then

					echo -e "${RED}no URLs found, the .dat file is not added to the database${NC}"
					datas_file=1

				else

					# le fichier contient au moins une URL,
					# vérification des URLs
					if check_urls $file; then
						echo -n "all urls are valid : "
					else
						echo -e "${RED}at least one URL is not valid, the .dat file is not added to the database${NC}"
						datas_file=1
					fi

				fi

			fi

			# data_file = 0, le fichier .dat n'a pas été ajouté à la base de données
			# et toutes les URL sont valides, le fichier peut être ajouté à la base de données
			if [ $datas_file == 0 ]; then

				echo -e "${YELLOW}searching for games...${NC}"

				# boucle sur toutes les URL
				tail -n +4 $file | while read url_page; do

					# vérifier si la ligne url_page n'est pas vide
					if [ -z "$url_page" ]; then
						break
					fi

					# insérer dans la table pages identifiant_systeme et lien
					sqlite3 -batch $BDD_NOM "\
					insert into pages (identifiant_systeme,lien) \
					values ('$identifiant','$url_page');" 2> /dev/null

					# extraire le dernier répertoire de l'URL
					echo -n "${url_page#*/*/*/*/} : "

					# obtenir tous les liens de jeux avec l'extension spécifiée contenus dans la page
					counter=0; while read url_jeu; do

						# extraire de url_jeu le nom du jeu
						[[ $url_jeu == *\'* ]] && url_jeu=$(echo $url_jeu | sed "s/'/''/g")
						nom_jeu=$(basename "$url_jeu" ".$extension")

						# insérer dans la table jeux lien_page, lien, nom, telechargement
						sqlite3 -batch $BDD_NOM "\
						insert into jeux (lien_page,lien,nom,telechargement) \
						values ('$url_page','$url_jeu','$nom_jeu','-');" 2> /dev/null

						# compter les jeux
						let counter++

					# obtenir tous les liens de jeux avec l'extension spécifiée contenus dans la page avec lynx
					done < <(lynx -dump -listonly -nonumbers $url_page | grep "\.${extension}$")

					echo -e "${GREEN}${counter} found${NC}"

				# boucle sur toutes les URL
				done

				# insérer dans la table systemes identifiant, machine, televerseur, extension
				sqlite3 -batch $BDD_NOM "\
				insert into systemes (identifiant,machine,televerseur,extension) \
				values ('$identifiant','$machine','$televerseur','$extension');" 2> /dev/null

			fi

		# boucle sur tous les fichiers .dat
		done

	fi

}

# ----
# main
# ----

# creation de la base de données et des tables
create_tables

# inserer les fichiers .dat dans la base de données
files_to_database
