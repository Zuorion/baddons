# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Origin Pie/Menu",
    "description": "Origin Snap/Place Menu, Hotkey: 'Ctrl Alt X'",
    "author": "Zuorion, pitiwazou, meta-androcto",
    "version": (0, 1, 3),
    "blender": (2, 81, 0),
    "location": "3D View",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
    }

import bpy
from bpy.types import (
        Menu,
        Operator,
        )


# Pivot to selection
class PIE_OT_PivotToSelection(Operator):
    bl_idname = "object.pivot2selection"
    bl_label = "Pivot To Selection"
    bl_description = "Pivot Point To Selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        saved_location = context.scene.cursor.location.copy()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        context.scene.cursor.location = saved_location

        return {'FINISHED'}

# Pivot to Bottom
class PIE_OT_PivotBottom(Operator):
    bl_idname = "object.pivotobottom"
    bl_label = "Pivot To Bottom"
    bl_description = ("Set the Pivot Point To Lowest Point\n"
                      "Needs an Active Object of the Mesh type")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        o = context.active_object
        init = 0
        for x in o.data.vertices:
            if init == 0:
                a = x.co.z
                init = 1
            elif x.co.z < a:
                a = x.co.z

        for x in o.data.vertices:
            x.co.z -= a

        o.location.z += a

        return {'FINISHED'}


# Pivot to Bottom
class PIE_OT_PivotBottom_edit(Operator):
    bl_idname = "object.pivotobottom_edit"
    bl_label = "Pivot To Bottom"
    bl_description = ("Set the Pivot Point To Lowest Point\n"
                      "Needs an Active Object of the Mesh type")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        o = context.active_object
        init = 0
        for x in o.data.vertices:
            if init == 0:
                a = x.co.z
                init = 1
            elif x.co.z < a:
                a = x.co.z

        for x in o.data.vertices:
            x.co.z -= a

        o.location.z += a
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


# Pivot to Cursor Edit Mode
class PIE_OT_PivotToCursor_edit(Operator):
    bl_idname = "object.pivot2cursor_edit"
    bl_label = "Pivot To Cursor"
    bl_description = "Pivot Point To Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


# Origin to Center of Mass Edit Mode
class PIE_OT_OriginToMass_edit(Operator):
    bl_idname = "object.origintomass_edit"
    bl_label = "Origin"
    bl_description = "Origin to Center of Mass"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


# Origin to Geometry Edit Mode
class PIE_OT_OriginToGeometry_edit(Operator):
    bl_idname = "object.origintogeometry_edit"
    bl_label = "Origin to Geometry"
    bl_description = "Origin to Geometry"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


# Origin to Geometry Edit Mode
class PIE_OT_GeometryToOrigin_edit(Operator):
    bl_idname = "object.geometrytoorigin_edit"
    bl_label = "Geometry to Origin"
    bl_description = "Geometry to Origin"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


# Origin To Selected Edit Mode #
def vfeOrigin_pie(context):
    try:
        cursorPositionX = context.scene.cursor.location[0]
        cursorPositionY = context.scene.cursor.location[1]
        cursorPositionZ = context.scene.cursor.location[2]
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene.cursor.location[0] = cursorPositionX
        context.scene.cursor.location[1] = cursorPositionY
        context.scene.cursor.location[2] = cursorPositionZ
        return True
    except:
        return False


class PIE_OT_SetOriginToSelected_edit(Operator):
    bl_idname = "object.setorigintoselected_edit"
    bl_label = "Set Origin to Selected"
    bl_description = "Set Origin to Selected"

    @classmethod
    def poll(cls, context):
        return (context.area.type == "VIEW_3D" and context.active_object is not None)

    def execute(self, context):
        check = vfeOrigin_pie(context)
        if not check:
            self.report({"ERROR"}, "Set Origin to Selected could not be performed")
            return {'CANCELLED'}

        return {'FINISHED'}

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
        bpy.context.scene.tool_settings.use_transform_data_origin = True
        bpy.ops.transform.transform(mode='ALIGN', value=(0, 0, 0, 0), orient_type='rOrientation', mirror=True, use_proportional_edit=False)
        #Restore settings and editmode
        bpy.ops.transform.delete_orientation()
        bpy.context.scene.transform_orientation_slots[0].type = prev_orientation 
        bpy.context.scene.tool_settings.use_transform_data_origin = utdo
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}



# Pie Origin/Pivot - Shift + S
class PIE_MT_OriginPivot(Menu):
    bl_idname = "ORIGIN_MT_pivotmenu"
    bl_label = "Origin Menu"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        pie = layout.menu_pie()
        if obj and obj.type == 'MESH' and obj.mode in {'OBJECT'}:
            # 4 - LEFT
            pie.operator("object.origin_set", text="Origin to Center of Mass",
                         icon='NONE').type = 'ORIGIN_CENTER_OF_MASS'
            # 6 - RIGHT
            pie.operator("object.origin_set", text="Origin to Cursor",
                        icon='PIVOT_CURSOR').type = 'ORIGIN_CURSOR'
            # 2 - BOTTOM
            pie.operator("object.pivotobottom", text="Origin to Bottom",
                        icon='TRIA_DOWN')
            # 8 - TOP
            pie.operator("object.pivot2selection", text="Origin To Selection",
                        icon='SNAP_INCREMENT')
            # 7 - TOP - LEFT
            pie.operator("object.origin_set", text="Geometry To Origin",
                        icon='NONE').type = 'GEOMETRY_ORIGIN'
            # 9 - TOP - RIGHT
            pie.operator("object.origin_set", text="Origin To Geometry",
                        icon='NONE').type = 'ORIGIN_GEOMETRY'


        elif obj and obj.type == 'MESH' and obj.mode in {'EDIT'}:                        
            # 4 - LEFT
            pie.operator("object.origintomass_edit", text="Origin to Center of Mass",
                         icon='NONE')
            # 6 - RIGHT
            pie.operator("object.pivot2cursor_edit", text="Origin to Cursor",
                        icon='PIVOT_CURSOR')
            # 2 - BOTTOM
            pie.operator("object.pivotobottom_edit", text="Origin to Bottom",
                        icon='TRIA_DOWN')
            # 8 - TOP
            pie.operator("object.setorigintoselected_edit", text="Origin To Selected",
                        icon='SNAP_INCREMENT')        
            # 7 - TOP - LEFT
            pie.operator("object.geometrytoorigin_edit", text="Geometry To Origin",
                        icon='NONE')
            # 9 - TOP - RIGHT
            pie.operator("object.origintogeometry_edit", text="Origin To Geometry",
                        icon='NONE')
            # 10 - TOP - RIGHT          
            pie.operator("object.ralign_orientation_to_selection", text="Align Orientation To Selection",
                        icon='NONE')

        else:
            # 4 - LEFT
            pie.operator("object.origin_set", text="Origin to Center of Mass",
                         icon='NONE').type = 'ORIGIN_CENTER_OF_MASS'
            # 6 - RIGHT
            pie.operator("object.origin_set", text="Origin To 3D Cursor",
                        icon='PIVOT_CURSOR').type = 'ORIGIN_CURSOR'
            # 2 - BOTTOM
            pie.operator("object.pivot2selection", text="Origin To Selection",
                        icon='SNAP_INCREMENT')
            # 8 - TOP
            pie.operator("object.origin_set", text="Origin To Geometry",
                        icon='NONE').type = 'ORIGIN_GEOMETRY'
            # 7 - TOP - LEFT
            pie.operator("object.origin_set", text="Geometry To Origin",
                        icon='NONE').type = 'GEOMETRY_ORIGIN'



class VIEW3D_MT_OriginPivotMenu(Menu):
    bl_idname = "VIEW3D_MT_OriginPivotMenu"
    bl_label = "Origin Menu"
    
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        obj = context.object

        if obj and obj.type == 'MESH' and obj.mode in {'OBJECT'}:
            # 4 - LEFT
            layout.operator("object.origin_set", text="Origin to Center of Mass",
                         icon='NONE').type = 'ORIGIN_CENTER_OF_MASS'
            # 6 - RIGHT
            layout.operator("object.origin_set", text="Origin to Cursor",
                        icon='PIVOT_CURSOR').type = 'ORIGIN_CURSOR'
            # 2 - BOTTOM
            layout.operator("object.pivotobottom", text="Origin to Bottom",
                        icon='TRIA_DOWN')
            # 8 - TOP
            layout.operator("object.pivot2selection", text="Origin To Selection",
                        icon='SNAP_INCREMENT')
            # 7 - TOP - LEFT
            layout.operator("object.origin_set", text="Geometry To Origin",
                        icon='NONE').type = 'GEOMETRY_ORIGIN'
            # 9 - TOP - RIGHT
            layout.operator("object.origin_set", text="Origin To Geometry",
                        icon='NONE').type = 'ORIGIN_GEOMETRY'


        elif obj and obj.type == 'MESH' and obj.mode in {'EDIT'}:                        
            # 4 - LEFT
            layout.operator("object.origintomass_edit", text="Origin to Center of Mass",
                         icon='NONE')
            # 6 - RIGHT
            layout.operator("object.pivot2cursor_edit", text="Origin to Cursor",
                        icon='PIVOT_CURSOR')
            # 2 - BOTTOM
            layout.operator("object.pivotobottom_edit", text="Origin to Bottom",
                        icon='TRIA_DOWN')
            # 8 - TOP
            layout.operator("object.setorigintoselected_edit", text="Origin To Selected",
                        icon='SNAP_INCREMENT')        
            # 7 - TOP - LEFT
            layout.operator("object.geometrytoorigin_edit", text="Geometry To Origin",
                        icon='NONE')
            # 9 - TOP - RIGHT
            layout.operator("object.origintogeometry_edit", text="Origin To Geometry",
                        icon='NONE')
            layout.operator("object.ralign_orientation_to_selection", text="Align Orientation To Selection",
                        icon='NONE')

        else:
            # 4 - LEFT
            layout.operator("object.origin_set", text="Origin to Center of Mass",
                         icon='NONE').type = 'ORIGIN_CENTER_OF_MASS'
            # 6 - RIGHT
            layout.operator("object.origin_set", text="Origin To 3D Cursor",
                        icon='PIVOT_CURSOR').type = 'ORIGIN_CURSOR'
            # 2 - BOTTOM
            layout.operator("object.pivot2selection", text="Origin To Selection",
                        icon='SNAP_INCREMENT')
            # 8 - TOP
            layout.operator("object.origin_set", text="Origin To Geometry",
                        icon='NONE').type = 'ORIGIN_GEOMETRY'
            # 7 - TOP - LEFT
            layout.operator("object.origin_set", text="Geometry To Origin",
                        icon='NONE').type = 'GEOMETRY_ORIGIN'

def addmenu_callback(self, context):
    self.layout.menu("VIEW3D_MT_OriginPivotMenu")

classes = (
    PIE_MT_OriginPivot,
    PIE_OT_PivotToSelection,
    PIE_OT_PivotBottom,
    PIE_OT_PivotToCursor_edit,
    PIE_OT_OriginToMass_edit,
    PIE_OT_PivotBottom_edit,
    PIE_OT_OriginToGeometry_edit,
    PIE_OT_GeometryToOrigin_edit,
    PIE_OT_SetOriginToSelected_edit,
    RAlignOrientationToSelection,
    VIEW3D_MT_OriginPivotMenu
    )

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Origin/Pivot
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'X', 'PRESS', ctrl=True, alt=True)
        kmi.properties.name = "VIEW3D_MT_OriginPivotMenu"
        addon_keymaps.append((km, kmi))
        
    bpy.types.VIEW3D_MT_edit_mesh.append(addmenu_callback)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.types.VIEW3D_MT_edit_mesh.remove(addmenu_callback)


if __name__ == "__main__":
    register()
