@echo off
pyuic5 ui/main_ui.ui -o ui/main_ui.py
pyuic5 ui/edit_ui.ui -o ui/edit_ui.py
pyuic5 ui/create_delete_ui.ui -o ui/create_delete_ui.py
pyuic5 ui/batch_edit_ui.ui -o ui/batch_edit_ui.py
pyuic5 ui/create_ui.ui -o ui/create_ui.py