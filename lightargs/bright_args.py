# Copyright 2020 @ Max Planck Gesellschaft

def _check_class(name,class_):
    if not isinstance(name,class_):
        error = str("operation {} "+
                    "should be a {} (it is a  {})")
        raise TypeError(error.format(name,class_,name.__class__))


class BrightArgs:

    def __init__(self):
        self._docs = {}
        self._classes = {}
        self._boundaries = {}
        self._authorized = {}
        self._options = set()
        self._operations = set()

    def _check_duplicate(self,arg_type,name):
        if name in self._doc:
            error = str("{} {} added more than once")
            raise ValueError(error.format(arg_type,name))
        
    def _check_valid(self,arg_type,name):
        if not hasattr(self,name):
            error = str("{} is not a known {}")
            raise ValueError(error.format(name,arg_type))

    def _is_operation(self,arg):
        if arg.startswith("--"):
            if arg[2:] in self._operations:
                return arg[2:]
        return False

    def _is_option(self,arg):
        if arg.startswith("--"):
            return False
        if arg.startswith("-"):
            if arg[1:] in self._options:
                return arg[1:]
        return False

    def _check_boundaries(self,name,value):
        if self._boundaries[name] is None:
            return 
        try :
            smaller = value < self._boundaries[name][0]
        except:
            error = str("failed to compare value {} (option {})"+
                        " with boundaries {}")
            raise ValueError(error.format(value,name,self._boundaries[name]))
        if smaller:
            error = str("value {} for option {} is too small "+
                        "(boundaries:{})")
            raise ValueError(error.format(value,name,self._boundaries[name]))
        try :
            bigger = value > self._boundaries[name][1]
        except:
            error = str("failed to compare value {} (option {})"+
                        " with boundaries {}")
            raise ValueError(error.format(value,name,self._boundaries[name]))
        if bigger:
            error = str("value {} for option {} is too big "+
                        "(boundaries:{})")
            raise ValueError(error.format(value,name,self._boundaries[name]))
        
    def _check_authorized(self,name,value):
        if self._authorized[name] is None:
            return
        if value in self._authorized[name]:
            return
        error = str("value {} not authorized for option {} "+
                    "(valid: {})")
        authorized_list = ",".join([str(a) for a in self._authorized[name]])
        raise ValueError(error.format(value,name,
                                      authorized_list))
        
    def add_operation(self,name,doc):
        _check_class(name,str)
        self._check_duplicate("operation",name)
        self.setattr(self,name,False)
        self._docs[name]=str(doc)
        self._operations.add(name)
        
    def add_option(self,name,default,doc,class_,
                   boundaries=None,
                   authorized=None):
        _check_class(name,str)
        self._check_duplicate("option",name)
        self.setattr(self,name,default)
        self._docs[name]=str(doc)
        self._classes[name]=class_
        self._boundaries[name]=boundaries
        self._authorized[name]=authorized
        self._options.add(name)
        
    def _populate(self,args,index):
        operation = self._is_operation(args[index])
        if operation:
            setattr(self,operation,True)
            return False # do not skip next argment
        option = self._is_option(args[index])
        if option:
            if index>=len(args):
                error = "failed to read value for option {}"
                raise ValueError(error.format(option))
            value = args[index+1]
            try:
                value = self._classes[option](value)
            except:
                error = "failed to cast {} to {} (option {})"
                raise ValueError(error.format(value,
                                              self._classes[option],option))
            self._check_boundaries(option,value)
            self._check_authorized(option,value)
            setattr(self,option,value)
            return True # skip next argument (value of the option)
        error = "unkown argument: {}. Known arguments: {}"
        known_options = ",".join(["--"+o for o in self._options])
        known_operations = ",".join(["-"+o for o in self._operations])
        known_arguments = ",".join(known_options,known_operations)
        raise ValueError(error.format(args[index],known_arguments))
                                   
    def parse(self,args):
        skip=False
        for index in range(len(args)):
            if skip:
                skip=False
            else:
                skip = self._populate(args,index)
                        
    
    
