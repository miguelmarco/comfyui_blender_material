import tempfile
import os
import bpy


from bpy.props import StringProperty, IntProperty, PointerProperty
import json
from urllib import request, parse
from urllib.error import URLError

from .presets import workflowjson

url = 'http://127.0.0.1:8188'

def send_job(prompt = 'brick texture', url=url, seed = 0, model='realisticVisionV51_v51VAE.safetensors'):
    workflow = json.loads(workflowjson)
    workflow['3']['inputs']['text'] = prompt
    workflow['6']['inputs']['seed'] = seed
    workflow['1']['inputs']['ckpt_name'] = model
    d = {"prompt": workflow}
    data = json.dumps(d).encode('utf-8')
    req =  request.Request(f"{url}/prompt", data=data)
    result = request.urlopen(req)
    status = result.status
    if not status == 200:
        raise URLError
    prompt_id = json.loads(result.read())['prompt_id']
    return prompt_id

def get_status(prompt_id, url=url):
    check_queue = request.Request(f'{url}/queue')
    queue = request.urlopen(check_queue)
    queuedic = json.loads(queue.read())
    if any(prompt_id in q for q in queuedic['queue_pending']):
        return 'pending'
    if any(prompt_id in q for q in queuedic['queue_running']):
        return 'running'
    get_job_req = request.Request(f"{url}/history/{prompt_id}")
    hist = request.urlopen(get_job_req)
    history = json.loads(hist.read())
    return history[prompt_id]['status']['status_str']

def download_files(prompt_id, url=url, prefix=''):
    get_job_req = request.Request(f"{url}/history/{prompt_id}")
    hist = request.urlopen(get_job_req)
    history = json.loads(hist.read())
    outputs = history[prompt_id]['outputs']
    dn = outputs['34']['images'][0]['filename']
    nn = outputs['14']['images'][0]['filename']
    rn = outputs['24']['images'][0]['filename']

    for (filename, pref) in [(dn, "D"), (nn, "N") , (rn, "R")]:
        imgdata = {'filename' : filename, 'subfolder' : '', 'type' : 'temp'}
        fields = parse.urlencode(imgdata)
        imgurl = f'{url}/api/view?{fields}'
        request.urlretrieve(imgurl, f'{prefix}_{pref}.png')

def get_models(url):
    get_models_request = request.Request(f'{url}/models')
    ans = request.urlopen(get_models_request)
    models = json.loads(ans.read())
    return models

class ComfyUIProperties(bpy.types.PropertyGroup):
    url: bpy.props.StringProperty(name="URL", default="http://127.0.0.1:8188")
    model: bpy.props.StringProperty(name="model", default="realisticVisionV51_v51VAE.safetensors")
    prompt: bpy.props.StringProperty(name="Prompt", default="brick texture")
    seed: bpy.props.IntProperty(name="Seed", default=0)
    status: bpy.props.StringProperty(name="Status", default="")
    counter: bpy.props.IntProperty(name="counter", default=0)

class ComfyUIOperator(bpy.types.Operator):
    bl_idname = "material.generate_with_comfyui"
    bl_label = "Generate Material"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        scene = context.scene
        mytool = scene.comfyui_tool
        try:
            pid = send_job(mytool.prompt, mytool.url, mytool.seed, mytool.model)
            def run_update():
                status = get_status(pid, mytool.url)
                mytool.status = status
                if status in ('pending', 'running'):
                    return 0.5
                elif status == 'success':
                    mytool.seed += 1
                    tmpdir = tempfile.mkdtemp()
                    print(tmpdir)
                    prefix = os.path.join(tmpdir, f'CMFT{mytool.counter}')
                    download_files(pid, mytool.url, prefix)
                    mat = bpy.data.materials.new(name=f"ComfyUI_Material{mytool.counter}")
                    mat.use_nodes = True
                    bsdf = mat.node_tree.nodes.get('Principled BSDF')
                    diffusenode = mat.node_tree.nodes.new("ShaderNodeTexImage")
                    diffusenode.location=(-300,500)
                    imgD = bpy.data.images.load(f'{prefix}_D.png')
                    diffusenode.image = imgD
                    mat.node_tree.links.new(bsdf.inputs['Base Color'], diffusenode.outputs['Color'])
                    roughnessnode = mat.node_tree.nodes.new("ShaderNodeTexImage")
                    roughnessnode.location = (-300,200)
                    imgR = bpy.data.images.load(f'{prefix}_R.png')
                    imgR.colorspace_settings.name ='Non-Color'
                    roughnessnode.image = imgR
                    mat.node_tree.links.new(bsdf.inputs['Roughness'], roughnessnode.outputs['Color'])
                    normalnode = mat.node_tree.nodes.new("ShaderNodeTexImage")
                    normalnode.location = (-600,-100)
                    imgN = bpy.data.images.load(f'{prefix}_N.png')
                    imgN.colorspace_settings.name ='Non-Color'
                    normalnode.image = imgN
                    normalmapnode = mat.node_tree.nodes.new('ShaderNodeNormalMap')
                    normalmapnode.location = (-300,-100)
                    mat.node_tree.links.new(normalmapnode.inputs['Color'], normalnode.outputs['Color'])
                    mat.node_tree.links.new(bsdf.inputs['Normal'], normalmapnode.outputs['Normal'])
                    mytool.counter += 1
                    obj = bpy.context.object
                    if obj is not None:
                        if obj.data.materials:
                            obj.data.materials[0] = mat
                        else:
                            obj.data.materials.append(new_material)
                    self.report({'INFO'}, "Material generated")
                    return None
                else:
                  return None
            bpy.app.timers.register(run_update)
        except Exception as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}

class ComfyUIPanel(bpy.types.Panel):
    bl_idname = "MATERIAL_PT_ComfyUI"
    bl_label = "Material generator (ComfyUI)"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ComfyUI'
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.comfyui_tool
        layout.prop(mytool, "url")
        layout.prop(mytool, "model")
        layout.prop(mytool, "seed")
        layout.prop(mytool, "prompt")
        props = layout.operator("material.generate_with_comfyui")
        row = layout.row()
        row.enabled = False
        row.prop(mytool, "status")

def register():
    bpy.utils.register_class(ComfyUIProperties)
    bpy.utils.register_class(ComfyUIOperator)
    bpy.utils.register_class(ComfyUIPanel)
    bpy.types.Scene.comfyui_tool = PointerProperty(type=ComfyUIProperties)

def unregister():
    bpy.utils.unregister_class(ComfyUIPanel)
    bpy.utils.unregister_class(ComfyUIOperator)
    del bpy.types.Scene.comfyui_tool
    bpy.utils.unregister_class(ComfyUIProperties)

