import bpy


bl_info = {
    "name": "ReAdd Smooth Active",
    "author": "Zuorion",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > WeightPaint > Weight",
    "description": "ReAdd Smooth Active Vertex group option in menu",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

def draw_item(self, context):
        layout = self.layout

        layout.operator("object.vertex_group_smooth", text="Smooth Active").group_select_mode='ACTIVE'


def register():
    bpy.types.VIEW3D_MT_paint_weight.append(draw_item)


def unregister():
    bpy.types.VIEW3D_MT_paint_weight.remove(draw_item)
    


if __name__ == "__main__":
    register()
