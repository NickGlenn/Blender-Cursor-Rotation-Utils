from bpy.types import Operator, Context, Object, Mesh
from bpy.props import BoolProperty
from mathutils import Vector, Euler


def check_selection_mode(context: Context, vert=True, edge=False, face=False) -> bool:
    """Returns true if the context mode is EDIT_MESH and the specified elements are selected."""
    return context.mode == "EDIT_MESH" and tuple(context.scene.tool_settings.mesh_select_mode) == (vert, edge, face)


class SnapCursorToItem(Operator):
    bl_idname = "view3d.smart_snap_cursor_to_item"
    bl_label = "Smart Snap Cursor to Item"
    bl_description = "Snaps the cursor to the selected item(s), attempting to match averaged location and rotation (or normal)"
    bl_options = {"UNDO", "REGISTER"}

    set_location: BoolProperty(
        name="Set Location",
        description="Set the location of the cursor to match the averaged location of the selection",
        default=True,
    )

    set_rotation: BoolProperty(
        name="Set Rotation",
        description="Set the rotation of the cursor to match the averaged rotation or normal of the selection",
        default=True,
    )

    ignore_object_transform: BoolProperty(
        name="Ignore Object Transform",
        description="Transform of the object will be ignored - keep this unchecked to match visual location",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        obj: Object = context.active_object
        cursor = context.scene.cursor
        final_location = Vector()
        final_rotation = Euler()

        if context.mode == "OBJECT":
            final_location = obj.location
            final_rotation = obj.rotation_euler
        elif context.mode == "EDIT_MESH":
            obj.update_from_editmode()
            mesh: Mesh = obj.data

            verts = [v for v in mesh.vertices if v.select]
            edges = [e for e in mesh.edges if e.select]
            faces = [f for f in mesh.polygons if f.select]

            if len(verts) == 0:
                return {"CANCELLED"}

            vert_locations = [v.co for v in verts]
            final_location = sum(vert_locations, Vector()) / len(vert_locations)

            if len(faces) > 0 and check_selection_mode(context, face=True):
                normals = [f.normal for f in faces]
            elif len(edges) > 0 and check_selection_mode(context, edge=True):
                normals = [e.normal for e in edges]
            else:
                normals = [v.normal for v in verts]

            avg_normal = sum(normals, Vector()) / len(normals)
            final_rotation = avg_normal.to_track_quat("X", "Z").to_euler()
        elif context.mode == "EDIT_ARMATURE":
            bones = context.selected_bones

            if len(bones) == 0:
                return {"CANCELLED"}

            centers = [b.center for b in bones if b.select]
            avg_center = sum(centers, Vector()) / len(centers)

            final_location = avg_center

        elif context.mode == "POSE":
            bones = context.selected_pose_bones
            pass
        else:
            print("Unable to move cursor to location for current mode")
            return {"CANCELLED"}

        if context.mode != "OBJECT" and not self.ignore_object_transform:
            final_location = obj.location + final_location
            final_rotation.rotate(obj.rotation_euler)

        if self.set_location:
            cursor.location = final_location

        if self.set_rotation:
            cursor.rotation_euler = final_rotation

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "set_location")
        layout.prop(self, "set_rotation")

        if context.mode != "OBJECT":
            layout.prop(self, "ignore_object_transform")