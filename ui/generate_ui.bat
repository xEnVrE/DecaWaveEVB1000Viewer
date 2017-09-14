@ECHO OFF
ECHO Generate UI
pyuic5 -o evb1000viewer.py evb1000viewer.ui
ECHO Generate Tag Widget
pyuic5 -o tag_item_ui.py tag_item_ui.ui
ECHO Generate Anchor Widget
pyuic5 -o anchor_item_ui.py anchor_item_ui.ui
ECHO Generate Plane Widget
pyuic5 -o plane_height_setter_ui.py plane_height_setter_ui.ui
