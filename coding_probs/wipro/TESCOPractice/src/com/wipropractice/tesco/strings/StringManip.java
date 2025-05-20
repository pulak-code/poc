package com.wipropractice.tesco.strings;

import java.util.ArrayList;
import java.util.List;

public class StringManip {
	public static void main(String[] args) {
		System.out.println(reverseAlphabetic("H@RM@NPR##T&"));
	}
	public static String reverseAlphabetic(String input) {
        // Handle null or empty input strings
        if (input == null || input.isEmpty()) {
            return input;
        }
        char[] charArray = input.toCharArray();
        
        List<Character> alphabeticChars = new ArrayList<>();
        for(char c:charArray) {
        	if (Character.isLetter(c))
        		alphabeticChars.add(c);
        }
        int left = 0;
        int right = alphabeticChars.size() - 1;
        while(left<right) {
        	 char temp = alphabeticChars.get(left);
             alphabeticChars.set(left, alphabeticChars.get(right));
             alphabeticChars.set(right, temp);
             left++;
             right--;
        }
        int alphabeticIndex = 0;
        for (int i = 0; i < charArray.length; i++) {
            if (Character.isLetter(charArray[i])) {
                charArray[i] = alphabeticChars.get(alphabeticIndex);
                alphabeticIndex++;
            }
        }

        return new String(charArray);
	}
}
