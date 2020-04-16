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
    "name": "Select Current",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "Sequencer>Select menu, Shift+S",
    "description": "Select currently visible strips in sequencer",
    "warning": "",
    "wiki_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "category": "Sequencer",
    }



import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty, EnumProperty
import rna_keymap_ui

class SequencerSelectCurrent(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "sequencer.select_current"
    bl_label = "Select current"
    bl_description = "Sellects currently visible strips."
    bl_options = {'REGISTER', 'UNDO'}
    


    def execute(self, context):
        bpy.ops.screen.frameo_ffset(delta=-1)
        bpy.ops.sequencer.select(left_right='LEFT', linked_time=True)
        bpy.ops.screen.frame_offset(delta=2)
        bpy.ops.sequencer.select(left_right='RIGHT', extend=True, linked_time=True)
        bpy.ops.screen.frame_offset(delta=-1)
        bpy.ops.sequencer.select_all(action='INVERT')

        
        return {'FINISHED'}

def addmenu_callback(self, context):
    self.layout.operator("sequencer.select_current", text="Select current")


def get_hotkey_entry_item(km, kmi_name):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            return km_item
    return None

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    def addtomenuupdate(self, context):
        if self.addtomenu:
            bpy.types.SEQUENCER_MT_select.append(addmenu_callback)
        else:
            bpy.types.SEQUENCER_MT_select.remove(addmenu_callback)
        return
    
    addtomenu: BoolProperty(
        name="Select menu",
        description="Show opertor in Sequencer's Select menu",
        default=False,
        update=addtomenuupdate
    )
    
    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        
        box = layout.box()
        row = box.row()
        row.prop(self, "addtomenu", text="Show opertor in Sequencer's Select menu")
        
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text='Hotkey')
        col.separator()
        
        kc = wm.keyconfigs.user
        km = kc.keymaps['Sequencer']
        kmi = get_hotkey_entry_item(km, 'sequencer.select_current')
        
        col.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)


addon_keymaps = []

def register():
    bpy.utils.register_class(SequencerSelectCurrent)
    bpy.utils.register_class(AddonPreferences)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # As Ctrl + J
        km = wm.keyconfigs.addon.keymaps.new(name='Sequencer', space_type='SEQUENCE_EDITOR')
        
        kmi = km.keymap_items.new('sequencer.select_current', 'S', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))
        
    


def unregister():
    bpy.utils.unregister_class(SequencerSelectCurrent)
    bpy.utils.unregister_class(AddonPreferences)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.types.SEQUENCER_MT_select.remove(addmenu_callback)

if __name__ == "__main__":
    register()
