// data_processor.rs - Модуль обработки данных на Rust
use std::env;
use std::fs;
use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc, NaiveDateTime};

#[derive(Deserialize, Serialize, Clone, Debug)]
struct TimeBlock {
    id: u32,
    title: String,
    duration: u32,
    created_at: String,
    status: String,
}

#[derive(Serialize)]
struct ProcessedBlock {
    id: u32,
    title: String,
    duration: u32,
    created_at: String,
    status: String,
    efficiency: f64,
    priority_score: f64,
    optimal_time: String,
    processed_at: String,
}

#[derive(Serialize)]
struct ProcessingResult {
    processed_blocks: Vec<ProcessedBlock>,
    total_efficiency: f64,
    optimization_suggestions: Vec<String>,
    performance_metrics: PerformanceMetrics,
    processor: String,
}

#[derive(Serialize)]
struct PerformanceMetrics {
    total_duration: u32,
    average_duration: f64,
    efficiency_distribution: HashMap<String, u32>,
    peak_productivity_hours: Vec<u8>,
    fragmentation_index: f64,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 2 {
        eprintln!("Usage: {} <input_file>", args[0]);
        std::process::exit(1);
    }
    
    let filename = &args[1];
    
    match process_time_blocks(filename) {
        Ok(result) => {
            let json_output = serde_json::to_string_pretty(&result).unwrap();
            println!("{}", json_output);
        }
        Err(e) => {
            eprintln!("Error processing blocks: {}", e);
            std::process::exit(1);
        }
    }
}

fn process_time_blocks(filename: &str) -> Result<ProcessingResult, Box<dyn std::error::Error>> {
    // Читаем входные данные
    let content = fs::read_to_string(filename)?;
    let blocks: Vec<TimeBlock> = serde_json::from_str(&content)?;
    
    if blocks.is_empty() {
        return Ok(ProcessingResult {
            processed_blocks: vec![],
            total_efficiency: 0.0,
            optimization_suggestions: vec!["Добавьте временные блоки для анализа".to_string()],
            performance_metrics: PerformanceMetrics {
                total_duration: 0,
                average_duration: 0.0,
                efficiency_distribution: HashMap::new(),
                peak_productivity_hours: vec![],
                fragmentation_index: 0.0,
            },
            processor: "rust".to_string(),
        });
    }
    
    // Обрабатываем каждый блок
    let mut processed_blocks = Vec::new();
    let mut total_efficiency = 0.0;
    
    for block in &blocks {
        let efficiency = calculate_efficiency(&block);
        let priority_score = calculate_priority_score(&block);
        let optimal_time = suggest_optimal_time(&block);
        
        processed_blocks.push(ProcessedBlock {
            id: block.id,
            title: block.title.clone(),
            duration: block.duration,
            created_at: block.created_at.clone(),
            status: block.status.clone(),
            efficiency,
            priority_score,
            optimal_time,
            processed_at: Utc::now().to_rfc3339(),
        });
        
        total_efficiency += efficiency;
    }
    
    total_efficiency /= blocks.len() as f64;
    
    // Генерируем метрики производительности
    let performance_metrics = generate_performance_metrics(&blocks);
    
    // Генерируем рекомендации по оптимизации
    let optimization_suggestions = generate_optimization_suggestions(&blocks, &performance_metrics);
    
    Ok(ProcessingResult {
        processed_blocks,
        total_efficiency,
        optimization_suggestions,
        performance_metrics,
        processor: "rust".to_string(),
    })
}

fn calculate_efficiency(block: &TimeBlock) -> f64 {
    // Алгоритм расчета эффективности блока
    let base_efficiency = match block.duration {
        0..=30 => 60.0,      // Короткие блоки менее эффективны
        31..=90 => 85.0,     // Оптимальная длительность
        91..=180 => 95.0,    // Хорошая длительность для глубокой работы
        181..=300 => 80.0,   // Длинные блоки могут быть менее эффективны
        _ => 60.0,           // Очень длинные блоки
    };
    
    // Бонус за статус
    let status_multiplier = match block.status.as_str() {
        "completed" => 1.2,
        "active" => 1.0,
        "planned" => 0.8,
        _ => 0.9,
    };
    
    // Учитываем время создания (недавние блоки более актуальны)
    let time_bonus = 1.0; // Упрощенно, в реальности бы парсили дату
    
    (base_efficiency * status_multiplier * time_bonus).min(100.0)
}

fn calculate_priority_score(block: &TimeBlock) -> f64 {
    // Расчет приоритета на основе различных факторов
    let duration_score = (block.duration as f64 / 120.0).min(1.0) * 40.0; // До 40 баллов за длительность
    
    let title_score = if block.title.to_lowercase().contains("важн") || 
                         block.title.to_lowercase().contains("срочн") {
        30.0
    } else if block.title.to_lowercase().contains("встреча") ||
              block.title.to_lowercase().contains("звонок") {
        25.0
    } else {
        20.0
    };
    
    let status_score = match block.status.as_str() {
        "active" => 30.0,
        "planned" => 20.0,
        "completed" => 10.0,
        _ => 15.0,
    };
    
    duration_score + title_score + status_score
}

fn suggest_optimal_time(block: &TimeBlock) -> String {
    // Предлагаем оптимальное время для выполнения задачи
    match block.duration {
        0..=60 => "09:00-10:00 (утренняя концентрация)".to_string(),
        61..=120 => "10:00-12:00 (пик продуктивности)".to_string(),
        121..=180 => "14:00-17:00 (послеобеденная работа)".to_string(),
        _ => "09:00-12:00 (утренний блок)".to_string(),
    }
}

fn generate_performance_metrics(blocks: &[TimeBlock]) -> PerformanceMetrics {
    let total_duration: u32 = blocks.iter().map(|b| b.duration).sum();
    let average_duration = total_duration as f64 / blocks.len() as f64;
    
    // Распределение эффективности
    let mut efficiency_distribution = HashMap::new();
    for block in blocks {
        let efficiency = calculate_efficiency(block);
        let category = match efficiency as u32 {
            0..=60 => "low",
            61..=80 => "medium",
            81..=95 => "high",
            _ => "excellent",
        };
        *efficiency_distribution.entry(category.to_string()).or_insert(0) += 1;
    }
    
    // Пиковые часы продуктивности (упрощенно)
    let peak_productivity_hours = vec![9, 10, 11, 14, 15];
    
    // Индекс фрагментации (много коротких блоков = высокая фрагментация)
    let short_blocks = blocks.iter().filter(|b| b.duration < 60).count();
    let fragmentation_index = (short_blocks as f64 / blocks.len() as f64) * 100.0;
    
    PerformanceMetrics {
        total_duration,
        average_duration,
        efficiency_distribution,
        peak_productivity_hours,
        fragmentation_index,
    }
}

fn generate_optimization_suggestions(blocks: &[TimeBlock], metrics: &PerformanceMetrics) -> Vec<String> {
    let mut suggestions = Vec::new();
    
    // Анализ фрагментации
    if metrics.fragmentation_index > 50.0 {
        suggestions.push("🔄 Слишком много коротких блоков. Попробуйте объединить похожие задачи.".to_string());
    }
    
    // Анализ средней длительности
    if metrics.average_duration < 45.0 {
        suggestions.push("⏰ Увеличьте длительность блоков для лучшей концентрации (рекомендуется 60-90 мин).".to_string());
    } else if metrics.average_duration > 180.0 {
        suggestions.push("✂️ Разбейте длинные блоки на более короткие для лучшего фокуса.".to_string());
    }
    
    // Анализ общего времени
    if metrics.total_duration < 240 {
        suggestions.push("📈 Увеличьте общее время планирования для повышения продуктивности.".to_string());
    }
    
    // Анализ статусов
    let completed_count = blocks.iter().filter(|b| b.status == "completed").count();
    let completion_rate = (completed_count as f64 / blocks.len() as f64) * 100.0;
    
    if completion_rate < 70.0 {
        suggestions.push("✅ Низкий процент выполнения задач. Планируйте более реалистично.".to_string());
    }
    
    // Рекомендации по времени
    suggestions.push("🌅 Планируйте сложные задачи на утренние часы (9:00-12:00).".to_string());
    suggestions.push("🍽️ Используйте послеобеденное время для рутинных задач.".to_string());
    
    if suggestions.is_empty() {
        suggestions.push("🎉 Отличное планирование! Продолжайте в том же духе.".to_string());
    }
    
    suggestions
}

// Добавляем зависимости в Cargo.toml:
/*
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
chrono = { version = "0.4", features = ["serde"] }
*/

// Компиляция:
// cargo build --release
// Исполняемый файл будет в target/release/data_processor.exe
