bl_info = {
    "name": "Align Orientation To Selection",
    "author": "Zuorion",
    "version": (0, 1, 20200203),
    "blender": (2, 81, 0),
    "location": "Mesh > Snap",
    "description": "AlignOrientationToSelection",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}

import bpy
from bpy.types import Menu
import bmesh

class AlignOrientationToSelection(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Align object's orientation to the selected elements."
    bl_idname = "mesh.ralign_orientation_to_selection"
    bl_label = "Align Orientation To Selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        obj_type = obj.type
        return(obj and obj_type in {'MESH'})

    def execute(self, context):

        selected = context.selected_objects
        obj = context.active_object
        objects = bpy.data.objects
                
        #Create custom orientation
        prev_orientation = bpy.context.scene.transform_orientation_slots[0].type
        bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'
        bpy.ops.transform.create_orientation(name="rOrientation", use=True, overwrite=True)

        #Exit to Object Mode
        bpy.ops.object.editmode_toggle()
        
        utdo = bpy.context.scene.tool_settings.use_transform_data_origin

        #Add empty aligned to the orientation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.context.scene.tool_settings.use_transform_data_origin = True
        bpy.ops.transform.transform(mode='ALIGN', value=(0, 0, 0, 0), orient_type='rOrientation', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        #Restore settings and editmode
        bpy.ops.transform.delete_orientation()
        bpy.context.scene.transform_orientation_slots[0].type = prev_orientation 
        bpy.context.scene.tool_settings.use_transform_data_origin = utdo
        bpy.ops.object.editmode_toggle()


        return {'FINISHED'}
        
def addmenu_callback(self, context):
    self.layout.operator("mesh.ralign_orientation_to_selection", text="Origin Orientation To Selection",
                        icon='PIVOT_CURSOR')

def register():
    bpy.utils.register_class(AlignOrientationToSelection)
    bpy.types.VIEW3D_MT_snap.append(addmenu_callback)

def unregister():
    bpy.utils.unregister_class(AlignOrientationToSelection)
    bpy.types.VIEW3D_MT_snap.remove(addmenu_callback)

if __name__ == "__main__":
    register()
    
