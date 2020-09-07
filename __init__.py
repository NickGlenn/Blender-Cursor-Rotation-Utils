import bpy
from bpy.types import UILayout, VIEW3D_MT_snap, VIEW3D_MT_object_context_menu

from .op_rotate_item_to_cursor import RotateItemToCursor
from .op_rotate_cursor_to_item import RotateCursorToWorld, RotateCursorToItem

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
    "name": "Cursor Rotation",
    "author": "Nick Glenn",
    "description": "Small, but useful cursor utility for Blender",
    "version": (2020, 1, 0),
    "blender": (2, 80, 0),
    "url": "https://github.com/nickglenn/blender-magic-cursor",
    "location": "View3D",
    "support": "COMMUNITY",
    "warning": "",
    "category": "Generic"
}


classes = (
    RotateItemToCursor,
    RotateCursorToWorld,
    RotateCursorToItem,
)


def menu(self, context):
    layout: UILayout = self.layout
    layout.separator()
    layout.operator(RotateCursorToWorld.bl_idname, text="Orient Cursor to World Origin")
    layout.operator(RotateCursorToItem.bl_idname, text="Orient Cursor to Selected")


def register():
    for c in classes:
        bpy.utils.register_class(c)

    VIEW3D_MT_snap.append(menu)


def unregister():
    VIEW3D_MT_snap.remove(menu)

    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
