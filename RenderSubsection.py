import bpy

bl_info = {
	"name": "Render Subsection",
	"blender": (2,80,0),
	"category": "Render",
}

# Render Subsection
# Specify a range of frames to render without changing the timeline start / end yourself.
# Useful if you want to playback a section of the timeline, but only want to re-render a smaller subsection.
# This saves time swapping the start / end back and forth.
# Render bounds are specified in a new panel on the 3D View context menu

def register():
	bpy.utils.register_class(CustomPropertyGroup)
	bpy.utils.register_class(RenderSection)
	bpy.utils.register_class(PlayblastSection)
	bpy.utils.register_class(RenderSectionPanel)
	bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomPropertyGroup)

def unregister():
	del bpy.types.Scene.custom_props
	bpy.utils.unregister_class(RenderSectionPanel)
	bpy.utils.unregister_class(PlayblastSection)
	bpy.utils.unregister_class(RenderSection)
	bpy.utils.unregister_class(CustomPropertyGroup)
	

# my two properties aka variables
# Start_slider is used to indicate what the first frame of the subsection should be
# Stop_slider is used to indicate what the final frame of the subsection should be
class CustomPropertyGroup(bpy.types.PropertyGroup):
	start_slider: bpy.props.IntProperty(name='Start', soft_min=0, soft_max=100)
	stop_slider: bpy.props.IntProperty(name='Stop', soft_min=0, soft_max=100)
	

class RenderSection(bpy.types.Operator):
	bl_idname = "custom.render_section"
	bl_label = "Render Section"
	bl_description = "Render the timeline with above limits"
	bl_options = {'REGISTER'}
	def execute(self, context):
		S = bpy.context.scene

		# Save old start / end
		old_start = S.frame_start
		old_end = S.frame_end

		# set new start end
		S.frame_start = S.custom_props.start_slider
		S.frame_end = S.custom_props.stop_slider

		# render
		bpy.ops.render.render(animation=True)
		#bpy.ops.render.opengl(animation=True)

		#restore old start / end
		S.frame_start = old_start
		S.frame_end = old_end
		self.report({'INFO'}, "Render Finished")
		return {'FINISHED'}

class PlayblastSection(bpy.types.Operator):
	bl_idname = "custom.playblast_section"
	bl_label = "Playblast Section"
	bl_description = "Playblast the timeline with above limits"
	bl_options = {'REGISTER'}
	def execute(self, context):
		S = bpy.context.scene

		# Save old start / end
		old_start = S.frame_start
		old_end = S.frame_end

		# set new start end
		S.frame_start = S.custom_props.start_slider
		S.frame_end = S.custom_props.stop_slider

		# render
		#bpy.ops.render.render(animation=True)
		bpy.ops.render.opengl(animation=True)

		#restore old start / end
		S.frame_start = old_start
		S.frame_end = old_end
		self.report({'INFO'}, "Render Finished")
		return {'FINISHED'}

class RenderSectionPanel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_render_section"
	bl_label = "Render Section"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_context = "objectmode"

	def draw(self, context):
		self.layout.label(text="Render Limits:")
		
		subrow = self.layout.row(align=True)
		subrow.prop(context.scene.custom_props, 'start_slider')
		subrow.prop(context.scene.custom_props, 'stop_slider')
		
		renderRow = self.layout.row(align=False)
		renderRow.operator('custom.render_section', text="Render")
		renderRow.operator('custom.playblast_section', text="Playblast")
		
if __name__ == "__main__":
	register()
