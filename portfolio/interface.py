from blessings import Terminal

t = Terminal()

#======= colorcode gain ========
def str_color(number):
  if number < 0:
    return t.bold(t.red(str(number))) 
  else:
    return t.bold(t.green(str(number))) 


