# First In First Out (FIFO) data structure

class Queue:
    def __init__(self):
        self.queue = []
    
    def empty(self):
        return self.queue == []
    
    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.empty():
            return self.queue.pop(0)
        return None
        
    def removeTail(self):
        if not self.empty():
            return self.queue.pop()
        return None
        
    def peek(self):
        if not self.empty():
            return self.queue[0]
        return None
        
    def end(self):
        if not self.empty():
            return self.queue[-1]
        return None
        
    def size(self):
        return len(self.queue)
    
    def clear(self):
        self.queue.clear()
    
    def __str__(self):
        formatted_element = [str(element) for element in self.queue]
        return f"Queue: [{' -> '.join(formatted_element)}]"
    

