from bpy.types import Operator, Context, Object, Mesh
from bpy.props import BoolProperty
from mathutils import Vector, Euler


def check_selection_mode(context: Context, vert=True, edge=False, face=False) -> bool:
    """Returns true if the context mode is EDIT_MESH and the specified elements are selected."""
    return context.mode == "EDIT_MESH" and tuple(context.scene.tool_settings.mesh_select_mode) == (vert, edge, face)


class RotateCursorToWorld(Operator):
    bl_idname = "view3d.rotate_cursor_to_world"
    bl_label = "Rotate Cursor to World Origin"
    bl_description = "Orients the cursor back to a euler value of 0, 0, 0"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cursor = context.scene.cursor
        cursor.rotation_euler = (0, 0, 0)
        return {"FINISHED"}


class RotateCursorToItem(Operator):
    bl_idname = "view3d.rotate_cursor_to_selected"
    bl_label = "Rotate Cursor to Selected"
    bl_description = "Orients the cursor to match the selected object(s) rotation or normal"
    bl_options = {"UNDO", "REGISTER"}

    ignore_object_transform: BoolProperty(
        name="Ignore Object Transform",
        description="Transform of the object will be ignored - keep this unchecked to match visual location",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = context.active_object
        cursor = context.scene.cursor

        if context.mode == "OBJECT":
            if obj is not None:
                final_rotation = obj.rotation_euler
            else:
                final_rotation = Euler()  # back to world center

        elif context.mode == "EDIT_MESH":
            obj.update_from_editmode()
            mesh: Mesh = obj.data

            verts = [v for v in mesh.vertices if v.select]
            edges = [e for e in mesh.edges if e.select]
            faces = [f for f in mesh.polygons if f.select]

            if len(verts) == 0:
                return {"CANCELLED"}

            if len(faces) > 0 and check_selection_mode(context, face=True):
                normals = [f.normal for f in faces]
            elif len(edges) > 0 and check_selection_mode(context, edge=True):
                normals = [e.normal for e in edges]
            else:
                normals = [v.normal for v in verts]

            avg_normal = sum(normals, Vector()) / len(normals)
            final_rotation = avg_normal.to_track_quat("Z", "X").to_euler()

        elif context.mode == "EDIT_ARMATURE":
            bones = context.selected_bones

            if len(bones) == 0:
                return {"CANCELLED"}

        elif context.mode == "POSE":
            bones = context.selected_pose_bones
            pass
        else:
            print("Unable to move cursor to location for current mode")
            return {"CANCELLED"}

        if context.mode != "OBJECT" and not self.ignore_object_transform:
            final_rotation.rotate(obj.rotation_euler)

        cursor.rotation_euler = final_rotation

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        if context.mode != "OBJECT":
            layout.prop(self, "ignore_object_transform")
