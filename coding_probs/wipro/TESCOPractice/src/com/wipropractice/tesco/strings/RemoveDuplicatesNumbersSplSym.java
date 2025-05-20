package com.wipropractice.tesco.strings;

import java.util.LinkedHashSet;
import java.util.Set;

public class RemoveDuplicatesNumbersSplSym {

	public static void main(String[] args) {
		Set<Character> seenCharacters = new LinkedHashSet<>();
        StringBuilder result = new StringBuilder();
String input="aabcdcddbabc4e%@6";
        
        for (char c : input.toCharArray()) {
            if (Character.isLetter(c)) {
                char lowerCaseChar = Character.toLowerCase(c);
                if (seenCharacters.add(lowerCaseChar)) {
                    result.append(c);
                }
            }
        }
        System.out.println(result.toString());

	}

}
