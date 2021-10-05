from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import os
import json
import xml

PATH_JSON_SNAP_PROJECT = os.path.dirname(os.path.abspath(__file__)) + '/' + 'data.json'

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inproject = False
        self.instage=False
        self.inSprites = False
        self.inScripts = False
        self.inBlock = False
        self.inScript = False
        self.inScript2 = False
        self.inSprite = False
        self.inVariables = False
        self.numberSprites = 0
        self.numberScripts = 0
        self.numberVariables = 0
        self.numberBlocks = 0
        self.inBlocks = False
        self.inContent = False
        self.nameProject = ""
        self.theContent = ""
        self.inBlockDef=False
        self.numberBlockDef=0
        self.data = {}
        self.data['project_name'] = []
        self.data['sprites'] = []
        self.data['variables'] = []
        self.data['block-definition']=[]
        self.inVariable = False
        self.inProject = False
        self.value=""

        self.inBlockCustom=False

    def startElement (self, name, attrs):

        cont = 0
        if name == 'project':
            self.inProject = True
            self.nameProject = attrs.get("name")
            self.data['project_name'].append({'name': self.nameProject})
        elif self.inProject:
            if name == 'stage':
                self.instage = True
            elif self.instage:
                if name == 'sprites':
                    self.inSprites = True
                elif self.inSprites:
                    if name == 'sprite':
                        self.inSprite =True
                        self.numberSprites = self.numberSprites + 1
                    elif self.inSprite:
                        if name == 'scripts':
                            self.inScripts=True
                        elif self.inScripts:
                            if name == 'script':
                                try:
                                    value = attrs.getValue('x')
                                    self.inScript = True
                                    self.inScript2=False
                                    self.numberScripts = self.numberScripts + 1
                                except:
                                    self.inScript = True
                                    self.inScript2=True
                            elif self.inScript or self.inScript2:
                                if name == 'block':
                                    self.inBlock = True
                                    self.numberBlocks = self.numberBlocks + 1
                                    try:
                                        self.data['sprites'].append({
                                            'sprite': self.numberSprites,
                                            'script': self.numberScripts,
                                            'block': attrs.getValue('s'),
                                            'num_block':self.numberBlocks
                                            })

                                    except:
                                            self.inBlock = False
                            elif name=='block':
                                self.inBlock = True
                                self.numberBlocks = self.numberBlocks + 1
                                try:
                                    self.data['sprites'].append({
                                        'sprite': self.numberSprites,
                                        'script': self.numberScripts,
                                        'block': attrs.getValue('s'),
                                        'num_block':self.numberBlocks
                                        })

                                except:
                                        self.inBlock = False


                        elif name == 'blocks':
                            self.inBlocks = True
                        elif self.inBlocks:
                            #bloque definido
                            if name == 'block-definition':
                                try:
                                    value = attrs.getValue('s')
                                    self.inBlockDef = True
                                    self.numberBlockDef= self.numberBlockDef + 1
                                    self.data['block-definition'].append({
                                        'name': value,
                                        'number': self.numberBlockDef,
                                        })
                                    self.data[value]=[]
                                    self.value = value
                                except:
                                    self.inBlockDef = False
                            #guardamos los bloques usados en los bloques definidos
                            elif self.inBlockDef:

                                self.inBlockCustom=True
                                try:
                                    self.data[self.value].append({
                                        #'name': self.value,
                                        'block': attrs.getValue('s'),
                                        })
                                except:
                                    self.inBlockCustom=False

                        elif name == 'variables':
                            self.inVariables = True
                        elif self.inVariables:
                            try:
                                value = attrs.getValue('name')
                                self.numberVariables=self.numberVariables+1
                                self.data['variables'].append({
                                    'variable': value,
                                    'number_var':self.numberVariables
                                    })
                                self.inVariable = True
                            except:
                                self.inVariable = False

            elif name == 'blocks':
                self.inBlocks = True
            elif self.inBlocks:
                if name == 'block-definition':
                    try:
                        self.value = attrs.getValue('s')
                        self.data[self.value]=[]
                        self.inBlockDef = True
                        self.numberBlockDef= self.numberBlockDef + 1
                        self.data['block-definition'].append({
                            'name': self.value,
                            'number': self.numberBlockDef
                            })

                    except:
                        self.inBlockDef = False

                elif self.inBlockDef:
                    if name == 'block':
                        self.inBlockCustom=True
                        try:
                            self.data[self.value].append({
                                #'name': self.value,
                                'block': attrs.getValue('s'),
                                })

                        except:
                            self.inBlockCustom=False

            elif name == 'variables':
                self.inVariables = True

            elif self.inVariables:
                try:
                    value = attrs.getValue('name')
                    self.numberVariables=self.numberVariables+1
                    self.data['variables'].append({
                        'variable': value,
                        'number_var':self.numberVariables
                        })

                    self.inVariable = True

                except:
                    self.inVariable = False

    #cerramos
    def endElement (self, name):

        #salimos del xml por lo que volcamos la información recogida en un JSON
        if name == 'project':
            self.inProject=False
            with open(PATH_JSON_SNAP_PROJECT, 'w') as file:
                json.dump(self.data, file, indent=4)

        elif self.inProject:
            if name == 'stage':
                self.instage=False

            elif  self.instage:
                if name=='sprites':
                    self.inSprites=False

                elif self.inSprites:

                    if name == 'blocks':
                        self.inBlocks = False

                    elif self.inBlocks:
                        if name== 'block-definition':
                            self.inBlockDef = False
                        elif self.inBlockDef:
                            self.inBlockCustom=False

                    elif name == 'variables':
                        self.inVariables=False

                    elif self.inVariable:
                        self.inVariables=False

                    elif name == 'sprite':
                        self.inSprite = False
                    elif self.inSprite:
                        if name == 'scripts':
                            self.inScripts=False
                        elif self.inScripts:
                            if name == 'script' and not self.inScript2:
                                self.inScript = False
                            elif name == 'script' and self.inScript2:
                                self.inScript2=False
                            elif self.inScript or self.inScript2:
                                if name == 'block':
                                        self.inBlock = False
                            elif name=='block':
                                    self.inBlock = False
            elif name == 'blocks':
                self.inBlocks = False
            elif self.inBlocks:
                if name== 'block-definition':
                    self.inBlockDef = False
                elif self.inBlockDef:
                    if name == 'block':
                        self.inBlockCustom = False

            elif name == 'variables':
                self.inVariables=False
            elif self.inVariable:
                self.inVariables=False


    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


class ParserXML:

    ERROR_FILE = "./error_parser.txt"

    def __init__(self, xml_file):
        self.parser = make_parser()
        self.handler = myContentHandler()
        self.parser.setContentHandler(self.handler)
        try:
            self.parser.parse(xml_file)
        except xml.sax._exceptions.SAXParseException as e:
            with open(xml_file, "r") as file_error:
                texto = file_error.read()
                if '<project name="' in texto:
                    project_name = texto.split('"')[1]
                else:
                    project_name = "Unknown"

                with open(ParserXML.ERROR_FILE, "a") as file_err_write:
                    file_err_write.write(f"Error en el proyecto {project_name} el fichero {xml_file} no está bien formado: {str(e)}\n")
                print(f"Error en el proyecto {project_name} el fichero {xml_file} no está bien formado")
