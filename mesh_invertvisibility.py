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
    "name": "Invert hidden",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "Ctrl+Alt+H",
    "description": "Invert hide operator",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }



import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty, EnumProperty
import rna_keymap_ui

class ObjectInvertHidden(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.invert_visibility"
    bl_label = "Invert hidden"
    bl_description = "Hide currently visible objects and reveals previously visible."
    bl_options = {'REGISTER', 'UNDO'}
    
    selectafter : BoolProperty(
        name="Select", default=True,
        description="Select revealed objects.")
    
    def execute(self, context):
        selected_obj = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        
        if context.mode =='EDIT_MESH':
            bpy.ops.object.editmode_toggle()

        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.hide_view_clear()
        bpy.ops.object.hide_view_set(unselected=True)
        
        if not self.selectafter:
            bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}
        
class MeshInvertHidden(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.invert_visibility"
    bl_label = "Invert hidden"
    bl_description = "Hide currently visible mesh and reveals previously visible."
    bl_options = {'REGISTER', 'UNDO'}
    
        
    selectafter : BoolProperty(
        name="Select", default=True,
        description="Select revealed mesh")
    
    @classmethod
    def poll(cls, context): 
        return context.mode =='EDIT_MESH'

    def execute(self, context):
        #act = context.scene.act
            
        selected_obj = bpy.context.selected_objects
        active_obj = bpy.context.active_object
        
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.hide(unselected=True)
        
        if not self.selectafter:
            bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}

def addobjmenu_callback(self, context):
    self.layout.operator("object.invert_visibility")
    
def addeditmenu_callback(self, context):
    self.layout.operator("mesh.invert_visibility")
  

def get_hotkey_entry_item(km, kmi_name):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            return km_item
    return None

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    def addtomenuupdate(self, context):
        if self.addtomenu:
            bpy.types.VIEW3D_MT_edit_mesh_showhide.append(addeditmenu_callback)
            bpy.types.VIEW3D_MT_object_showhide.append(addobjmenu_callback)
        else:
            bpy.types.VIEW3D_MT_edit_mesh_showhide.remove(addeditmenu_callback)
            bpy.types.VIEW3D_MT_object_showhide.remove(addeditmenu_callback)
        return
    
    addtomenu: BoolProperty(
        name="Show in menu",
        description="Add opertors to Editmode:Mesh>Show/Hide and Objectmod:Object>show/hide menu.",
        default=True,
        update=addtomenuupdate
    )
    
    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        
        box = layout.box()
        row = box.row()
        row.prop(self, "addtomenu", text="Show in menus")
        
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text='Hotkey')
        col.separator()
        kc = wm.keyconfigs.user
        km = kc.keymaps['Object Mode']
        col.label(text='Object Mode')
        kmi = get_hotkey_entry_item(km, 'object.invert_visibility')
        col.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        
        km = kc.keymaps['Mesh']
        col.label(text='Hotkey')
        kmi = get_hotkey_entry_item(km, 'mesh.invert_visibility')
        col.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)


addon_keymaps = []

def register():
    bpy.utils.register_class(ObjectInvertHidden)
    bpy.utils.register_class(MeshInvertHidden)
    bpy.utils.register_class(AddonPreferences)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # As Ctrl + Alt + H
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
        kmi = km.keymap_items.new('object.invert_visibility', 'H', 'PRESS', ctrl=True, alt=True)
        
        
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('mesh.invert_visibility', 'H', 'PRESS', ctrl=True, alt=True)
        addon_keymaps.append((km, kmi))
        
    bpy.types.VIEW3D_MT_edit_mesh_showhide.append(addeditmenu_callback)
    bpy.types.VIEW3D_MT_object_showhide.append(addobjmenu_callback)


def unregister():
    bpy.utils.unregister_class(ObjectInvertHidden)
    bpy.utils.unregister_class(MeshInvertHidden)
    bpy.utils.unregister_class(AddonPreferences)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.types.VIEW3D_MT_edit_mesh_showhide.remove(addobjmenu_callback)
    bpy.types.VIEW3D_MT_object_showhide.remove(addeditmenu_callback)
    

if __name__ == "__main__":
    register()
