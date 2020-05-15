# MARK: -- Queue for BFS
class Queue:
	def __init__(self):
		self.queue = []
	def enqueue(self, value):
		self.queue.append(value)
	def dequeue(self):
		if self.size() > 0:
			return self.queue.pop(0)
		else:
			return None
	def size(self):
		return len(self.queue)

# MARK: -- Stack for DFS
class Stack:
	def __init__(self):
		self.stack = []
	def push(self, value):
		self.stack.append(value)
	def pop(self):
		if self.size() > 0:
			return self.stack.pop()
		else:
			return None
	def size(self):
		return len(self.stack)
	def peek(self):
		return self.stack[-1]