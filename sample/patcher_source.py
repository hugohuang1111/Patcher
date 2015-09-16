#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("..")
from patcher.mod_source import ModSource

def main():
	cur_dir = os.path.dirname(os.path.realpath(__file__))
	# cpp code
	# cfg = {'dir': cur_dir,
	# 'file': 'AppDelegate.cpp',
	# 'class': 'AppDelegate',
	# 'function': 'applicationDidFinishLaunching',
	# 'position': 'before',
	# 'content': 'sdkbox::Plugin$(SDKBOX_PLUGIN_NAME)::init();',
	# 'header': '#include "Plugin$(SDKBOX_PLUGIN_NAME)/Plugin$(SDKBOX_PLUGIN_NAME).h"'
	# }
	# m = ModSource(cfg)
	# m.apply_modify()

	cfg = {'dir': cur_dir,
	'file': 'lua_module_register.h',
	'class': '',
	'function': 'lua_module_register',
	'position': 'before',
	'content': 'sdkbox::Plugin$(SDKBOX_PLUGIN_NAME)::init();',
	'header': '#include "Plugin$(SDKBOX_PLUGIN_NAME)/Plugin$(SDKBOX_PLUGIN_NAME).h"'
	}
	m = ModSource(cfg)
	m.apply_modify()

	# java code
	# cfg = {'dir': cur_dir,
	# 'file': 'Cocos2dxActivity.java',
	# 'class': 'Cocos2dxActivity',
	# 'function': 'onCreate(',
	# 'position': 'after',
	# 'target': 'onLoadNativeLibraries();',
	# 'content': 'sdkbox.init();',
	# 'header': 'import android.content.Intent;\rimport com.sdkbox.plugin.SDKBox;'
	# }
	# m = ModSource(cfg)
	# m.apply_modify()

	# cfg = {'dir': cur_dir,
	# 'file': 'Cocos2dxActivity.java',
	# 'class': 'Cocos2dxActivity',
	# 'function': 'onStart',
	# 'position': 'after',
	# 'target': 'super.onStart();',
	# 'content': 'sdkbox.init();',
	# 'content_a':'@Override\rprotected void onStart() {\rsuper.onStart();\rSDKBox.onStart();\r}',
	# 'header': 'import android.content.Intent;\rimport com.sdkbox.plugin.SDKBox;'
	# }
	# m = ModSource(cfg)
	# m.apply_modify()


if __name__ == '__main__':
	main()
