#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdexcept>
#include <typeinfo>
#include <map>

using namespace std;

struct Move {
	bool right_turn;
	int steps;
};

class Position {
	map<array<int, 2>, bool> visited_positions = {};
	array<int, 2> revisited_pos_sentinel_value = {1000, 1000}; // should not get to this point, safe sentinel
	array<int, 2> revisited_position = revisited_pos_sentinel_value;
	array<int, 2> heading = {0, 1};
	array<int, 2> position = {0, 0};
public:

	void make_move(Move move) {
		if (move.right_turn == true) {
			if (heading[0] != 0) {
				heading[1] = -1 * heading[0];
				heading[0] = 0;
			} else {
				heading[0] = heading[1];
				heading[1] = 0;
			}
		} else {
			if (heading[1] != 0) {
				heading[0] = -1 * heading[1];
				heading[1] = 0;
			} else {
				heading[1] = heading[0];
				heading[0] = 0;
			}
		}

		for (int i = 0; i < move.steps; i++) {
			position[0] += heading[0];
			position[1] += heading[1];
			if (visited_positions.find(position) != visited_positions.end()) {
				if (revisited_position == revisited_pos_sentinel_value) { // has not revisited any
																		  // position yet
					revisited_position = position;
				}
			} else {
				visited_positions[position] = true;
			}
		}

	}
	bool has_revisited_a_position() {
		return revisited_position != revisited_pos_sentinel_value;
	}
	int revisited_pos_dist() {
		return abs(revisited_position[0]) + abs(revisited_position[1]);
	}
	int dist() {
		return abs(position[0]) + abs(position[1]);
	}
	void print() {
		cout<<"pos: ("<<position[0]<<", "<<position[1]<<"), heading: ("<<heading[0]<<", "<<heading[1]<<")."<<endl;
	}
};

std::vector<Move> get_moves() {
	static std::vector<Move> moves;

	std::string line;
	std::ifstream input_file ("inputs/1");
	if (input_file.is_open()) {
		while (getline(input_file, line)) {
			int i = 0;
			while (i < line.size()) {
				static Move move;
				char direction = line[i];
				if (direction == 'R') {
					move.right_turn = true;
				} else if (direction == 'L') {
					move.right_turn = false;
				} else {
					string msg = "expected 'R' or 'L', found ";
					msg.push_back(direction);
					throw std::runtime_error(msg);
				}
				i++;

				int start_of_nr = i;
				int end_of_nr = 0;
				for (int j = start_of_nr; j < line.size(); j++) {
					if (line[j] == ',') {
						end_of_nr = j - 1;
						break;
					}
				}
				if (end_of_nr == 0) { // when reading the final direction, a ',' will not be found
					end_of_nr = line.size();
				}
				i = end_of_nr;
				int steps_string_length = end_of_nr - start_of_nr + 1;
				string steps_string = line.substr(start_of_nr, steps_string_length);
				int steps = stoi(steps_string);
				move.steps = steps;

				moves.push_back(move);

				i = i + 3; // assumes that i is at the position of the last digit in the number
			}
		}
	}
	return moves;
}

int day1a() {
	Position pos;
	std::vector<Move> moves = get_moves();
	// pos.print();
	for (Move move : moves) {
		// cout<<"Making move "<<move.right_turn<<", "<<move.steps<<endl;
		pos.make_move(move);
		// pos.print();
	}
	return pos.dist();
}

int day1b() {
	Position pos;
	std::vector<Move> moves = get_moves();
	for (Move move : moves) {
		pos.make_move(move);
		if (pos.has_revisited_a_position()) {
			return pos.revisited_pos_dist();
		}
	}
	cout<<"did not revisit old spot."<<endl;
	return -1;
}
