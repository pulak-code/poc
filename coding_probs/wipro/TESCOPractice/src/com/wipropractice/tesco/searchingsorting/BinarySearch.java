package com.wipropractice.tesco.searchingsorting;

public class BinarySearch {
	public static void main(String[] args) {
		int[] arr = { 2, 5, 8, 12, 16, 23, 38, 56, 72, 91 };
		int target = 56;
		int idx = binarySearch(arr, target);
		System.out.println(idx);
	}

	private static int binarySearch(int[] arr, int target) {
		int low = 0;
		int high = arr.length - 1;
		while (low <= high) {
			int mid = low + (high - low) / 2;
			int midValue = arr[mid];
			if (midValue == target)
				return mid;
			else if (midValue < target)
				low = mid + 1;
			else
				high = mid - 1;
		}
		return -1;
	}
}
