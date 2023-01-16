# ##### BEGIN GPL LICENSE BLOCK #####
# yes, its gpl
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Mouseover Multiply",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "UI mouseover shortcut",
    "description": "Adds Operator that multiplies value under cursor",
    "tracker_url": "https://github.com/Zuorion/baddons",
    "doc_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "category": "User Interface",
}

import bpy
from bpy.props import (
    FloatProperty,
)
import rna_keymap_ui


class UI_Multiply(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ui.multiply_value"
    bl_label = "Multiply Value Under Cursor"
    
    
    my_float: FloatProperty(
        name="Multiplier",
        description="Value multiplier",
        default=2.0,
    )
    
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        wm = context.window_manager
        __class__.buffer = wm.clipboard
        
        try:
            bpy.ops.ui.copy_data_path_button(full_path=True)
            full_path = context.window_manager.clipboard
            eval_path = eval(wm.clipboard)
        
            if (type(eval(full_path)) is float) or (type(eval(full_path)) in int):
                number = eval_path * self.my_float
                exec(f"{wm.clipboard} = number")
                     
        except:
            self.report(
                {'WARNING'}, "Couldn't get path, invalid selection!")
            return {'CANCELLED'}
        finally:
            # restore clipboard content
            wm.clipboard = __class__.buffer
        
        return {'FINISHED'}    

        
class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    

   
    
    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager

        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text='Hotkey')
        col.separator()
        
        kc = wm.keyconfigs.user
        km = kc.keymaps['User Interface']
        
        kmi = get_hotkey_entry_items(km, 'ui.multiply_value', 0.5)
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            
        kmi = get_hotkey_entry_items(km, 'ui.multiply_value', 2.0)
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)



addon_keymaps = []



def get_addon_preferences():
    ''' quick wrapper for referencing addon preferences '''
    addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    return addon_preferences


def get_hotkey_entry_items(km, kmi_name, kmi_value):
    '''
    returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
    if there are multiple hotkeys!)
    '''
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if km.keymap_items[i].properties.my_float == kmi_value:
                return km_item
    return None 


def get_hotkey_entry_item(km, kmi_name):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            return km_item
    return None


    
    
def remove_hotkey():
    ''' clears all addon level keymap hotkeys stored in addon_keymaps '''
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['User Interface']
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

def register():
    bpy.utils.register_class(UI_Multiply)
    
    bpy.utils.register_class(AddonPreferences)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # As Numpad / * 
        km = wm.keyconfigs.addon.keymaps.new(name='User Interface')
        kmi = km.keymap_items.new('ui.multiply_value', 'NUMPAD_ASTERIX', 'PRESS')
        kmi.active = False
        kmi.properties.my_float = 2.0
        
        kmi = km.keymap_items.new('ui.multiply_value', 'NUMPAD_SLASH', 'PRESS')
        kmi.active = False
        kmi.properties.my_float = 0.5
        
        addon_keymaps.append((km, kmi))



def unregister():
    bpy.utils.unregister_class(UI_Multiply)
    
    bpy.utils.unregister_class(AddonPreferences)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    

if __name__ == "__main__":
    register()