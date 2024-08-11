#
# fichier généré par glade2py.sh
# le 15/04/2024 à 03:49:45
#
# liste des objets identifiés :
#
# GtkListStore
#     UI.list_store_combo_box_doublons
#     UI.list_store_combo_box_etats_jeux
#     UI.list_store_combo_box_sections_jeux
#     UI.list_store_tree_view_liste_jeux
#
# GtkTreeStore
#     UI.tree_store_tree_view_systemes
#
# GtkWindow
#     UI.window_scrom
#
# GtkLabel
#     UI.label_info_machine
#     UI.label_info_page
#     UI.label_info_jeux
#
# GtkTreeView
#     UI.tree_view_systemes
#     UI.tree_view_liste_jeux
#
# GtkTreeSelection
#     UI.tree_selection_systemes
#     UI.tree_selection_liste_jeux
#
# GtkTreeViewColumn
#     UI.tree_view_column_systemes
#     UI.tree_view_column_id
#     UI.tree_view_column_telechargements
#     UI.tree_view_column_noms
#     UI.tree_view_column_televerseurs
#
# GtkCellRendererText
#     UI.cell_renderer_systemes
#     UI.cell_renderer_doublons
#     UI.cell_renderer_sections_jeux
#     UI.cell_renderer_etats_jeux
#     UI.cell_renderer_id
#     UI.cell_renderer_telechargements
#     UI.cell_renderer_noms
#     UI.cell_renderer_televerseurs
#
# GtkTextView
#     UI.text_view_infos
#
# GtkButton
#     UI.button_page_precedente
#     UI.button_page_suivante
#     UI.button_arreter_telechargement
#     UI.button_telecharger
#     UI.button_quitter
#
# GtkComboBox
#     UI.combo_box_doublons
#     UI.combo_box_sections_jeux
#     UI.combo_box_etats_jeux
#
# GtkSearchEntry
#     UI.entry_recherches
#
# GtkEntry
#     UI.entry_lien_telechargement
#     UI.entry_commande_telechargement
#     UI.entry_repertoire_telechargement
#     UI.entry_repertoire_telechargement_systeme
#
# GtkProgressBar
#     UI.progress_bar_telechargement
#
# GtkCheckButton
#     UI.check_button_ajouter_repertoire_machine
#

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class UI: pass

class Glade:

    def __init__(self, glade_file):

        UI.builder = Gtk.Builder()
        if isinstance(glade_file, str):
            UI.builder.add_from_file(glade_file)
        else:
            UI.builder.add_from_file(glade_file.as_posix())

        #
        # GtkListStore
        #
        UI.list_store_combo_box_doublons = \
            UI.builder.get_object("list_store_combo_box_doublons")
        UI.list_store_combo_box_etats_jeux = \
            UI.builder.get_object("list_store_combo_box_etats_jeux")
        UI.list_store_combo_box_sections_jeux = \
            UI.builder.get_object("list_store_combo_box_sections_jeux")
        UI.list_store_tree_view_liste_jeux = \
            UI.builder.get_object("list_store_tree_view_liste_jeux")

        #
        # GtkTreeStore
        #
        UI.tree_store_tree_view_systemes = \
            UI.builder.get_object("tree_store_tree_view_systemes")

        #
        # GtkWindow
        #
        UI.window_scrom = \
            UI.builder.get_object("window_scrom")

        #
        # GtkLabel
        #
        UI.label_info_machine = \
            UI.builder.get_object("label_info_machine")
        UI.label_info_page = \
            UI.builder.get_object("label_info_page")
        UI.label_info_jeux = \
            UI.builder.get_object("label_info_jeux")

        #
        # GtkTreeView
        #
        UI.tree_view_systemes = \
            UI.builder.get_object("tree_view_systemes")
        UI.tree_view_liste_jeux = \
            UI.builder.get_object("tree_view_liste_jeux")

        #
        # GtkTreeSelection
        #
        UI.tree_selection_systemes = \
            UI.builder.get_object("tree_selection_systemes")
        UI.tree_selection_liste_jeux = \
            UI.builder.get_object("tree_selection_liste_jeux")

        #
        # GtkTreeViewColumn
        #
        UI.tree_view_column_systemes = \
            UI.builder.get_object("tree_view_column_systemes")
        UI.tree_view_column_id = \
            UI.builder.get_object("tree_view_column_id")
        UI.tree_view_column_telechargements = \
            UI.builder.get_object("tree_view_column_telechargements")
        UI.tree_view_column_noms = \
            UI.builder.get_object("tree_view_column_noms")
        UI.tree_view_column_televerseurs = \
            UI.builder.get_object("tree_view_column_televerseurs")

        #
        # GtkCellRendererText
        #
        UI.cell_renderer_systemes = \
            UI.builder.get_object("cell_renderer_systemes")
        UI.cell_renderer_doublons = \
            UI.builder.get_object("cell_renderer_doublons")
        UI.cell_renderer_sections_jeux = \
            UI.builder.get_object("cell_renderer_sections_jeux")
        UI.cell_renderer_etats_jeux = \
            UI.builder.get_object("cell_renderer_etats_jeux")
        UI.cell_renderer_id = \
            UI.builder.get_object("cell_renderer_id")
        UI.cell_renderer_telechargements = \
            UI.builder.get_object("cell_renderer_telechargements")
        UI.cell_renderer_noms = \
            UI.builder.get_object("cell_renderer_noms")
        UI.cell_renderer_televerseurs = \
            UI.builder.get_object("cell_renderer_televerseurs")

        #
        # GtkTextView
        #
        UI.text_view_infos = \
            UI.builder.get_object("text_view_infos")

        #
        # GtkButton
        #
        UI.button_page_precedente = \
            UI.builder.get_object("button_page_precedente")
        UI.button_page_suivante = \
            UI.builder.get_object("button_page_suivante")
        UI.button_arreter_telechargement = \
            UI.builder.get_object("button_arreter_telechargement")
        UI.button_telecharger = \
            UI.builder.get_object("button_telecharger")
        UI.button_quitter = \
            UI.builder.get_object("button_quitter")

        #
        # GtkComboBox
        #
        UI.combo_box_doublons = \
            UI.builder.get_object("combo_box_doublons")
        UI.combo_box_sections_jeux = \
            UI.builder.get_object("combo_box_sections_jeux")
        UI.combo_box_etats_jeux = \
            UI.builder.get_object("combo_box_etats_jeux")

        #
        # GtkSearchEntry
        #
        UI.entry_recherches = \
            UI.builder.get_object("entry_recherches")

        #
        # GtkEntry
        #
        UI.entry_lien_telechargement = \
            UI.builder.get_object("entry_lien_telechargement")
        UI.entry_commande_telechargement = \
            UI.builder.get_object("entry_commande_telechargement")
        UI.entry_repertoire_telechargement = \
            UI.builder.get_object("entry_repertoire_telechargement")
        UI.entry_repertoire_telechargement_systeme = \
            UI.builder.get_object("entry_repertoire_telechargement_systeme")

        #
        # GtkProgressBar
        #
        UI.progress_bar_telechargement = \
            UI.builder.get_object("progress_bar_telechargement")

        #
        # GtkCheckButton
        #
        UI.check_button_ajouter_repertoire_machine = \
            UI.builder.get_object("check_button_ajouter_repertoire_machine")

