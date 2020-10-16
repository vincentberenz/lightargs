# Copyright 2020 @ Max Planck Gesellschaft


def _check_class(name,class_):
    if not isinstance(name,class_):
        error = str("operation {} "+
                    "should be a {} (it is a  {})")
        raise TypeError(error.format(name,class_,name.__class__))


class Range:

    def __init__(self,min_v,max_v):
        self._min_v = min_v
        self._max_v = max_v

    def __str__(self):
        return repr([self._min_v,self._max_v])

    def help(self):
        s = "value should be between {} and {}"
        return s.format(self._min_v,self._max_v)
        
    def check(self,value): 
        try :
            smaller = value < self._min_v
        except:
            error = str("failed to compare value {} (option {})"+
                        " with range {}")
            raise ValueError(error.format(value,name,str(self)))
        if smaller:
            error = str("value {} for option {} is too small "+
                        "(range:{})")
            raise ValueError(error.format(value,name,str(self)))
        try :
            bigger = value > self._max_v
        except:
            error = str("failed to compare value {} (option {})"+
                        " with range {}")
            raise ValueError(error.format(value,name,str(self)))
        if bigger:
            error = str("value {} for option {} is too big "+
                        "(range:{})")
            raise ValueError(error.format(value,name,str(self)))

class Set:
    
    def __init__(self,*authorized):
        self._authorized = authorized

    def __str__(self):
        return ",".join([str(a) for a in self._authorized])

    def help(self):
        return "value should be in: {}".format(str(self))
    
    def check(self,value):
        if value not in self._authorized:
            error = str("{} not in authorized values ({})")
            raise ValueError(error.format(value,str(self)))
        
class BrightArgs:

    def __init__(self,help_str):
        self._help = help_str
        self._helps = {}
        self._classes = {}
        self._integrity_checks = {}
        self._options = set()
        self._operations = set()
        self._defaults = {}

    def __str__(self):
        r = ["\n"]
        args = sorted(self._options.union(self._operations))
        for arg in args:
            r.append("\t{}:\t{}".format(arg,getattr(self,arg)))
        r.append("\n")
        return "\n".join(r)
            
    def _check_duplicate(self,arg_type,name):
        if name in self._help:
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

    def _check_integrity(self,name,value):
        checks = self._integrity_checks[name]
        if not checks:
            return
        for check in checks:
            check.check(value)
    
    def add_operation(self,name,help_str):
        _check_class(name,str)
        self._check_duplicate("operation",name)
        setattr(self,name,False)
        self._helps[name]=str(help_str)
        self._operations.add(name)
        self._integrity_checks[name]=None
        
    def add_option(self,name,default,help_str,class_,
                   integrity_checks=[]):
        _check_class(name,str)
        self._check_duplicate("option",name)
        setattr(self,name,default)
        self._helps[name]=str(help_str)
        self._classes[name]=class_
        self._integrity_checks[name]=integrity_checks
        self._options.add(name)
        self._defaults[name]=default
        
    def _set_operation_value(self,name,value):
        if not isinstance(value,bool):
            error = "{} should be set a boolean value ({} is {})"
            raise ValueError(error.format(name,value,value.__class__))
        setattr(self,name,value)
        
    def _set_option_value(self,name,value):
        try:
            value = self._classes[name](value)
        except:
            error = "failed to cast {} to {} (option {})"
            raise ValueError(error.format(value,
                                          self._classes[name],name))
        self._check_integrity(name,value)
        setattr(self,name,value)

    def _complain_unknown(self,unknown):
        error = "unkown argument: {}. Known arguments: {}"
        known_options = ",".join(["--"+o for o in self._options])
        known_operations = ",".join(["-"+o for o in self._operations])
        known_arguments = ",".join([known_options,known_operations])
        raise ValueError(error.format(unknown,known_arguments))
        
    def _parse_single(self,args,index):
        operation = self._is_operation(args[index])
        if operation:
            self._set_operation_value(args[index],True)
            return False # do not skip next argment
        option = self._is_option(args[index])
        if option:
            if index>=len(args):
                error = "failed to read value for option {}"
                raise ValueError(error.format(option))
            value = args[index+1]
            self._set_option_value(option,value)
            return True # skip next argument (value of the option)
        self._complain_unknown(args[index])
        
    def parse(self,args):
        skip=False
        for index in range(len(args)):
            if skip:
                skip=False
            else:
                skip = self._parse_single(args,index)

    def _print_option_help(self,name):
        s = str("\t\t--{} ({}, default:{})\t{}{}")
        class_ = str(self._classes[name])
        if "'" in class_:
            class_ = class_[class_.find("'")+1:class_.rfind("'")]
        default = self._defaults[name]
        help_ = self._helps[name]
        if help_ is None:
            help_ = ""
        integrity_str = self._integrity_checks_str(name)
        print(s.format(name,class_,default,help_,integrity_str))

    def _integrity_checks_str(self,name):
        integrity_checks = self._integrity_checks[name]
        if not integrity_checks :
            return ""
        r = ["\t\t\t\t"]
        for ic in integrity_checks:
            r.append(ic.help())
        return "\n\t\t\t\t".join(r)
        
    def _print_operation_help(self,name):
        s = str("\t\t-{}\t{}")
        help_ = self._helps[name]
        if help_ is None:
            help_ = ""
        print(s.format(name,help_))
                
    def print_help(self):
        if self._help :
              print("\n\t{}\n".format(self._help))
        else:
              print("\n")
        for operation in self._operations:
            self._print_operation_help(operation)
        for option in self._options:
              self._print_option_help(option)
        print()

    def print_status(self):
        print(str(self))
