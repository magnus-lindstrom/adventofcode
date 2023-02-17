#include <iostream>
#include <vector>
#include <fstream>
#include "utils.h"

std::string input_file_name = "inputs/3";

std::vector<std::vector<int>> get_input_a() {
	std::vector<std::vector<int>> triangles;
	std::ifstream input_file (input_file_name);
	if (input_file.is_open()) {
		std::string line;
		while (getline(input_file, line)) {
			std::vector<int> triangle;
			std::vector<std::string> nr_vector = split(line, ' ');
			for (std::string str: nr_vector) {
				triangle.push_back(std::stoi(str));
				// std::cout<<std::stoi(str)<<std::endl;
			}
			triangles.push_back(triangle);
		}
	} else {
		std::cout<<"could not open file '"<<input_file_name<<"'."<<std::endl;
		exit(-1);
	}
	return triangles;
}

std::vector<std::vector<int>> get_input_b() {
	std::vector<std::vector<int>> triangles;
	std::ifstream input_file (input_file_name);
	if (input_file.is_open()) {
		std::string line;
		std::vector<int> triangle1;
		std::vector<int> triangle2;
		std::vector<int> triangle3;
		while (getline(input_file, line)) {
			std::vector<std::string> nr_vector = split(line, ' ');
			triangle1.push_back(stoi(nr_vector[0]));
			triangle2.push_back(stoi(nr_vector[1]));
			triangle3.push_back(stoi(nr_vector[2]));

			if (triangle1.size() == 2) {
				triangles.push_back(triangle1);
				triangles.push_back(triangle2);
				triangles.push_back(triangle3);
				triangle1.clear();
				triangle2.clear();
				triangle3.clear();
			}
		}
	} else {
		std::cout<<"could not open file '"<<input_file_name<<"'."<<std::endl;
		exit(-1);
	}
	for (int i = 0; i < triangles.size(); i++) {
		for (int j = 0; j < 3; j++) {
			std::cout<<triangles[i][j]<<" ";
		}
	}
	std::cout<<std::endl;
	return triangles;
}

int day3a() {
	int nr_possible_triangles = 0;
	std::vector<std::vector<int>> triangles = get_input_a();
	for (std::vector<int> triangle: triangles) {
		if (
			triangle[0] + triangle[1] > triangle[2] &&
			triangle[0] + triangle[2] > triangle[1] &&
			triangle[1] + triangle[2] > triangle[0]
		) {
			nr_possible_triangles += 1;
		}
	}
	return nr_possible_triangles;
}

int day3b() {
	int nr_possible_triangles = 0;
	std::vector<std::vector<int>> triangles = get_input_b();
	for (std::vector<int> triangle: triangles) {
		if (
			triangle[0] + triangle[1] > triangle[2] &&
			triangle[0] + triangle[2] > triangle[1] &&
			triangle[1] + triangle[2] > triangle[0]
		) {
			nr_possible_triangles += 1;
		}
	}
	return nr_possible_triangles;
}
