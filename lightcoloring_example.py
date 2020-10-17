
from lightargs import lightcoloring as lc

a = lc.format("\nWelcome to light coloring example",lc.green,lc.bright)

b = lc.format("This is a {} to have you {}\n",
              ("pleasure",lc.cyan,lc.bright),
              ("here",lc.red),
              default=(lc.green,lc.dim))

print(a)
print(b)
