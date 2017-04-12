import bpy


MTL_KEYWORDS_MAP = {
    'map_Ka' : "AMBIENT_TEXTURE",
    'map_Kd' : "DIFFUSE_TEXTURE",
    'map_bump' : "BUMP_TEXTURE",
    'bump' : "BUMP_TEXTURE",
    'map_d' : "ALPHA_TEXTURE"
}

# Vectors
MTL_KEYWORDS_COLOR = {
    'Ka' : "AMBIENT_COLOR",
    'Kd' : "DIFFUSE_COLOR",
    'Ks' : "SPECULAR_COLOR"
}

# Floats
MTL_KEYWORDS_PROP = {
    'Ns' : "SPECULAR_WIDTH",
    'd' : "TRANSPARENCY_BRIGHTNESS",
    'Tr' : "TRANSPARENCY_BRIGHTNESS"
}

MTL_KEYWORDS_NAMES = {
    "AMBIENT_TEXTURE" : 'ambient',
    "DIFFUSE_TEXTURE" : 'diffuse',
    "BUMP_TEXTURE" : 'bump map',
    "ALPHA_TEXTURE" : 'mask',

    "AMBIENT_COLOR" : 'ambient color',
    "DIFFUSE_COLOR" : 'diffuse color',
    "SPECULAR_COLOR" : 'specular color',

    "SPECULAR_WIDTH" : 'specular coefficient',
    "TRANSPARENCY_BRIGHTNESS" : 'transparency'
}

# Map C4D constants to multipliers
MTL_KEYWORDS_MUL = {
    "AMBIENT_COLOR" : 1.0,
    "DIFFUSE_COLOR" : 1.0,
    "SPECULAR_COLOR" : 1.0,

    "SPECULAR_WIDTH" : 0.01,
    "TRANSPARENCY_BRIGHTNESS" : 1.0
}
                   
# Map C4D constants to 'use channel' IDs
# MTL_KEYWORDS_USE = {
#     AMBIENT_TEXTURE : USE_AMBIENT,
#     COLOR_TEXTURE : USE_COLOR,
#     BUMP_TEXTURE : USE_BUMP,
#     ALPHA_TEXTURE : USE_ALPHA,

#     AMBIENT_COLOR : USE_AMBIENT,
#     COLOR_COLOR : USE_COLOR,
#     SPECULAR_COLOR : USE_SPECULAR,

#     SPECULAR_WIDTH : USE_SPECULAR,
#     TRANSPARENCY_BRIGHTNESS : USE_TRANSPARENCY
# }

class Material:
    def set_cycles(self):
        scn = bpy.context.scene
        if not scn.render.engine == 'CYCLES':
            scn.render.engine = 'CYCLES'
            
    def make_material(self, name):
        self.mat = bpy.data.materials.new(name)
        self.mat.use_nodes = True
        self.nodes = self.mat.node_tree.nodes
        
    def link(self, from_node, from_slot_name, to_node, to_slot_name):
        input = to_node.inputs[to_slot_name]
        output = from_node.outputs[from_slot_name]
        self.mat.node_tree.links.new(input, output)
        
    def makeNode(self, type, name):
        self.node = self.nodes.new(type)
        self.node.name = name
        self.xpos += 200
        self.node.location = self.xpos, self.ypos
        return self.node
    
    def dump_node(self, node):
        print (node.name)
        print ("Inputs:\n")
        for n in node.inputs: print ("\t", n)
        print ("Outputs:\n")
        for n in node.outputs: print ("\t", n)
    
    def new_row():
        self.xpos = 0
        self.ypos += 200        
        
    def __init__(self):
        self.xpos = 0
        self.ypos = 0

# Set a material property
def SetMatProperty(material, matName, value, targetId):
    print('-> Inserting "' + str(value) + '" as "' + MTL_KEYWORDS_NAMES[targetId] + '" of material "' + matName + '".')
    mat = material
    if (targetId == "DIFFUSE_COLOR"):
        diffuseBSDF = mat.nodes['Diffuse BSDF']
        diffuseBSDF.inputs["Color"].default_value = [float(value[0]), float(value[1]), float(value[2]), 1]
    
    

# Iterate lines of .mtl file, extract data, create cycles materials
def ParseFile(fName):
    # print(fName)

    # Variables
    matName = ''
    matCount = 0
    mapCount = 0
    lineNbr = 0

    lines = [line.rstrip('\n') for line in open(fName)]

    for line in lines:
        lineNbr += 1
        words = line.split(' ')

        # Empty line -> End of current material
        if (line == ''):
            continue

        # Comment line
        elif (line.startswith('#')):
            continue

        # Check if line is the beginning of a new material
        elif (line.startswith('newmtl')):
            matName = words[1]
            matCount += 1

            m = Material()
            m.make_material(matName)

            print (' \nLine ' + str(lineNbr) + ': Found new material "' + matName + '"')

        # Check for maps
        elif (words[0] in MTL_KEYWORDS_MAP):
            mapName = words[1]
            mapCount += 1
            print ('Found ' + MTL_KEYWORDS_NAMES[MTL_KEYWORDS_MAP[words[0]]] + ' map: ' + words[1])

        # Check for colors
        elif (words[0] in MTL_KEYWORDS_COLOR):
            targetId = MTL_KEYWORDS_COLOR[words[0]]
            SetMatProperty(m, matName, [words[1], words[2], words[3]], targetId)
            print ('Found ' + MTL_KEYWORDS_NAMES[targetId] + ': ' + words[1] + ' ' + words[2] + ' ' + words[3])

        # Check for float values
        elif (words[0] in MTL_KEYWORDS_PROP):
            targetId = MTL_KEYWORDS_PROP[words[0]]
            value = float(words[-1])
            print ('Found ' + MTL_KEYWORDS_NAMES[targetId] + ': ' + str(value))

    print (' \nDone. Parsed ' + str(lineNbr) + ' lines and found ' + str(matCount) + ' mat with ' + str(mapCount) + ' texture maps')
    

ParseFile('test.mtl')

