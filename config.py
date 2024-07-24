import configparser

# class Config():
#     """
#     __init__
#     Params:

#     Returns:
#     - Config object, for which we can access config vars from
#     """
#     def __init__(self):
#         self.config = configparser.ConfigParser()
#         self.config.read('config.conf')

#         # Config does not exist yet
#         if not self.config.sections(): 
#             self.create_config()
#             print("Created config")
        
#         self.model = self.config['General']['model']
#         self.prompt = self.config['General']['prompt']
#         self.system = self.config['General']['system']

#     def create_config(self):    
#         self.config['General'] = {'model': 'mixtral-8x7B-32768',
#                                   'prompt': 'None',
#                                   'system': 'None'}
        
#         with open('config.conf', 'w') as configfile:
#             self.config.write(configfile)


import xml.etree.ElementTree as ET
class Config:
    def __init__(self):
        self.find_config()
        self.read_config()

    def read_config(self):
        tree = ET.parse(self.configPath)
        root = tree.getroot()

        sys_prompt_info = root[2].text
        print(sys_prompt_info)
        # sys_prompt_rp = root[1].text
        # character = root[0].text
        # init_wiki = root[].t`ext

    def find_config(self):
        self.configPath = 'rp.xml'
        #file = open(self.configPath, 'r')

    def generate_config(self):
        try:
            self.configPath = 'config.xml'
            file = open(self.configPath, 'wr')
            file.write(self.config_template)
            file.close()
        except PermissionError as e:
            raise RuntimeError
        

if __name__ == "__main__":
    conf = Config()