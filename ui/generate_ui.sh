#! /bin/bash
echo "Generate UI"
pyuic5 -o evb1000viewer.py evb1000viewer.ui
echo "Generate Tag Widget"
pyuic5 -o tag_item_ui.py tag_item_ui.ui
echo "Generate Anchor Widget"
pyuic5 -o anchor_item_ui.py anchor_item_ui.ui
echo "Generate Plane Widget"
pyuic5 -o plane_height_setter_ui.py plane_height_setter_ui.ui
