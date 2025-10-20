# EXCEPTIONS


# SINGLE LINE EXCEPTION
# def second_item(x) -> int:
#     try:
#         return x[10]
#     except IndexError:
#         print("incorrect type")
#     except TypeError:
#         print("missing index")
#     # else:
#     #     print(second_item(0))
#     finally:
#         print("Completed")

# print(second_item(0))



# MULTILINE  EXCEPTIONS
# try:
#     value = int("123")
# except(ValueError, TypeError) as e:
#     print("Value/Type error: ", e)

# def second_item(x) -> int:
#     try:
#         return x[10]
#     except (IndexError,TypeError) as e:
#         return f"Error: {e}"
#     finally:
#         print("Completed")

# print(second_item(0))


# RAISING ERRORS

# def withdraw(balance, amount):
#     if amount > balance:
#         raise ValueError("Insufficient Funds")
#     return balance - amount

# print(withdraw(50, 100))


# CUSTOM EXCEPTION 
# class ToManyTry(Exception):
#     pass

# raise ToManyTry("Too many attempts")


# CLASSWORK

# def ask_for_int():
#     min_val = 5
#     max_val = 10
#     retries = 3

#     try:
#         prompt = "Enter a your value: "
#         if prompt == min_val 


class TooManyTriesError(Exception):
    """Custom exception raised when user exceeds the number of allowed tries."""
    pass


def get_number_in_range(min_val, max_val, total_tries=3):
    tries = 0
    
    while tries < total_tries:
        try:
            prompt = int(input(f"Enter a number between {min_val} and {max_val}: "))
            
            if min_val <= prompt <= max_val:
                print(f" Great! {prompt} is within the range.")
                return prompt
            else:
                print(f" {prompt} is out of range. Try again.")
                tries += 1
                
        except ValueError:
            print(" Invalid input. Please enter a valid number.")
            tries += 1

    # If we reach this point, user has exceeded allowed attempts
    raise TooManyTriesError("You have exceeded the maximum number of tries.")


# Example usage
if __name__ == "__main__":
    try:
        number = get_number_in_range(2, 10)
    except TooManyTriesError as e:
        print(e)
    finally:
        print("process complete")


