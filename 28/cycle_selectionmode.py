bl_info = {
    "name": "Cyclic selection mode",
    "author": "Zuorion",
    "version": (0, 1, 668),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Cyclice through edit selection modes",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}
    
import bpy
    
class Cycleselectionmode(bpy.types.Operator):
    bl_idname = "mesh.cycle_selection_mode"
    bl_label = "Cycles Selection modes"
    bl_options = {'REGISTER'}
    
    reverse = bpy.props.BoolProperty(name="Reverse", default= True )
    
    def invoke(self, context, event):
        curselection = bpy.context.scene.tool_settings.mesh_select_mode
        if self.reverse == True:
            #bpy.context.tool_settings.mesh_select_mode = (curselection[1], curselection[2], curselection[0])
            if (curselection[1]): bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            elif (curselection[2]): bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            elif (curselection[0]): bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        else:
            #bpy.context.tool_settings.mesh_select_mode = (curselection[2], curselection[0], curselection[1])
            if (curselection[2]): bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            elif (curselection[0]): bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            elif (curselection[1]): bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

        return {'FINISHED'}


addon_keymaps = []
        
def register():
    
    bpy.utils.register_class(Cycleselectionmode)
    
    # handle the keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        print("aa")
        km = kc.keymaps.new(name="Mesh", space_type="EMPTY")
        kmi = km.keymap_items.new("mesh.cycle_selection_mode", "WHEELUPMOUSE", "PRESS", shift=True)
        kmi.properties.reverse = False
        
        kmi = km.keymap_items.new("mesh.cycle_selection_mode", "WHEELDOWNMOUSE", "PRESS", shift=True)
        kmi.properties.reverse = True
        
        
    
    addon_keymaps.append((km, kmi))
    
def unregister():  
    bpy.utils.unregister_class(Cycleselectionmode)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
if __name__ == "__main__":
    register()
    
    