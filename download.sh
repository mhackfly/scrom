#!/bin/bash

commande=$1
repertoire=$2
lien=$3

# Cette fonction execute la commande axel avec les options 
# -p -c -n $commande pour telecharger le fichier a l'adresse $lien
# dans le repertoire $repertoire.
# La commande est executee directement dans le repertoire $repertoire
# grace a la commande eval.
function exec_download() {
	str_cmd=$(echo "axel -p -c -n $commande" | tr -d '"')
	str_cmd+=" $lien"
	eval "(cd $repertoire && $str_cmd)"
}

exec_download
exit $?
