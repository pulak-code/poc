package com.wipropractice.tesco.strings;

import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

import com.wipropractice.tesco.strings.util.MyPair;

public class SplitAndSortNamesAgesLambdaStream {
	public static void main(String[] args) {
		String input = "PV-29#Pulak-29#Charlie-66#Pablo-39";
		List<MyPair<String, Integer>> pairlist = splitAndSortNameAge(input);
		if (!pairlist.isEmpty()) {
			System.out.println(pairlist);
		} else
			System.out.println("");
	}

	private static List<MyPair<String, Integer>> splitAndSortNameAge(String input) {
		if (Objects.isNull(input) || input.isEmpty()) {
			return Collections.emptyList();
		}

		Comparator<? super MyPair<String, Integer>> ageThenNameComparator = Comparator
				.<MyPair<String, Integer>, Integer>comparing(MyPair::getValue)
				.thenComparing(pair -> pair.getKey().toLowerCase());
		return Arrays.stream(input.split("#")).filter(pairString -> pairString.split("-").length == 2)
				.map(pairString -> {
					String[] parts = pairString.split("-");
					String name = parts[0];
					int age = Integer.parseInt(parts[1]);
					return new MyPair<>(name, age);
				}).sorted(ageThenNameComparator).toList();
	}
}
