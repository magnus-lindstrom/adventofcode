#include <vector>
#include <sstream>
#include <string>

template <typename Out>
void split2(const std::string &s, char delim, Out result) {
	std::istringstream iss(s);
	std::string item;
	while (std::getline(iss, item, delim)) {
		if (!item.empty()) {
			*result++ = item;
		}
	}
}

std::vector<std::string> split(const std::string &s, char delim) {
	std::vector<std::string> elems;
	split2(s, delim, std::back_inserter(elems));
	return elems;
}
