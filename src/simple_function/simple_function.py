
def simple_function():
  print("Select a cluster:")
  nums = [10, 20, 30, 40]
  for num in nums:
    print(num)
  selected_num = int(input("Enter the number: "))
  print(f"{selected_num} is selected.")

def main():
  simple_function()

if __name__ == "__main__":
  main()
