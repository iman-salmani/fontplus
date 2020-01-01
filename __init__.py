bl_info = {
    "name": "Font Plus",
    "author": "Iman Salmani",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "location": "View3d > Text edit mode",
    "description": "Better Font support like RTL languages support and coming soon... forked from Write arabic text",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/iman-salmani/fontplus",
    "tracker_url": "https://github.com/iman-salmani/fontplus/issues",
    "category": "3D View",
}


# library
import bpy
import os
import sys

# modules
plugin_dir = os.path.dirname(bpy.data.filepath)
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)

import RTLTextTools


class __OT_ArabicTextMode(bpy.types.Operator):
    bl_idname = "view3d.arabic_text_mode"
    bl_label = "Write RTL Text"

    def modal(self, context, event):
        global text_buffer
        global current_char_index
        
        # Use this handler only when a 3DText object is selected and being edited
        
        if not bpy.context.object or bpy.context.object.type != 'FONT' or bpy.context.object.mode != 'EDIT':
            return {'PASS_THROUGH'}

        #
        
        if event.type == 'BACK_SPACE':

            if event.value == 'PRESS':
            
                RTLTextTools.delete_previous()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'DEL':
            
            if event.value == 'PRESS':
            
                RTLTextTools.delete_next()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'HOME':
            
            if event.value == 'PRESS':
            
                RTLTextTools.move_line_start()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'END':
            
            if event.value == 'PRESS':
            
                RTLTextTools.move_line_end()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'RIGHT_ARROW':
            
            if event.value == 'PRESS':
            
                RTLTextTools.move_previous()
            
            return {'RUNNING_MODAL'}
            
        elif event.type == 'LEFT_ARROW':
            
            if event.value == 'PRESS':
            
                RTLTextTools.move_next()
            
            return {'RUNNING_MODAL'}
        
        elif event.type == 'UP_ARROW':

            if event.value == 'PRESS':
            
                RTLTextTools.move_up()
            
            return {'RUNNING_MODAL'}

        elif event.type == 'DOWN_ARROW':

            if event.value == 'PRESS':
            
                RTLTextTools.move_down()
            
            return {'RUNNING_MODAL'}

        elif event.type == 'RET':
            
            if event.value == 'PRESS':
            
                RTLTextTools.insert_text('\n')
            
            return {'RUNNING_MODAL'}
                   
        elif event.type == 'TAB':
            
            if event.value == 'RELEASE':
                
                if bpy.context.object.mode == 'EDIT':
                
                    RTLTextTools.init()
            
            return {'PASS_THROUGH'}
            
        elif event.unicode:
            
            if event.value == 'PRESS':
                
                RTLTextTools.insert_text(event.unicode)
            
            return {'RUNNING_MODAL'}
        
        return {'PASS_THROUGH'}
     
    #
        
    def invoke(self, context, event):

        if context.area.type == 'VIEW_3D':
            
            context.window_manager.modal_handler_add(self)
            
            if bpy.context.object and bpy.context.object.type == 'FONT' and bpy.context.object.mode == 'EDIT':

                # update text data (i don't know a better way to do this)

                bpy.ops.object.editmode_toggle()
                bpy.ops.object.editmode_toggle()
                
                RTLTextTools.init()
            
            return {'RUNNING_MODAL'}
        else:
            return {'PASS_THROUGH'}


def register():
    bpy.utils.register_class(__OT_ArabicTextMode)
    wm = bpy.context.window_manager


def unregister():
    bpy.utils.unregister_class(__OT_ArabicTextMode)


if __name__ == "__main__":
    register()

    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            bpy.ops.view3d.arabic_text_mode({'area': area}, 'INVOKE_DEFAULT')
            break
