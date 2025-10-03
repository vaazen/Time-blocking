// performance.cpp - Модуль производительности на C++
#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>

extern "C" {
    // Функция расчета продуктивности
    double calculate_productivity(int total_blocks, int total_minutes) {
        if (total_blocks == 0) return 0.0;
        
        // Базовый расчет продуктивности
        double base_productivity = (static_cast<double>(total_minutes) / 480.0) * 100.0;
        
        // Бонус за количество блоков (лучшее планирование)
        double block_bonus = std::min(20.0, total_blocks * 2.0);
        
        // Итоговая продуктивность
        double result = std::min(100.0, base_productivity + block_bonus);
        
        return result;
    }
    
    // Функция оптимизации расписания
    int optimize_schedule(int* durations, int count, int max_time) {
        if (count == 0 || max_time <= 0) return 0;
        
        std::vector<int> blocks(durations, durations + count);
        std::vector<bool> selected(count, false);
        
        int total_time = 0;
        int selected_count = 0;
        
        // Жадный алгоритм: выбираем блоки по убыванию эффективности
        for (int i = 0; i < count; ++i) {
            int best_idx = -1;
            double best_efficiency = -1.0;
            
            for (int j = 0; j < count; ++j) {
                if (!selected[j] && total_time + blocks[j] <= max_time) {
                    double efficiency = static_cast<double>(blocks[j]) / (blocks[j] + 10); // +10 для overhead
                    if (efficiency > best_efficiency) {
                        best_efficiency = efficiency;
                        best_idx = j;
                    }
                }
            }
            
            if (best_idx == -1) break;
            
            selected[best_idx] = true;
            total_time += blocks[best_idx];
            selected_count++;
        }
        
        return selected_count;
    }
    
    // Функция анализа паттернов работы
    double analyze_work_patterns(int* start_times, int* durations, int count) {
        if (count < 2) return 50.0; // Базовая оценка
        
        double consistency_score = 0.0;
        double focus_score = 0.0;
        
        // Анализ консистентности (регулярность начала работы)
        std::vector<int> starts(start_times, start_times + count);
        double avg_start = 0.0;
        for (int start : starts) {
            avg_start += start;
        }
        avg_start /= count;
        
        double variance = 0.0;
        for (int start : starts) {
            variance += (start - avg_start) * (start - avg_start);
        }
        variance /= count;
        
        consistency_score = std::max(0.0, 100.0 - std::sqrt(variance) / 10.0);
        
        // Анализ фокуса (предпочтение длинных блоков)
        std::vector<int> durs(durations, durations + count);
        double avg_duration = 0.0;
        for (int dur : durs) {
            avg_duration += dur;
        }
        avg_duration /= count;
        
        focus_score = std::min(100.0, avg_duration / 2.0); // 2 часа = 100%
        
        return (consistency_score + focus_score) / 2.0;
    }
    
    // Быстрая сортировка для оптимизации
    void quick_sort_blocks(int* arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quick_sort_blocks(arr, low, pi - 1);
            quick_sort_blocks(arr, pi + 1, high);
        }
    }
    
    int partition(int* arr, int low, int high) {
        int pivot = arr[high];
        int i = (low - 1);
        
        for (int j = low; j <= high - 1; j++) {
            if (arr[j] < pivot) {
                i++;
                std::swap(arr[i], arr[j]);
            }
        }
        std::swap(arr[i + 1], arr[high]);
        return (i + 1);
    }
    
    // Функция бенчмарка производительности
    double performance_benchmark() {
        auto start = std::chrono::high_resolution_clock::now();
        
        // Выполняем вычислительно интенсивную задачу
        volatile double result = 0.0;
        for (int i = 0; i < 1000000; ++i) {
            result += std::sin(i) * std::cos(i);
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        return static_cast<double>(duration.count()) / 1000.0; // возвращаем в миллисекундах
    }
}

// Компиляция:
// g++ -shared -fPIC -O3 performance.cpp -o performance.dll (Windows)
// g++ -shared -fPIC -O3 performance.cpp -o performance.so (Linux)
