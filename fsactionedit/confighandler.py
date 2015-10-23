import configparser
from fsactionedit.amigaactions import AmigaActions


class ConfigHandler:

    def __init__(self):
        self.amigaactions = AmigaActions()
        self._loaded_config = None
        self._loaded_configfile = None
        self._our_config = None
        self._non_action_count = 0

    @property
    def loaded_config(self):
        return self._loaded_config

    @loaded_config.setter
    def loaded_config(self, value):
        if not isinstance(value, configparser.ConfigParser) and value is not None:
            raise TypeError('Cannot assign this shit as a loaded config.')
        else:
            self._loaded_config = value
        if value is None:
            self._loaded_configfile = None

    @property
    def loaded_configfile(self):
        return self._loaded_configfile

    @property
    def non_action_count(self):
        return self._non_action_count

    def load(self, configfile):
        """Load config from file,
        return actions (key = val) or None on error."""
        self._non_action_count = 0
        self._loaded_config = configparser.ConfigParser(
            delimiters=('=',), strict=False)
        try:
            cfglist = self._loaded_config.read(configfile)
        except configparser.Error:
            return None
        if len(cfglist) == 0 or self._loaded_config.has_section('fs-uae') is False:
            return None
        self._loaded_configfile = configfile
        action_opts = []
        for opt, val in self._loaded_config.items('fs-uae'):
            print(opt, val)
            if self.amigaactions.is_valid(val):
                action_opts.append('{0} = {1}'.format(opt, val))
            else:
                self._non_action_count += 1
        print(action_opts)
        return action_opts

    def save(self, path, cfglist, include_loaded=True):
        """Save a key=val list of options to path, if include_loaded=True
        ALL prev. loaded options will also be saved.
        Return path on success, False on error."""
        if include_loaded is True and self._loaded_config is not None:
            self._our_config = self._loaded_config
        else:
            self._our_config = configparser.ConfigParser(delimiters=('=',), strict=False)
        if not self._our_config.has_section('fs-uae'):
            self._our_config['fs-uae'] = {}
        self._our_fsconfig = self._our_config['fs-uae']
        for cfg in cfglist:
            key, val = cfg.split('=', 1)
            self._our_fsconfig[key.strip()] = val.strip()
        if not path.endswith('.fs-uae'):
            path += '.fs-uae'
        try:
            with open(path, 'wt') as f:
                self._our_config.write(f)
        except OSError:
            return False
        else:
            self._loaded_config = self._our_config
            self._loaded_configfile = path
            return path

    def remove_action(self, action):
        """Remove an action from the loaded configuration."""
        if self.loaded_config is None:
            return
        self.loaded_config.remove_option('fs-uae', action)

if '__name__' == '__main__':
    import os
    os.chdir('/tmp')
    c = ConfigHandler()
    a = c.load(os.path.expanduser('~/FS-UAE/Configurations/Host.fs-uae'))
    print(a)
