#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from mod_source import ModSource

def main():
	sys.path.append("..")

	# cpp code
	cfg = {'dir': '.',
	'file': 'AppDelegate.cpp',
	'class': 'AppDelegate',
	'function': 'applicationDidFinishLaunching',
	'position': 'before',
	'content': 'sdkbox::Plugin$(SDKBOX_PLUGIN_NAME)::init();',
	'header': '#include "Plugin$(SDKBOX_PLUGIN_NAME)/Plugin$(SDKBOX_PLUGIN_NAME).h"'
	}
	m = ModSource(cfg)
	m.apply_modify()

	# java code
	cfg = {'dir': '.',
	'file': 'Cocos2dxActivity.java',
	'class': 'Cocos2dxActivity',
	'function': 'onCreate',
	'position': 'after',
	'target': 'onLoadNativeLibraries();',
	'content': 'sdkbox.init();',
	'header': 'import android.content.Intent;\rimport com.sdkbox.plugin.SDKBox;'
	}
	m = ModSource(cfg)
	m.apply_modify()

	cfg = {'dir': '.',
	'file': 'Cocos2dxActivity.java',
	'class': 'Cocos2dxActivity',
	'function': 'onStart',
	'position': 'after',
	'target': 'super.onStart();',
	'content': 'sdkbox.init();',
	'content_a':'@Override\rprotected void onStart() {\rsuper.onStart();\rSDKBox.onStart();\r}',
	'header': 'import android.content.Intent;\rimport com.sdkbox.plugin.SDKBox;'
	}
	m = ModSource(cfg)
	m.apply_modify()

if __name__ == '__main__':
	main()
