import bpy
from bpy.types import Operator
from bpy.props import BoolProperty


class SnapItemToCursor(Operator):
    bl_idname = "view3d.smart_snap_item_to_cursor"
    bl_label = "Smart Snap Item to Cursor"
    bl_description = "Snaps the selected item(s) to the cursor, matching both location and rotation"
    bl_options = {"UNDO", "REGISTER"}

    set_location: BoolProperty(
        name="Set Location",
        description="Set the selection location to match the cursor's location",
        default=True,
    )

    set_rotation: BoolProperty(
        name="Set Rotation",
        description="Set the selection rotation to match the cursor's rotation",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        cursor = context.scene.cursor

        if context.mode == "OBJECT":
            for obj in context.selected_objects:
                obj.location = cursor.location
                obj.rotation_euler = cursor.rotation_euler

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "set_location")
        layout.prop(self, "set_rotation")