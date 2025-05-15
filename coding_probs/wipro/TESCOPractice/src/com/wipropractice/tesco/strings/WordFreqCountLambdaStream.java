package com.wipropractice.tesco.strings;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.function.Function;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class WordFreqCountLambdaStream {
	public static void main(String[] args) {
		String p = "Hello World Hello 123 Hello 123";
		Map<String, Long> map = countWords(p);
		if (!map.isEmpty()) {
			for (Entry<String, Long> entry : map.entrySet())
				System.out.print("(" + entry.getKey() + "," + entry.getValue() + ")");
		}
	}

	private static Map<String, Long> countWords(String p) {
		Pattern pattern = Pattern.compile("\\s+");
		return pattern.splitAsStream(p).filter(token->!token.trim().isEmpty()).collect(Collectors.groupingBy(Function.identity(),LinkedHashMap::new,Collectors.counting()));
		
	}
}
