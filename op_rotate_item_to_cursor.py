import bpy
from bpy.types import Operator
from bpy.props import BoolProperty


class RotateItemToCursor(Operator):
    bl_idname = "view3d.rotate_item_to_cursor"
    bl_label = "Rotate Item to Cursor"
    bl_description = "Orients the selected item(s) to match the current rotation of the 3D cursor"
    bl_options = {"UNDO", "REGISTER"}

    active_only: BoolProperty(
        name="Active Only",
        description="When enabled, only the active object or item will be rotated",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        cursor = context.scene.cursor

        if context.mode == "OBJECT":
            selected = [context.active_object] if self.active_only else context.selected_objects
            for obj in selected:
                obj.rotation_euler = cursor.rotation_euler

        return {"FINISHED"}

    def draw(self, context):
        if context.mode == "OBJECT":
            self.layout.prop(self, "active_only")