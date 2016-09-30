#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	# print(sys.argv)
	# if len(sys.argv) == 1:
	# 	sys.argv = ['manage.py', 'test']; print('	 - sys.argv override: ' + str(sys.argv))
	
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
