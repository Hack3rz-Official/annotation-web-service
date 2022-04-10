export function useRandomCode(language) {
  if (language == "java") {
    return `import java.util.Scanner;
    
    public class HelloWorld {
    
        public static void main(String[] args) {
    
            Scanner reader = new Scanner(System.in);
            System.out.print("Enter a number: ");
    
            // nextInt() reads the next integer from the keyboard
            int number = reader.nextInt();
    
            System.out.println("You entered: " + number);
        }
    }`;
  } else if (language == "python3") {
    return `# This program adds two numbers
    
    num1 = 1.5
    num2 = 6.3
    
    # Add two numbers
    sum = num1 + num2
    
    # Display the sum
    print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))`;
  } else if (language == "kotlin") {
    return `fun main() {
        val name = "stranger"        // Declare your first variable
        println("Hi, $name!")        // ...and use it!
        print("Current count:")
        for (i in 0..10) {           // Loop over a range from 0 to 10
            print(" $i")
        }
    }`;
  }
}
