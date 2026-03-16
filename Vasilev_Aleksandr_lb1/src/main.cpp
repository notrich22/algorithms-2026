#include <algorithm>
#include <iostream>
#include <vector>

#define INDEX(x, y, n) ((y) * (n) + (x))

#define DEBUG 0

#if DEBUG
    #define LOG(depth, msg) do { \
        for(int _i = 0; _i < (depth); ++_i) std::cout << "  "; \
        std::cout << msg << "\n"; \
    } while(0)
#else
    #define LOG(depth, msg)
#endif

struct Square {
    int x, y, w;
};

struct Frame {
    int x, y;
    int nextSize;
    int scanStartY;
    Square enteredBy;
    bool hasEnteredBy;
};

int N;
std::vector<unsigned char> field;
std::vector<Square> currentSolution;
std::vector<Square> bestSolution;
std::vector<Frame> stackFrames;

int currentCount = 0;
int bestCount = 0;
int remainingArea = 0;

bool canPlace(int x, int y, int w) {
    if (x + w > N || y + w > N) {
        return false;
    }

    for (int yi = y; yi < y + w; yi++) {
        for (int xi = x; xi < x + w; xi++) {
            if (field[INDEX(xi, yi, N)]) {
                return false;
            }
        }
    }
    return true;
}

void placeSquare(const Square& sq) {
    for (int yi = sq.y; yi < sq.y + sq.w; yi++) {
        for (int xi = sq.x; xi < sq.x + sq.w; xi++) {
            field[INDEX(xi, yi, N)] = 1;
        }
    }

    currentCount++;
    remainingArea -= sq.w * sq.w;
    currentSolution.push_back(sq);
}

void removeSquare(const Square& sq) {
    for (int yi = sq.y; yi < sq.y + sq.w; yi++) {
        for (int xi = sq.x; xi < sq.x + sq.w; xi++) {
            field[INDEX(xi, yi, N)] = 0;
        }
    }

    currentCount--;
    remainingArea += sq.w * sq.w;
    currentSolution.pop_back();
}

bool findFirstFreeCell(int startY, int& outX, int& outY) {
    for (int y = startY; y < N; y++) {
        for (int x = 0; x < N; x++) {
            if (!field[INDEX(x, y, N)]) {
                outX = x;
                outY = y;
                return true;
            }
        }
    }
    outX = -1;
    outY = -1;
    return false;
}

Frame buildFrame(bool hasEnteredBy, Square enteredBy, int scanStartY) {
    int x, y;
    bool found = findFirstFreeCell(scanStartY, x, y);

    if (!found) {
        return {-1, -1, 0, scanStartY, enteredBy, hasEnteredBy};
    }

    int maxSize = std::min(N - x, N - y);

    return {x, y, maxSize, y, enteredBy, hasEnteredBy};
}

Frame buildRootFrame() {
    Square dummy{0, 0, 0};
    return {0, 0, N - 1, 0, dummy, false};
}

void buildGreedyUpperBound() {
    LOG(0, "Жадный старт");
    field.assign(N * N, 0);
    currentSolution.clear();
    currentCount = 0;
    remainingArea = N * N;

    while (remainingArea > 0) {
        int x, y;
        findFirstFreeCell(0, x, y);

        int maxSize = std::min(N - x, N - y);

        if (x == 0 && y == 0 && maxSize == N) {
            maxSize = N - 1;
        }

        for (int w = maxSize; w >= 1; w--) {
            if (canPlace(x, y, w)) {
                placeSquare({x, y, w});
                LOG(1, "Cтавим " << w << "x" << w << " в (" << x + 1 << ", " << y + 1 << ")");
                break;
            }
        }
    }

    bestCount = currentCount;
    bestSolution = currentSolution;
    LOG(0, "Жадная оценка: " << bestCount << " квадратов \n");

    while (!currentSolution.empty()) {
        Square sq = currentSolution.back();
        removeSquare(sq);
    }
}

void solve() {
    field.assign(N * N, 0);
    currentSolution.clear();
    bestSolution.clear();
    stackFrames.clear();
    currentCount = 0;
    remainingArea = N * N;

    bestCount = N * N;

    buildGreedyUpperBound();

    LOG(0, "Запуск для N = " << N);
    Frame root = buildRootFrame();
    stackFrames.push_back(root);

    while (!stackFrames.empty()) {
        Frame& frame = stackFrames.back();

        if (frame.nextSize < 1) {
            Square entered = frame.enteredBy;
            bool hasEntered = frame.hasEnteredBy;
            stackFrames.pop_back();

            if (hasEntered) {
                removeSquare(entered);
                LOG(currentCount, "Откат: убираем " << entered.w << "x" << entered.w 
                    << " из (" << entered.x + 1 << ", " << entered.y + 1 << ")");
            }
            continue;
        }

        int w = frame.nextSize;
        frame.nextSize--;

        if (frame.x == 0 && frame.y == 0 && !frame.hasEnteredBy && w < (N + 1) / 2) {
            LOG(currentCount, "Пропуск: " << w << "x" << w << " в корневом кадре слишком мал");
            frame.nextSize = 0;
            continue;
        }

        if (!canPlace(frame.x, frame.y, w)) {
            continue;
        }

        Square sq{frame.x, frame.y, w};
        LOG(currentCount, "Пробуем поставить " << w << "x" << w << " в (" << frame.x + 1 << ", " << frame.y + 1 << ")");
        placeSquare(sq);

        if (currentCount >= bestCount) {
            LOG(currentCount, "Отсечение: количество квадратов превышает или равно лучшему (" << bestCount << ")");
            removeSquare(sq);
            LOG(currentCount, "Откат: убираем " << sq.w << "x" << sq.w << " из (" << sq.x + 1 << ", " << sq.y + 1 << ")");
            continue;
        }

        // если уже bestCount - 1 квадратов и поле не заполнено,
        // то ещё один квадрат не даст улучшения
        if (currentCount >= bestCount - 1 && remainingArea > 0) {
            LOG(currentCount, "Отсечение: улучшение невозможно");
            removeSquare(sq);
            LOG(currentCount, "Откат: убираем " << sq.w << "x" << sq.w << " из (" << sq.x + 1 << ", " << sq.y + 1 << ")");
            continue;
        }

        if (remainingArea == 0) {
            bestCount = currentCount;
            bestSolution = currentSolution;
            LOG(currentCount, "Новое лучшее решение: " << bestCount << " квадратов");
            removeSquare(sq);
            continue;
        }

        Frame child = buildFrame(true, sq, frame.y);
        stackFrames.push_back(child);
    }
    LOG(0, "Поиск завершен");
}

// решение для четных N
bool solveEvenCase() {
    if (N % 2 != 0) {
        return false;
    }
    
    LOG(0, "Чётный N, берём 4 квадрата");
    int half = N / 2;

    std::cout << 4 << "\n";
    std::cout << 1 << " " << 1 << " " << half << "\n";
    std::cout << 1 + half << " " << 1 << " " << half << "\n";
    std::cout << 1 << " " << 1 + half << " " << half << "\n";
    std::cout << 1 + half << " " << 1 + half << " " << half << "\n";

    return true;
}

int main() {
    std::cin >> N;

    if (solveEvenCase()) {
        return 0;
    }

    solve();

    std::cout << bestCount << "\n";
    for (const auto& sq : bestSolution) {
        std::cout << sq.x + 1 << " " << sq.y + 1 << " " << sq.w << "\n";
    }

    return 0;
}