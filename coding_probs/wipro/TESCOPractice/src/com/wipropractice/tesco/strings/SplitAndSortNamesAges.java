package com.wipropractice.tesco.strings;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import com.wipropractice.tesco.strings.util.MyPair;

public class SplitAndSortNamesAges {
	public static void main(String[] args) {
		String input = "PV-29#Pulak-29#Charlie-66#Pablo-39";
		List<MyPair<String, Integer>> pairlist = splitAndSortNameAge(input);
		if (!pairlist.isEmpty()) {
			System.out.println(pairlist);
		} else
			System.out.println("");
	}

	private static List<MyPair<String, Integer>> splitAndSortNameAge(String input) {
		List<MyPair<String, Integer>> pairlist = new ArrayList<>();
		String[] pairs = input.split("#");
		for (String MyPair : pairs) {
			String[] parts = MyPair.split("-");
			if (parts.length == 2)
				pairlist.add(new MyPair<>(parts[0], Integer.parseInt(parts[1])));
		}
		Collections.sort(pairlist, (p1, p2) -> {
			int valueComparison = Integer.compare(p1.getValue(), p2.getValue());
			if (valueComparison == 0)
				return p1.getKey().toLowerCase().compareTo(p2.getKey().toLowerCase());
			return valueComparison;
		});
		return pairlist;
	}
}