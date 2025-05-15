package com.wipropractice.tesco.strings;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Objects;
import java.util.function.Function;
import java.util.regex.Pattern;
import java.util.stream.Collectors;


public class CountAndSortWordsWithFrequencyLambdaStream {
	public static void main(String[] args) {
		String input = "This is a test! Only a test!!";
		List<Entry<String, Long>> list = countAndSortWords(input);
		if (!list.isEmpty()) {
			System.out.print("(");
			for (int i = 0; i < list.size(); i++) {
				Entry<String, Long> entry = list.get(i);
				System.out.print("\"" + entry.getKey() + "\"," + entry.getValue());
				if (i < list.size() - 1) {
					System.out.print("),(");
				}
			}
			System.out.println(")");
		} else
			System.out.println("()");
	}

	private static List<Entry<String, Long>> countAndSortWords(String text) {
		if (Objects.isNull(text) || text.isEmpty())
			return Collections.emptyList();
		String refinedText = text.replaceAll("[^a-zA-Z0-9\\s]", "");
		Pattern pattern = Pattern.compile("\\s+");
		Map<String, Long> wordFrequencyMap = pattern.splitAsStream(refinedText).filter(token -> !token.trim().isEmpty())
				.collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
		return wordFrequencyMap.entrySet().stream().sorted(Map.Entry.<String, Long>comparingByValue().reversed())
				// or
				/*
				 * .sorted( (entry1, entry2) -> { return
				 * entry1.getValue().compareTo(entry2.getValue()); } )
				 */
				// or
				/*
				 * .sorted( (entry1, entry2) -> entry1.getValue().compareTo(entry2.getValue())
				 */
				.collect(Collectors.toList());
	}
}
