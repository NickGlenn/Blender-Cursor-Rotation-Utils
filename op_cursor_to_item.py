import bpy
from bpy.types import Operator, Context
from bpy.props import BoolProperty


class SnapCursorToItem(Operator):
    bl_idname = "view3d.smart_snap_cursor_to_item"
    bl_label = "(Smart) Snap Cursor to Item"
    bl_description = "Snaps the cursor to the selected item(s), attempting to match averaged location and rotation (or normal)"
    bl_options = {"UNDO", "REGISTER"}

    ignore_object_transform: BoolProperty(
        name="Ignore Object Transform",
        description="Transform of the object will be ignored - keep this unchecked to match visual location",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.view3d.rotate_cursor_to_item(ignore_object_transform=self.ignore_object_transform)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        if context.mode != "OBJECT":
            layout.prop(self, "ignore_object_transform")