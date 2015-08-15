from blessings import Terminal

t = Terminal()


#======= colorcode ========

def up(string):
  return t.bold(t.green(string)) 

def down(string):
  return t.bold(t.red(string)) 
  
def num_color(number):
  if number < 0:
    return down(str(number)) 
  else:
    return up(str(number)) 

def str_color(string,number):
  if number < 0:
    return down(string) 
  else:
    return up(string)


  
