# ##### BEGIN GPL LICENSE BLOCK #####
# yes, its gpl
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Volume to Clipboard",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "3D View > Search volume",
    "description": "Utilities for 3D printing",
    "tracker_url": "https://github.com/Zuorion/baddons",
    "doc_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "category": "Object",
}


import bpy
import bmesh

def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """Returns a transformed, triangulated copy of the mesh"""

    #assert obj.type == 'MESH'

    if apply_modifiers and obj.modifiers:
        import bpy
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        me = obj_eval.to_mesh()
        bm = bmesh.new()
        bm.from_mesh(me)
        obj_eval.to_mesh_clear()
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # TODO. remove all customdata layers.
    # would save ram

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm


class VolumeToClipboard(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.volumetoclipboard"
    bl_label = "Volume to Clipboard"
    bl_description = "Copy selectsd objects name and volumes to clipboard with format acceptable by excel"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        scene = context.scene
        unit = scene.unit_settings
        scale = 1.0 if unit.system == 'NONE' else unit.scale_length
        bpy.context.window_manager.clipboard = ""
        
        
        for ob in context.selected_objects:
            bm = bmesh_copy_from_object(ob, apply_modifiers=True)
            volume = bm.calc_volume()
            bm.free()
            
            bpy.context.window_manager.clipboard+=ob.name_full+";"+str(volume)+"\n"
        
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(VolumeToClipboard)


def unregister():
    bpy.utils.unregister_class(VolumeToClipboard)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.volumetoclipboard()
