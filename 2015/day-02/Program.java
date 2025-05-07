import java.util.Scanner;
import java.util.ArrayList;
import java.io.File;
import java.io.FileNotFoundException;

public class Program {

  public static String inputPath = "./input.txt";

  public static void main(String[] args) {

      ArrayList<String> input = getInput();

      int totalWrappingPaper = 0;
      int totalRibbon = 0; 

      for (String dimension : input) {
        int[] dim = getDimensionsFromString(dimension);
        totalWrappingPaper += getNeededWrappingPaper(dim);
        totalRibbon += getNeededRibbon(dim);
      }

      System.out.println("The needed square feet of wrapping paper is: " + totalWrappingPaper);
      System.out.println("The needed feet of ribbon is: " + totalRibbon);

  }

  public static int[] getDimensionsFromString(String sDim) {
    String curSDim = sDim;
    int[] dimensions = new int[3];

    for (int i = 0; i < 3; i++) {
      int stopIndex = curSDim.indexOf("x");

      if (stopIndex == -1) {
        stopIndex = curSDim.length();
      }

      dimensions[i] = Integer.parseInt(curSDim.substring(0, stopIndex));

      if (i < 2) {
        curSDim = curSDim.substring(stopIndex+1);
      }
    }

    return dimensions;
  }

  public static int getNeededWrappingPaper(int[] dim) {
    int[] faces = new int[3];
    faces[0] = dim[0]*dim[1];
    faces[1] = dim[0]*dim[2];
    faces[2] = dim[1]*dim[2];

    int smallestFace = faces[0];

    for (int face : faces) {
      if (face < smallestFace) {
        smallestFace = face;
      }
    }

    return 2*faces[0] + 2*faces[1] + 2*faces[2] + smallestFace;
  }

  public static int getNeededRibbon(int[] dim) {
    int[] perimeters = new int[3];
    perimeters[0] = dim[0]*2+dim[1]*2;
    perimeters[1] = dim[0]*2+dim[2]*2;
    perimeters[2] = dim[1]*2+dim[2]*2;

    int smallestPerimeter = perimeters[0];

    for (int perim : perimeters) {
      if (perim < smallestPerimeter) {
        smallestPerimeter = perim;
      }
    }

    return smallestPerimeter + dim[0]*dim[1]*dim[2];
  }

  public static ArrayList<String> getInput() {

    try {

      File file = new File(inputPath);
      Scanner reader = new Scanner(file);

      ArrayList<String> input = new ArrayList<String>();

      while (reader.hasNextLine()) {
        input.add(reader.nextLine());
      }

      reader.close();

      return input;

    } catch (FileNotFoundException e) {
      System.out.println("Could not find: " + inputPath);
    }

    return new ArrayList<String>();

  }

}