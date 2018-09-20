from configparser import SafeConfigParser

config = SafeConfigParser()

async def read_config():
    config.read('data.ini')

async def save_config():
    with open('data.ini', mode='w') as fh:
        config.write(fh)

async def get_skill_config(skill, cfg):
    if not (config.has_section(skill) and config.has_option(skill, cfg)):
        return None
    return config.get(skill, cfg)

async def set_skill_config(skill, cfg, value):
    if not config.has_section(skill):
        config.add_section(skill)
    
    if config.has_option(skill, cfg) and value is None:
        config.remove_option(skill, cfg)
    else:
        config.set(skill, cfg, value)

