import bpy
from bpy.types import UILayout, VIEW3D_MT_snap, VIEW3D_MT_object_context_menu

from .op_item_to_cursor import SnapItemToCursor
from .op_cursor_to_item import SnapCursorToItem

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Smart Cursor",
    "author": "Nick Glenn",
    "description": "Small, but powerful cursor utility for Blender",
    "version": (2020, 1, 0),
    "blender": (2, 80, 0),
    "url": "https://github.com/nickglenn/blender-magic-cursor",
    "location": "View3D",
    "support": "COMMUNITY",
    "warning": "",
    "category": "Generic"
}


classes = (
    SnapCursorToItem,
    SnapItemToCursor,
)


def menu(self, context):
    layout: UILayout = self.layout
    layout.separator()
    layout.operator(SnapCursorToItem.bl_idname, text="(Smart) Cursor to Selected")
    layout.operator(SnapItemToCursor.bl_idname, text="(Smart) Selected to Cursor")


def register():
    for c in classes:
        bpy.utils.register_class(c)

    VIEW3D_MT_snap.append(menu)


def unregister():
    VIEW3D_MT_snap.remove(menu)

    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
