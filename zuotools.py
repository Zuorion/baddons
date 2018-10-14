bl_info = {
    "name": "Zuotools",
    "author": "Zuorion",
    "version": (0, 1, 20180812),
    "blender": (2, 7, 9, 5),
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
        me.show_edge_sharp = True
        me.show_edge_seams = True
            
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

class VIEW3D_MT_edit_mesh_zuoedges(Menu):
    bl_label = "ZEdge Data"
    bl_idname = "VIEW3D_MT_edit_mesh_zuoedges"

    def draw(self, context):
        layout = self.layout

        with_freestyle = bpy.app.build_options.freestyle

        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("transform.edge_crease")
        layout.operator("transform.edge_bevelweight")

        layout.separator()

        layout.operator("mesh.mark_seam", text="(A) Mark Seam").clear = False
        layout.operator("mesh.mark_seam", text="(Q) Clear Seam").clear = True

        layout.separator()

        layout.operator("mesh.mark_sharp", text="(S) Mark Sharp")
        layout.operator("mesh.mark_sharp", text="(W) Clear Sharp").clear = True

        layout.separator()
        
        self.layout.operator( "edit.mark_smoothsharp", "(D) Mark Smoot'n'Sharp" )
        layout.separator()

        if with_freestyle:
            layout.operator("mesh.mark_freestyle_edge").clear = False
            layout.operator("mesh.mark_freestyle_edge", text="Clear Freestyle Edge").clear = True
            layout.separator()        
        

    
def register():
    bpy.utils.register_class(MarkSmoothSharp)
    bpy.utils.register_class(VIEW3D_MT_edit_mesh_zuoedges)
    

def unregister():
    bpy.utils.unregister_class(MarkSmoothSharp)
    bpy.utils.unregister_class(VIEW3D_MT_edit_mesh_zuoedges)
    

if __name__ == "__main__":
    register()
    