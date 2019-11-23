bl_info = {
    "name": "Zuotools",
    "author": "Zuorion",
    "version": (0, 1, 201910),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Zuotools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}

import bpy
from bpy.types import Menu
import bmesh

class MarkSmoothSharp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "edit.mark_smoothsharp"
    bl_label = "Mark Seam & Sharp"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        object = context.active_object
        return(object.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
    
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bpy.context.space_data.overlay.show_edge_sharp = True
        bpy.context.space_data.overlay.show_edge_seams = True
            
        selected = [e for e in bm.edges if e.select]
        if any(e.smooth == True for e in selected):
            for e in selected:
                e.smooth = False
                e.seam = True
        else:    
            for e in selected:
                e.smooth = True
                e.seam = False
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}

class VIEW3D_PT_view3d_itemname(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "Selected Item"

    @classmethod
    def poll(cls, context):
        return (context.space_data and context.active_object)

    def draw(self, context):
        layout = self.layout
        
        ob = context.active_object
        row = layout.row()
        row.label(text="", icon='OBJECT_DATA')
        row.prop(ob, "name", text="")
        
        if ob.type == 'MESH':
            layout.template_ID(ob, "data")
            split = layout.split()
            col = split.column()
            col.prop(ob, "show_wire", text="Wireframe")
            col.prop(ob, "show_all_edges")
            

        if ob.type == 'ARMATURE' and ob.mode in {'EDIT', 'POSE'}:
            bone = context.active_bone
            if bone:
                row = layout.row()
                row.label(text="", icon='BONE_DATA')
                row.prop(bone, "name", text="")
                
class VIEW3D_PT_view3d_itemcursor(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "3D Cursor"

    def draw(self, context):
        layout = self.layout

        cursor = context.scene.cursor

        layout.column().prop(cursor, "location", text="Location")
        rotation_mode = cursor.rotation_mode
        if rotation_mode == 'QUATERNION':
            layout.column().prop(cursor, "rotation_quaternion", text="Rotation")
        elif rotation_mode == 'AXIS_ANGLE':
            layout.column().prop(cursor, "rotation_axis_angle", text="Rotation")
        else:
            layout.column().prop(cursor, "rotation_euler", text="Rotation")
        layout.prop(cursor, "rotation_mode", text="")

class RAlignOrientationToSelection(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Align object's orientation to the selected elements."
    bl_idname = "object.ralign_orientation_to_selection"
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

class RAlignOrientationToSelectionWarning(bpy.types.Operator):

    bl_idname = "object.ralign_orientation_to_selection_warning"
    bl_label = "You can't change the orientation of multi-user objects."
    bl_options = {"UNDO", "INTERNAL"}

    #Trivia: Properties can be defined here in such a dialog. Example:
    #string_prop = bpy.props.StringProperty(name="String Prop")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(MarkSmoothSharp)
    bpy.utils.register_class(RAlignOrientationToSelection)
    bpy.utils.register_class(RAlignOrientationToSelectionWarning)
    bpy.utils.register_class(VIEW3D_PT_view3d_itemname)
    bpy.utils.register_class(VIEW3D_PT_view3d_itemcursor)

def unregister():
    bpy.utils.unregister_class(MarkSmoothSharp)
    bpy.utils.unregister_class(RAlignOrientationToSelection)
    bpy.utils.unregister_class(VIEW3D_PT_view3d_itemname)
    bpy.utils.unregister_class(VIEW3D_PT_view3d_itemcursor)

if __name__ == "__main__":
    register()
    
