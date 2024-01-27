class Interpreter:

    def __init__(self):
        self.stack = []
        self.enviroment = {}

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.enviroment[name] = val

    def LOAD_NAME(self, name):
        val = self.enviroment[name]
        self.stack.append(val)

    def parse_argument(self, instruction, argument, what_to_execute):
        numbers = ["LOAD_VALUE"]
        names = ["LOAD_NAME", "STORE_NAME"]

        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]

        return argument

    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)

            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(argument)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()
            elif instruction == "STORE_NAME":
                self.STORE_NAME(argument)
            elif instruction == "LOAD_NAME":
                self.LOAD_NAME(argument)

    def execute(self, what_to_execute):
        instructions = what_to_execute["instruction"]
        for each_step in instructions:
            instruction, argument = each_step
            argument, self.parse_argument(instruction, argument, what_to_execute)
            bytecode_methode = getattr(self, instruction)
            if argument is None:
                bytecode_methode()
            else:
                bytecode_methode(argument)


# Let's use python internal to get some real bytecode
def get_bytecode_example():
    # Function definition
    def cond():
        x = 3
        if x < 5:
            return 'OK!'
        else:
            return 'NOT OK :('

    # Get the bytecode
    bytecode = cond.__code__.co_code
    bytes_list = list(bytecode)
    print(f"Raw byte code: {bytecode} \nInt representation: {bytes_list}")

    import dis
    info = dis.dis(cond)
    print(f"Using dis:\n{info}")


def get_bytecode_example_loop():
    # Function definition
    def loop():
        x = 0
        for i in range(5):
            x += i

    def while_loop():
        x = 0
        i = 0
        while i < 5:
            x += i
            i += 1

    def comprehension():
        x = [i for i in range(5)]

    # Get the bytecode
    import dis
    print(f"Using dis on loop:")
    dis.dis(loop)

    print(f"\nUsing dis on while loop:")
    dis.dis(while_loop)

    print(f"List comprehension:")
    dis.dis(comprehension)



def basic_instr_set():
    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("LOAD_VALUE", 1),
                         ("ADD_TWO_VALUES", None),
                         ("LOAD_VALUE", 2),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [7, 5, 8]
    }
    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)


def var_instr_dummy_set():

    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("STORE_NAME", 0),
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0),
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names": ["a", "b"]
    }

    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)


if __name__ == '__main__':
    get_bytecode_example_loop()
