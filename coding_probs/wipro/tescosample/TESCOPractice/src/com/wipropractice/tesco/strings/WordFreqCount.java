package com.wipropractice.tesco.strings;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Objects;

public class WordFreqCount {
	public static void main(String[] args) {
		String p = "Hello World Hello 123 Hello 123";
		Map<String, Integer> map = countWordFrequency(p);
		if (!map.isEmpty()) {
			for (Entry<String, Integer> entry : map.entrySet())
				System.out.print("(" + entry.getKey() + "," + entry.getValue() + ")");
		}
	}

	private static Map<String, Integer> countWordFrequency(String text) {
		if (Objects.isNull(text) || text.isEmpty())
			return Collections.emptyMap();
		String[] words = text.split("\\s+");
		Map<String, Integer> map = new LinkedHashMap<>();
		for (String word : words) {
			String trimmedWord = word.trim();
			Integer count = null;
			if (!trimmedWord.isEmpty()) {
				count = map.getOrDefault(trimmedWord, 0);
				map.put(trimmedWord, count + 1);
			}
		}
		return map;
	}
}
