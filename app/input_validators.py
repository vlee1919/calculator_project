


class input_validator:
    def validate_length(value):
        try:
            # Splits the user input into parts and checks if it has exactly three components
            input_split = value.split()
            if len(input_split) != 3:
                print("Error: Invalid input format. Please use: <operation> <number1> <number2>")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

        return True