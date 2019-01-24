import lightargs
import sys


def _doA(a1,a2):

    print "A:",a1,a2

    
def _doB(b1,b2,b3):

    print "B:",b1,b2,b3

    
def _sum(value1,value2):

    print "sum:",float(value1)+float(value2)

    
def _hidden():

    print "called hidden function !"
    

lightargs.set_usage("welcome to lightargs example !")
    

lightargs.add( "doA",
               _doA,
               nb_args=2,
               args_label=("a1","a2"),
               defaults=("default_a1","default_a2"),
               man="print 'A:' followed by a1 and a2 arguments",
               category="example")


lightargs.add( "doB",
               _doB,
               nb_args=3,
               args_label=("b1","b2","b3"),
               defaults=("default_b1","default_b2","default_b3"),
               man="print 'B:' followed by b1, b2 and b3 arguments",
               category="example")

lightargs.add("sum",
              _sum,
              nb_args=2,
              man="print the sum of the two arguments",
              category="utils")


lightargs.add("hidden",
              _hidden,
              nb_args=0,
              man="because in category 'hidden', this argument will not shown up in the doc",
              category="hidden")



if __name__ == "__main__":

    try:
        lightargs.execute(sys.argv[1:])
    except lightargs.WrongParameters as e:
        print str(e)
    except lightargs.UnknownArgument as e:
        print str(e)

