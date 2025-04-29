import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Program {

  public static String fileName = "./input.txt";

  public static void main(String[] args) {

      String input = getInput();


      int floor = 0;
      int stepFirstEnteredBasement = -1;
      for (int i = 0; i < input.length(); i++) {
        String command = input.substring(i, i+1);
        if (command.equals("(")) {
          floor += 1;
        } else if (command.equals(")")) {
          floor -= 1;
        }

        if (stepFirstEnteredBasement < 0 && floor < 0) {
          // add one because the scenario uses 1 as the first index
          stepFirstEnteredBasement = i + 1;
        }
      }

      System.out.println("Santa is taken to floor " + floor + ".");
      System.out.println("Santa first reaches the basement on step " + stepFirstEnteredBasement + ".");

  }

  public static String getInput() {

    try {

      File file = new File(fileName);

      Scanner reader = new Scanner(file);

      String text = "";

      while (reader.hasNextLine()) {
        text += reader.nextLine();
      }

      reader.close();

      return text;

    } catch (FileNotFoundException e) {
      System.out.println("Could not find " + fileName);
    }

    return "";

  }

}