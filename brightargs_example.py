from lightargs import BrightArgs,Set,Range


bright = BrightArgs("Welcome to BrightArgs example")
bright.add_operation("operation1","operation number one")
bright.add_option("option1",1,"option number 1",int,integrity_checks=[Set(1,2,3),Range(1,3)])
bright.print_help()


bright.parse(["--operation1","-option1","3"])

bright.print_status()
