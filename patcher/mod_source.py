#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import platform

class CodeAnalytics(object):
	"""analytics source code"""
	def __init__(self, arg):
		super(CodeAnalytics, self).__init__()
		self.arg = arg
		self.cur_dir = os.path.dirname(os.path.realpath(__file__))
		print 'current dir:' + self.cur_dir
		self.search_dir = os.path.realpath(os.path.join(self.cur_dir, arg['dir']))
		self.search_dir = arg['dir']
		print 'search dir:' + self.search_dir
		self.scope = {}
		self.search_and_read_lines()

	def get_platform_name(self):
		p = platform.system()
		return p

	def get_line_end(self):
		platform = self.get_platform_name()
		if 'Darwin' == platform:
			return '\n'
		elif 'Windows' == platform:
			return '\r\n'
		else: # start with 'Linux'
			return '\n'

	def set_scope_line_start(self, linenumber, scope = None):
		if None == scope:
			scope = self.scope
		scope['start_line'] = linenumber

	def set_scope_line_end(self, linenumber, scope = None):
		if None == scope:
			scope = self.scope
		if -1 == linenumber:
			scope['end_line'] = len(self.lines) - 1
		else:
			scope['end_line'] = linenumber

	def set_scope_line_start_column(self, column, scope = None):
		if None == scope:
			scope = self.scope
		scope['start_column'] = column

	def set_scope_line_end_column(self, column, scope = None):
		if None == scope:
			scope = self.scope
		if -1 == column:
			scope['end_column'] = len(self.lines[self.get_scope_line_end(scope)]) - 1
		else:
			scope['end_column'] = column

	def get_scope_line_start(self, scope = None):
		if None == scope:
			scope = self.scope
		return scope['start_line']

	def get_scope_line_end(self, scope = None):
		if None == scope:
			scope = self.scope
		return scope['end_line']

	def get_scope_line_start_column(self, scope = None):
		if None == scope:
			scope = self.scope
		return scope['start_column']

	def get_scope_line_end_column(self, scope = None):
		if None == scope:
			scope = self.scope
		return scope['end_column']

	def scope_line_start_increase(self, val, scope = None):
		if self.scope_length_is_0(scope):
			print 'Warning! Scope lenght is 0, not decrease'
			return

		if None == scope:
			scope = self.scope
		line = self.get_scope_line_start(scope) + val
		self.set_scope_line_start(line, scope)

	def scope_start_column_increase(self, val, scope = None):
		if self.scope_length_is_0(scope):
			print 'Warning! Scope lenght is 0, not increase'
			return

		if None == scope:
			scope = self.scope
		column = self.get_scope_line_start_column(scope) + 1
		if column == len(self.lines[self.get_scope_line_start(scope)]):
			self.scope_line_start_increase(1)
			self.set_scope_line_start_column(0, scope)
		else:
			self.set_scope_line_start_column(column, scope)

	def scope_line_end_decrease(self, val, scope = None):
		if self.scope_length_is_0(scope):
			print 'Warning! Scope lenght is 0, not decrease'
			return

		if None == scope:
			scope = self.scope
		line = self.get_scope_line_end(scope) - val
		self.set_scope_line_end(line, scope)

	def scope_end_column_decrease(self, val, scope = None):
		if self.scope_length_is_0(scope):
			print 'Warning! Scope lenght is 0, not decrease'
			return

		if None == scope:
			scope = self.scope
		column = self.get_scope_line_end_column(scope) - 1
		if column < 0:
			self.scope_line_end_decrease(1, scope)
			self.set_scope_line_end_column(-1, scope)
		else:
			self.set_scope_line_end_column(column, scope)

	def scope_length_is_0(self, scope = None):
		if None == scope:
			scope = self.scope
		if self.get_scope_line_start(scope) == self.get_scope_line_end(scope) and self.get_scope_line_start_column(scope) == self.get_scope_line_end_column(scope):
			return True
		return False

	def set_class_scope(self):
		self.scope_class = {}
		self.set_scope_line_start(0, self.scope_class)
		self.set_scope_line_end(-1, self.scope_class)
		self.set_scope_line_start_column(0, self.scope_class)
		self.set_scope_line_end_column(-1, self.scope_class)

	def set_function_scope(self):
		function_name = self.get_function_name()
		scope = self.find_scope(function_name, self.scope_class)
		self.scope_function = scope.copy()

	def find_scope(self, word, in_scope):
		lines = self.lines
		start_line = self.get_scope_line_start(in_scope)
		end_line = self.get_scope_line_end(in_scope)
		start_column = self.get_scope_line_start_column(in_scope)
		end_column = self.get_scope_line_end_column(in_scope)
		scope = {}
		column = 0
		brace_count = 0
		state_code = 0 #0:search key word 1:search left brace 2:search right brace 3:end
		for i in xrange(start_line, end_line + 1):
			line = lines[i]
			if i == start_line:
				column = start_column
			if i == end_line:
				line = line[:end_line]
			if 0 == state_code:
				pos = line.find(word, column)
				if pos >= 0:
					state_code = 1
					column = pos
			if 1 == state_code:
				pos = line.find('{', column)
				if pos >= 0:
					self.set_scope_line_start(i, scope)
					self.set_scope_line_start_column(pos, scope)
					state_code = 2
					column = pos
			if 2 == state_code:
				brace_l = line.count('{', column)
				brace_r = line.count('}', column)
				brace_count_t = brace_count + brace_l
				brace_count_t = brace_count_t - brace_r
				if brace_count_t <= 0 and (brace_l > 0 or brace_r > 0):
					char_idx = 0
					for char in line:
						if char_idx < column:
							char_idx += 1
							continue
						if '{' == char:
							brace_count += 1
						elif '}' == char:
							brace_count -= 1
						if 0 == brace_count:
							self.set_scope_line_end(i, scope)
							self.set_scope_line_end_column(char_idx, scope)
							state_code = 3
							break
						char_idx += 1
				else:
					brace_count = brace_count_t
			if 3 == state_code:
				break
			column = 0
		print '(%s) scrope:' % word
		print scope
		return scope

	def get_function_name(self):
		return self.arg['function']

	def search_and_read_lines(self):
		search_dir = self.search_dir
		search_file = self.arg['file']
		for dir_, dirnames, filenames in os.walk(search_dir):
			if search_file in filenames:
				file_path = os.path.join(dir_, search_file)
				print 'find file (%s)' % file_path
				f = open(file_path)
				self.lines = f.readlines()
				f.close()
				self.file_path = file_path
				break
		if 0 == len(self.lines):
			raise RuntimeError('file (%s) is empty' % self.file_path)
		if len(self.lines) < 50:
			print 'file lines number:%d' % len(self.lines)

	def save_lines_to_file(self, lines):
		f = open(self.file_path, 'w')
		f.write(''.join(lines))
		f.close()

	def get_target_lines(self):
		cfg = self.arg
		if not 'target' in cfg:
			return []
		target = cfg['target']
		if not target or 0 == len(target):
			return []
		return target.splitlines()

	def find_modify_scope(self):
		target_lines = self.get_target_lines()
		target_scope = {}

		if not target_lines or 0 == len(target_lines):
			# target is none use whole function body as target
			target_scope = self.scope_function.copy()
			self.scope_start_column_increase(1, target_scope)
			self.scope_end_column_decrease(1, target_scope)
			self.target_scope = target_scope
			print self.target_scope
			return target_scope

		# init target scope
		self.set_scope_line_start(-1, target_scope)
		self.set_scope_line_end(-1, target_scope)
		self.set_scope_line_start_column(-1, target_scope)
		self.set_scope_line_end_column(-1, target_scope)

		scope_function = self.scope_function
		lines = self.lines
		column = 0
		line_start = self.get_scope_line_start(scope_function)
		line_end = self.get_scope_line_end(scope_function)
		target_line_idx = 0
		for i in xrange(line_start, line_end):
			line = lines[i]
			if i == line_start:
				column = self.get_scope_line_start_column(scope_function)
			if i == line_end:
				line = line[:self.get_scope_line_end_column(scope_function)]

			target_line = target_lines[target_line_idx]
			if 0 == target_line_idx:
				idx = line.find(target_line, column)
				if idx >= 0:
					target_line_idx += 1
					self.set_scope_line_start(i, target_scope)
					self.set_scope_line_start_column(idx, target_scope)
					if 1 == len(target_lines):
						self.set_scope_line_end(i, target_scope)
						self.set_scope_line_end_column(idx + len(target_line), target_scope)
						self.target_scope = target_scope
						return
			elif target_line_idx == len(target_lines) - 1:
				if line.strip().startswith(target_line):
					self.set_scope_line_end(i, target_scope)
					self.set_scope_line_end_column(line.find(target_line) + len(target_line), target_scope)
					self.target_scope = target_scope
					return
				else:
					target_line_idx = 0
			elif line_compare(target_line, line):
				target_line_idx += 1
			else:
				target_line_idx = 0
			column = 0

		raise RuntimeError("can not find target scrope in function")

	def add_header_if(self, lines):
		cfg = self.arg
		header_lines = cfg['header'].splitlines()
		need_add_header = []
		for h in header_lines:
			header_has_include = False
			for line in lines:
				if self.line_compare(line, h):
					header_has_include = True
					break
			if not header_has_include:
				need_add_header.append(h)

		if 0 == len(need_add_header):
			return lines
		last_include_line = -1
		i = 0
		for line in lines:
			if line.startswith(self.get_header_tag()):
				last_include_line = i
			i += 1
		last_include_line += 1
		for line in need_add_header:
			lines.insert(last_include_line, line)
			last_include_line += 1
		return lines

	def get_header_tag(self):
		return 'unkonw'

	def apply_modify(self):
		lines = self.lines
		cfg = self.arg
		content = cfg['content']
		new_lines = []

		self.scope = self.target_scope
		if cfg['position'] == 'before':
			new_lines = lines
			line_idx = self.get_scope_line_start()
			line1 = lines[line_idx][:self.get_scope_line_start_column()]
			line2 = lines[line_idx][self.get_scope_line_start_column():]
			new_lines[line_idx] = line1
			line_idx += 1

			new_lines.insert(line_idx, '')
			line_idx += 1
			new_lines.insert(line_idx, self.get_line_end() + '    /*** SDKbox auto modify Begin ***/' + self.get_line_end())
			line_idx += 1
			new_lines.insert(line_idx, '    ' + content)
			line_idx += 1
			new_lines.insert(line_idx, self.get_line_end() + '    /*** SDKbox auto modify End ***/' + self.get_line_end())
			line_idx += 1
			new_lines.insert(line_idx, '')
			line_idx += 1

			new_lines.insert(line_idx, '    ' + line2)
		elif cfg['position'] == 'after':
			new_lines = lines
			line_idx = self.get_scope_line_end()
			line1 = lines[line_idx][:self.get_scope_line_end_column()]
			line2 = lines[line_idx][self.get_scope_line_end_column():]
			new_lines[line_idx] = line1
			line_idx += 1

			new_lines.insert(line_idx, '')
			line_idx += 1
			new_lines.insert(line_idx, self.get_line_end() + '    /*** SDKbox auto modify Begin ***/' + self.get_line_end())
			line_idx += 1
			new_lines.insert(line_idx, '    ' + content)
			line_idx += 1
			new_lines.insert(line_idx, self.get_line_end() + '    /*** SDKbox auto modify End ***/' + self.get_line_end())
			line_idx += 1
			new_lines.insert(line_idx, '')
			line_idx += 1

			new_lines.insert(line_idx, '    ' + line2)
		else:
			i = 0
			line_start = self.get_scope_line_start()
			line_end = self.get_scope_line_end()
			for line in lines:
				if i == line_start:
					new_lines.append(line[:self.get_scope_line_start()])

					new_lines.append(self.get_line_end() + '/*** SDKbox auto modify Begin ***/' + self.get_line_end())
					new_lines.append(content)
				if i == line_end:
					new_lines.append(self.get_line_end() + '/*** SDKbox auto modify End ***/' + self.get_line_end())
					new_lines.append(self.get_line_end())

					new_lines.append(line[scrope['end_idx']:])
				if i < line_start or i > line_end:
					new_lines.append(line)
				i += 1

		return new_lines

	def line_compare(self, line1, line2):
		link = re.compile('\t+')
		linea = re.sub(link, ' ', line1)
		lineb = re.sub(link, ' ', line2)
		link = re.compile(' +')
		linea = re.sub(link, ' ', linea)
		lineb = re.sub(link, ' ', lineb)
		linea = linea.strip()
		lineb = lineb.strip()
		if linea == lineb:
			return True
		else:
			return False

	def modify(self):
		file_path = self.file_path
		self.set_class_scope()
		self.set_function_scope()
		if self.scope_function:
			scope = self.find_modify_scope()
		else:
			scope = self.scope_class.copy()
			self.set_scope_line_start(self.get_scope_line_end(scope), scope)
			self.set_scope_line_start_column(self.get_scope_line_end_column(scope), scope)
			self.target_scope = scope
			self.arg['content'] = self.arg['content_a']
			
		lines = self.apply_modify()
		lines = self.add_header_if(lines)
		self.save_lines_to_file(lines)

class CppAnalytics(CodeAnalytics):
	"""docstring for CppAnalytics"""
	def __init__(self, arg):
		super(CppAnalytics, self).__init__(arg)

	def get_header_tag(self):
		return '#include '

	def get_function_name(self):
		if self.arg['class']:
			return self.arg['class'] + '::' + self.arg['function']
		else:
			return self.arg['function']

class JavaAnalytics(CodeAnalytics):
	"""docstring for JavaAnalytics"""
	def __init__(self, arg):
		super(JavaAnalytics, self).__init__(arg)

	def set_class_scope(self):
		super(JavaAnalytics, self).set_class_scope()
		scope = self.find_scope('class Cocos2dxActivity', self.scope_class)
		self.scope_class = scope
		self.scope = scope.copy()

	def get_header_tag(self):
		return 'import '

class ModSource(object):
	"""docstring for ModSource"""
	def __init__(self, arg):
		super(ModSource, self).__init__()
		self.arg = arg

	def apply_modify(self):
		fileType = os.path.splitext(self.arg['file'])[-1]
		mod = None
		if '.cpp' == fileType or '.h' == fileType:
			mod = CppAnalytics(self.arg)
		elif '.java' == fileType:
			mod = JavaAnalytics(self.arg)
		else:
			raise RuntimeError('Unkonw file type:' + fileType)
		mod.modify()

if __name__ == '__main__':
	# cfg = {'dir': '.',
	# 'file': 'AppDelegate.cpp',
	# 'class': 'AppDelegate',
	# 'function': 'applicationDidFinishLaunching',
	# 'position': 'before',
	# 'target': 'auto director = Director::getInstance();',
	# 'content': 'sdkbox.init();',
	# 'header': '#include "A.h"\r#include "HelloWorldScene.h"\r#include "B.h"'
	# }
	# cfg = {'dir': '.',
	# 'file': 'Cocos2dxActivity.java',
	# 'class': 'Cocos2dxActivity',
	# 'function': 'onCreate',
	# 'position': 'after',
	# 'target': 'onLoadNativeLibraries();',
	# 'content': 'sdkbox.init();',
	# 'header': 'import android.content.Intent;\rimport com.sdkbox.plugin.SDKBox;'
	# }
	cfg = {'dir': '.',
	'file': 'Cocos2dxActivity.java',
	'class': 'Cocos2dxActivity',
	'function': 'onStart',
	'position': 'after',
	'target': 'super.onStart();',
	'content': 'sdkbox.init();',
	'content_a':'@Override\nprotected void onStart() {\nsuper.onStart();\nSDKBox.onStart();\n}',
	'header': 'import android.content.Intent;\nimport com.sdkbox.plugin.SDKBox;'
	}

	

	m = ModSource(cfg)
	m.apply_modify()
