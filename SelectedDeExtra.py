# ##### BEGIN GPL LICENSE BLOCK #####
# yes, its gpl
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Select DeExtra",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "3D View > Select",
    "description": "Extra Select options",
    "tracker_url": "https://github.com/Zuorion/baddons",
    "doc_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "category": "Object",
}

import bpy
import bmesh
import bpy
import numpy as np

Direction_Items =(
    ('MORE', "More", ""),
    ('LESS', "Less", "")
)

DELIMIT_ITEMS = (
    ('NORMAL', "Normal", ""),
    ('MATERIAL', "Material", ""),
    ('SEAM', "Seam", ""),
    ('SHARP', "Sharp", ""),
    ('UV', "UVs", ""),
)

def store_face_select(context, dic_f):
    for o in bpy.context.objects_in_mode:
        dic_f.update( {o : []} )
        bm = bmesh.from_edit_mesh(o.data)
        for f in bm.faces:
            if f.select:
                dic_f[o].append(f.index)
    return dic_f

def restore_face_select(context, dic_f):
    if dic_f:
        for o in dic_f:
            bm = bmesh.from_edit_mesh(o.data)
            bm.faces.ensure_lookup_table()
            for f in dic_f[o]:
                bm.faces[f].select = True 
                
            bmesh.update_edit_mesh(o.data, True)
    
def dict_intersect(*dicts):
    comm_keys = dicts[0].keys()
    for d in dicts[1:]:
        # intersect keys first
        comm_keys &= d.keys()
    # then build a result dict with nested comprehension
    result = {key:{d[key] for d in dicts} for key in comm_keys}
    return result
    
    
    
class SelectFlatDeex(bpy.types.Operator):
    bl_idname = "mesh.select_flat_deex"
    bl_label = "Flat Select Delimited"
    bl_options = {'REGISTER', 'UNDO'}

    extend: bpy.props.BoolProperty(options={'HIDDEN', 'SKIP_SAVE'})
    deselect: bpy.props.BoolProperty(options={'HIDDEN', 'SKIP_SAVE'})
    
    sharpness: bpy.props.FloatProperty(
        name="Sharpness", description="Sharpness",
        subtype='ANGLE',
        default=0.0872664626, min=0, soft_min=0.017453, max=3.141593,
        step=100, options={'SKIP_SAVE'})
    delimit: bpy.props.EnumProperty(
        name="Delimit",
        description="Delimit selected region",
        items=DELIMIT_ITEMS,
        default={"SEAM"},
        options={'ENUM_FLAG'})
    delimit_global: bpy.props.BoolProperty(name="Flip delimit order", default=False,
        description="Delimit globally selected region")
        
    def execute(self, context):
        oryginalselect = {}
        oryginalhidden = {}
        finalselect = {}
        store_face_select(context, oryginalselect)
        
        bpy.ops.mesh.select_all(action='DESELECT')  
        bpy.ops.mesh.reveal(select=True)
        store_face_select(context, oryginalhidden)
        bpy.ops.mesh.hide(unselected=False)

        restore_face_select(context, oryginalselect)  
        
        if self.delimit_global:
            bpy.ops.mesh.select_linked(delimit=self.delimit)
            bpy.ops.mesh.hide(unselected=True)
        else:
            bpy.ops.mesh.faces_select_linked_flat(sharpness=self.sharpness)
            bpy.ops.mesh.hide(unselected=True)
            
        bpy.ops.mesh.select_all(action='DESELECT')    
        
        restore_face_select(context, oryginalselect)               
        
        if self.delimit_global:
            bpy.ops.mesh.faces_select_linked_flat(sharpness=self.sharpness)
            bpy.ops.mesh.reveal(select=False)
        else:
            bpy.ops.mesh.select_linked(delimit=self.delimit)
            bpy.ops.mesh.reveal(select=False)
            
        store_face_select(context, finalselect)
        
        bpy.ops.mesh.select_all(action='DESELECT')   
        bpy.ops.mesh.reveal()
        restore_face_select(context, oryginalhidden)   
        bpy.ops.mesh.hide(unselected=False)
        restore_face_select(context, finalselect)   
        
        return {'FINISHED'}

class SelectMoreDeex(bpy.types.Operator):
    bl_idname = "mesh.select_more_deex"
    bl_label = "Select More Delimited"
    bl_options = {'REGISTER', 'UNDO'}
    
    direction: bpy.props.EnumProperty(
        name="Direction",
        description="Delimit selected region",
        items=Direction_Items,
        default='MORE'
        )
        
    delimit: bpy.props.EnumProperty(
        name="Delimit",
        description="Delimit selected region",
        items=DELIMIT_ITEMS,
        default={"SEAM"},
        options={'ENUM_FLAG'})
        
    flip_order: bpy.props.BoolProperty(name="Flip delimit order", default=False,
        description="Delimit globally selected region")
        
    use_face_step: bpy.props.BoolProperty(name="Face Step", default=True,
        description="Delimit globally selected region")
    
    def execute(self, context):
        oryginalselect = {}
        oryginalhidden = {}
        finalselect = {}
        store_face_select(context, oryginalselect)
        
        bpy.ops.mesh.select_all(action='DESELECT')  
        bpy.ops.mesh.reveal(select=True)
        store_face_select(context, oryginalhidden)
        bpy.ops.mesh.hide(unselected=False)
        
        restore_face_select(context, oryginalselect)  
        
        if self.flip_order:
            bpy.ops.mesh.select_linked(delimit=self.delimit)
            bpy.ops.mesh.hide(unselected=True)
        else:
            if self.direction == 'MORE':
                bpy.ops.mesh.select_more(use_face_step=self.use_face_step)
            else:
                bpy.ops.mesh.select_less(use_face_step=self.use_face_step)
            bpy.ops.mesh.hide(unselected=True)
            
        bpy.ops.mesh.select_all(action='DESELECT')    
        
        restore_face_select(context, oryginalselect)               
        
        if self.flip_order:
            if self.direction == 'MORE':
                bpy.ops.mesh.select_more(use_face_step=self.use_face_step)
            else:
                bpy.ops.mesh.select_less(use_face_step=self.use_face_step)
            bpy.ops.mesh.reveal(select=False)
        else:
            bpy.ops.mesh.select_linked(delimit=self.delimit)
            bpy.ops.mesh.reveal(select=False)
            
        store_face_select(context, finalselect)
        
        bpy.ops.mesh.select_all(action='DESELECT')   
        bpy.ops.mesh.reveal()
        restore_face_select(context, oryginalhidden)   
        bpy.ops.mesh.hide(unselected=False)
        restore_face_select(context, finalselect)   
        return {'FINISHED'}
        
        
def selectsimilarsmenu_callback(self, context):
    self.layout.operator("mesh.select_more_deex", text ='Select More Delimited').direction='MORE'
    self.layout.operator("mesh.select_more_deex", text ='Select Less Delimited').direction='LESS'

def selectlinkedsmenu_callback(self, context):
    self.layout.operator("mesh.select_flat_deex", text ='Select More Delimited')
    

def register():
    bpy.utils.register_class(SelectFlatDeex)
    bpy.utils.register_class(SelectMoreDeex)
    
    bpy.types.VIEW3D_MT_edit_mesh_select_more_less.append(selectsimilarsmenu_callback)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.append(selectlinkedsmenu_callback)


def unregister():
    bpy.utils.unregister_class(SelectFlatDeex)
    bpy.utils.unregister_class(SelectMoreDeex)
    
    bpy.types.VIEW3D_MT_edit_mesh_select_more_less.remove(selectsimilarsmenu_callback)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.remove(selectlinkedsmenu_callback)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.volumetoclipboard()
