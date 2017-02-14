#!/usr/bin/env python

class abstractWalker:
	def walk(self,cursor):
		pass

	def dump(self,cursor):
		print "Start Dump:"+str(cursor.kind)+"-"+cursor.spelling
		self.printChildren(cursor,0)

	def printChildren(self,cursor,depth):
		it = cursor.get_children()
		for c in it:
			print "|"+"-"*(depth+1)+str(c.kind)+" "+c.spelling
			self.printChildren(c,depth+1)