#include <iostream>
#include <vector>
#include <fstream>

enum Direction { up, down, right, left };

class Position2a {
	// positions range from 0 to 2
	int x_pos = 1;
	int y_pos = 1;
	char nrs[3][3] = {{'1','2','3'}, {'4','5','6'}, {'7','8','9'}};
public:
	void move(Direction dir) {
		if (dir == Direction::up) {
			if (y_pos != 0) {
				y_pos -= 1;
			}
		} else if (dir == Direction::down) {
			if (y_pos != 2) {
				y_pos += 1;
			}
		} else if (dir == Direction::right) {
			if (x_pos != 2) {
				x_pos += 1;
			}
		} else if (dir == Direction::left) {
			if (x_pos != 0) {
				x_pos -= 1;
			}
		}
	}
	int get_nr() {
		return nrs[y_pos][x_pos];
	}
};

class Position2b {
	// positions range from 0 to 2
	int x_pos = 0;
	int y_pos = 2;
	char nrs[5][5] = {
		{' ',' ','1', ' ', ' '},
		{' ','2','3', '4', ' '},
		{'5','6','7', '8', '9'},
		{' ','A','B', 'C', ' '},
		{' ',' ','D', ' ', ' '},
	};
public:
	void move(Direction dir) {
		if (dir == Direction::up) {
			if (x_pos == 1 || x_pos == 3) {
				if (y_pos != 1) {
					y_pos -= 1;
				}
			} else if (x_pos == 2) {
				if (y_pos != 0) {
					y_pos -= 1;
				}
			}
		} else if (dir == Direction::down) {
			if (x_pos == 1 || x_pos == 3) {
				if (y_pos != 3) {
					y_pos += 1;
				}
			} else if (x_pos == 2) {
				if (y_pos != 4) {
					y_pos += 1;
				}
			}
		} else if (dir == Direction::right) {
			if (y_pos == 1 || y_pos == 3) {
				if (x_pos != 3) {
					x_pos += 1;
				}
			} else if (y_pos == 2) {
				if (x_pos != 4) {
					x_pos += 1;
				}
			}
		} else if (dir == Direction::left) {
			if (y_pos == 1 || y_pos == 3) {
				if (x_pos != 1) {
					x_pos -= 1;
				}
			} else if (y_pos == 2) {
				if (x_pos != 0) {
					x_pos -= 1;
				}
			}
		}
	}
	int get_nr() {
		return nrs[y_pos][x_pos];
	}
};

std::string day2a() {
	Position2a pos;
	std::string answer = "";

	std::ifstream input_file ("inputs/2");
	if (input_file.is_open()) {
		std::string line;
		while (getline(input_file, line)) {
			for (int i = 0; i < line.size(); i++) {
				if (line[i] == 'U') {
					pos.move(Direction::up);
				} else if (line[i] == 'D') {
					pos.move(Direction::down);
				} else if (line[i] == 'L') {
					pos.move(Direction::left);
				} else if (line[i] == 'R') {
					pos.move(Direction::right);
				} else {
					std::cout<<"read unexpected char: "<<line[i]<<std::endl;
					exit(-1);
				}
			}
			answer.push_back(pos.get_nr());
		}
	} else {
		std::cout<<"could not open file 'inputs/2'"<<std::endl;
		exit(-1);
	}
	return answer;
}

std::string day2b() {
	Position2b pos;
	std::string answer = "";

	std::ifstream input_file ("inputs/2");
	if (input_file.is_open()) {
		std::string line;
		while (getline(input_file, line)) {
			for (int i = 0; i < line.size(); i++) {
				if (line[i] == 'U') {
					pos.move(Direction::up);
				} else if (line[i] == 'D') {
					pos.move(Direction::down);
				} else if (line[i] == 'L') {
					pos.move(Direction::left);
				} else if (line[i] == 'R') {
					pos.move(Direction::right);
				} else {
					std::cout<<"read unexpected char: "<<line[i]<<std::endl;
					exit(-1);
				}
			}
			answer.push_back(pos.get_nr());
		}
	} else {
		std::cout<<"could not open file 'inputs/2'"<<std::endl;
		exit(-1);
	}
	return answer;
}
