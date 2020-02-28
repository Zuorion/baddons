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
    "name": "Join Plus",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "Ctrl+J",
    "description": "Join operator with additional options",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }



import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty, EnumProperty
import rna_keymap_ui

class JoinPlus(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.joinplus"
    bl_label = "Join+"
    bl_description = "Join selected objects into active object."
    bl_options = {'REGISTER', 'UNDO'}
    
    uvmethod: EnumProperty(name="UV merge", 
        items=[('name', "by Name", "Merge UV channels if name mach or add as new"),
               ('order', "by Order", "Merge UV channels by order")],
               default='order')
    
    flipodd : BoolProperty(
        name="Flip normals", default=True,
        description="Flip normals of objects with odd number of negative scales")
        
    applymesh : BoolProperty(
        name="Apply mesh", default=True,
        description="Convert selected objects to mesh (apply modifiers)")
    
    @classmethod
    def poll(cls, context): 
        return context.active_object is not None

    def execute(self, context):
        #act = context.scene.act
            
        selected_obj = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        
        #Make mesh single user to not modify unselected objects
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', obdata=True)
        
        if self.applymesh:
            bpy.ops.object.convert(target='MESH')
            
        #Sync UV names by Order
        if self.uvmethod=='order':
            for x in selected_obj:
                if x.type != 'MESH':
                    continue
                a_uvs=len(active_obj.data.uv_layers)
                x_uvs=len(x.data.uv_layers)
                print(a_uvs)
                if x_uvs > 0:
                    for uv_index in range(0, max(a_uvs,x_uvs)):
                        if a_uvs > uv_index:
                            if x_uvs > uv_index:
                                x.data.uv_layers[uv_index].name = active_obj.data.uv_layers[uv_index].name
                        else:
                            #active have lower UVmap count
                            bpy.context.view_layer.objects.active = active_obj
                            bpy.ops.mesh.uv_texture_add()
                            active_obj.data.uv_layers[uv_index].name = x.data.uv_layers[uv_index].name
        
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
        bpy.ops.object.join()
        
        
        return {'FINISHED'}

def addmenu_callback(self, context):
    self.layout.operator("object.joinplus", text="JoinPlus")


def get_hotkey_entry_item(km, kmi_name):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            return km_item
    return None

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    def addtomenuupdate(self, context):
        if self.addtomenu:
            bpy.types.VIEW3D_MT_object.append(addmenu_callback)
        else:
            bpy.types.VIEW3D_MT_object.remove(addmenu_callback)
        return
    
    addtomenu: BoolProperty(
        name="Object menu",
        description="Show opertor in 3dView's Object menu",
        default=False,
        update=addtomenuupdate
    )
    
    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        
        box = layout.box()
        row = box.row()
        row.prop(self, "addtomenu", text="Add Join+ to 3dView>Object mode>Object menu")
        
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text='Hotkey')
        col.separator()
        kc = wm.keyconfigs.user
        km = kc.keymaps['Object Mode']
        kmi = get_hotkey_entry_item(km, 'object.joinplus')
        col.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)


addon_keymaps = []

def register():
    bpy.utils.register_class(JoinPlus)
    bpy.utils.register_class(AddonPreferences)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # As Ctrl + J
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
        kmi = km.keymap_items.new('object.joinplus', 'J', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))
        
    


def unregister():
    bpy.utils.unregister_class(JoinPlus)
    bpy.utils.unregister_class(AddonPreferences)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.types.VIEW3D_MT_object.remove(addmenu_callback)

if __name__ == "__main__":
    register()
