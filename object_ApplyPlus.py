# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Apply Plus",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "Apply menu",
    "description": "Apply operator with additional options",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }



import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty, EnumProperty
import rna_keymap_ui

class ApplyScalePlus(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.applyscaleplus"
    bl_label = "Apply Scale"
    bl_description = "Apply scale perseving visual normals."
    bl_options = {'REGISTER', 'UNDO'}
    
    
    flipodd : BoolProperty(
        name="Flip normals", default=True,
        description="Flip normals of objects with odd number of negative scales")
        
    makesingle : BoolProperty(
        name="Make single user", default=False,
        description="Make mesh single user to not modify unselected objects")
    
    @classmethod
    def poll(cls, context): 
        return context.active_object is not None

    def execute(self, context):
        #act = context.scene.act
            
        selected_obj = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        
        #Make mesh single user to not modify unselected objects
        if self.makesingle:
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', obdata=True)
        #TODO: keep nonsingle inside selected
        
            
        #pre-flipping scalefliped normals
        if self.flipodd == True:
            for x in selected_obj:
                bpy.ops.object.select_all(action='DESELECT')
                x.select_set(True)
                
                if x.type == 'MESH' and (x.scale[0] * x.scale[1] * x.scale[2]) < 0:
                    bpy.context.view_layer.objects.active = x
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.reveal()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    
                    
        for j in selected_obj:
            j.select_set(True)
        
        bpy.context.view_layer.objects.active = active_obj
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        
        
        return {'FINISHED'}

def addmenu_callback(self, context):
    self.layout.operator("object.applyscaleplus", text="Scale+")

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    def addtomenuupdate(self, context):
        if self.addtomenu:
            bpy.types.VIEW3D_MT_object_apply.append(addmenu_callback)
        else:
            bpy.types.VIEW3D_MT_object_apply.remove(addmenu_callback)
        return
    
    addtomenu: BoolProperty(
        name="Apply menu",
        description="Show opertor in 3dView's apply menu",
        default=True,
        update=addtomenuupdate
    )
    
    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        
        b = layout.box()
        row = b.row()
        row.prop(self, "addtomenu", text="Add to Menu")
        



def register():
    bpy.utils.register_class(ApplyScalePlus)
    bpy.utils.register_class(AddonPreferences)

    bpy.types.VIEW3D_MT_object_apply.append(addmenu_callback)  
    


def unregister():
    bpy.utils.unregister_class(ApplyScalePlus)
    bpy.utils.unregister_class(AddonPreferences)
    
    bpy.types.VIEW3D_MT_object_apply.remove(addmenu_callback)

if __name__ == "__main__":
    register()
