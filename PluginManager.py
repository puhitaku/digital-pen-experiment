import os, logging
from io import StringIO
from threading import Thread

from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
from yapsy.PluginInfo import PluginInfo

import BasePlugin

class DpxPluginManager(PluginManager):
    def __init__(self, **kwargs):
        kwargs['plugin_info_ext'] = 'dpx-plugin'
        super().__init__(**kwargs)
        self.setPluginPlaces(['plugins'])
        self.setCategoriesFilter({
            'Parse': BasePlugin.ParserPlugin,
            'Draw': BasePlugin.DrawPlugin
            })
        self.collectPlugins()

        for plugin in self.getAllPlugins():
            plugin.plugin_object.invoke()


class YetAnotherPluginManager(PluginManager):
    """This class manages plugin's availability and creates plugin thread.

    Original implementation:
        "Yapsy: a simple hack to get rid of the plugin info file"
        http://stackoverflow.com/questions/8642146/how-to-define-category-in-yapsy-plugin

    """

    def __init__(self, 
                 categories_filter={"Default":IPlugin}, 
                 directories_list=None, 
                 plugin_info_ext="plugin.py"):
        """
        Initialize the mapping of the categories and set the list of
        directories where plugins may be. This can also be set by
        direct call the methods: 

        - ``setCategoriesFilter`` for ``categories_filter``
        - ``setPluginPlaces`` for ``directories_list``
        - ``setPluginInfoExtension`` for ``plugin_info_ext``

        You may look at these function's documentation for the meaning
        of each corresponding arguments.

        This hack just assumes that the plugin has an extension ".plugin.py"
        (or ".plugin" for directory, but I did not test it).

        """
        self.setPluginInfoClass(PluginInfo)
        self.setCategoriesFilter(categories_filter)     
        self.setPluginPlaces(directories_list)
        self.setPluginInfoExtension(plugin_info_ext)    

    def _gatherCorePluginInfo(self, directory, filename):
        """
        Gather the core information (name, and module to be loaded)
        about a plugin described by it's info file (found at
        'directory/filename').

        Return an instance of ``self.plugin_info_cls`` and the
        config_parser used to gather the core data *in a tuple*, if the
        required info could be localised, else return ``(None,None)``.

        .. note:: This is supposed to be used internally by subclasses
            and decorators.

        """
        # now we can consider the file as a serious candidate
        candidate_infofile = os.path.join(directory,filename)
        print(candidate_infofile)

        # My hack : just create a StringIO file with basic plugin info
        _fname = filename.rstrip(".py")
        _file = StringIO()
        _file.write("""[Core]
Name = %s
Module = %s
        """ % (_fname, _fname))
        _file.seek(0)

        # parse the information file to get info about the plugin
        name,moduleName,config_parser = self._getPluginNameAndModuleFromStream(_file, candidate_infofile)
        print(name, moduleName, config_parser)
        if (name,moduleName,config_parser) == (None,None,None):
            return (None,None)
        # start collecting essential info
        plugin_info = self._plugin_info_cls(name,os.path.join(directory,moduleName))
        return (plugin_info,config_parser)