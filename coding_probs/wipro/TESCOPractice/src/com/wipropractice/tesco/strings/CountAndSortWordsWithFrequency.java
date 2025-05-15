package com.wipropractice.tesco.strings;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Objects;

public class CountAndSortWordsWithFrequency {
	public static void main(String[] args) {
		String input = "This is a test! This is Only a test!!";
		List<Entry<String, Integer>> list = countAndSortWords(input);
		if (!list.isEmpty()) {
			System.out.print("(");
			for (int i = 0; i < list.size(); i++) {
				Entry<String, Integer> entry = list.get(i);
				System.out.print("\"" + entry.getKey() + "\"," + entry.getValue());
				if (i < list.size() - 1) {
					System.out.print("),(");
				}
			}
			System.out.println(")");
		} else
			System.out.println("()");
	}

	private static List<Entry<String, Integer>> countAndSortWords(String text) {
		if (Objects.isNull(text) || text.isEmpty())
			return Collections.emptyList();
		String refinedText = text.replaceAll("[^a-zA-Z0-9\\s]", "");
		String[] words = refinedText.split("\\s+");
		Map<String, Integer> map = new LinkedHashMap<>();
		for (String word : words) {
			String trimmedWord = word.trim();
			Integer count = null;
			if (!trimmedWord.isEmpty()) {
				count = map.getOrDefault(trimmedWord, 0);
				map.put(trimmedWord, count + 1);
			}
		}
		List<Entry<String, Integer>> entryList = new ArrayList<>(map.entrySet());
		Collections.sort(entryList, (entry1, entry2) -> entry2.getValue().compareTo(entry1.getValue()));
		return entryList;
	}
}
