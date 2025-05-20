package com.wipropractice.tesco.strings;

import java.util.Objects;

public class NinetyDegRotationMatrix {
	public static void main(String[] args) {
		int[][] matrix = { { 5, 1, 9, 11 }, { 2, 4, 8, 10 }, { 13, 3, 6, 7 }, { 15, 14, 12, 16 } };
		int n = matrix.length;
		int[][] rotated = rotateMatrix(matrix, n);
		printMatrix(rotated);
	}

	private static int[][] rotateMatrix(int[][] matrix, int n) {
		if (matrix == null || matrix.length == 0 || matrix.length != matrix[0].length)
			return new int[0][0];
		int[][] transposed = transposeMatrix(matrix, n);
		return reverseEachRow(transposed, n);
	}

	private static void printMatrix(int[][] matrix) {
		if (Objects.isNull(matrix))
			return;
		for (int i = 0; i < matrix.length; i++) {
			for (int j = 0; j < matrix[0].length; j++) {
				System.out.print(matrix[i][j] + " ");
			}
			System.out.println();
		}
	}

	private static int[][] transposeMatrix(int[][] matrix, int n) {
		for (int i = 0; i < n; i++) {
			for (int j = i; j < n; j++) {
				swap(matrix, i, j);
			}
		}
		return matrix;
	}

	private static int[][] reverseEachRow(int[][] matrix, int n) {
		for (int i = 0; i < n; i++) {
			int left = 0;
			int right = n - 1;
			while (left < right) {
				swap(matrix, i, left, right);
				left++;
				right--;
			}
		}
		return matrix;
	}

	private static void swap(int[][] arr, int i, int left, int right) {
		int temp = arr[i][left];
		arr[i][left] = arr[i][right];
		arr[i][right] = temp;
	}

	private static void swap(int[][] arr, int i, int j) {
		int temp = arr[i][j];
		arr[i][j] = arr[j][i];
		arr[j][i] = temp;
	}
}
