# build_modules.py - Скрипт для компиляции модулей на разных языках
import os
import subprocess
import sys
import platform

def print_status(message, status="INFO"):
    """Печать статуса с цветами"""
    colors = {
        "INFO": "\033[94m",  # Синий
        "SUCCESS": "\033[92m",  # Зеленый
        "WARNING": "\033[93m",  # Желтый
        "ERROR": "\033[91m",  # Красный
        "RESET": "\033[0m"  # Сброс
    }
    
    color = colors.get(status, colors["INFO"])
    reset = colors["RESET"]
    
    print(f"{color}[{status}] {message}{reset}")

def check_dependencies():
    """Проверка наличия необходимых инструментов"""
    print_status("Проверка зависимостей...")
    
    dependencies = {
        "gcc": ["gcc", "--version"],
        "g++": ["g++", "--version"], 
        "cargo": ["cargo", "--version"],
        "rustc": ["rustc", "--version"]
    }
    
    available = {}
    
    for tool, command in dependencies.items():
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                available[tool] = True
                version = result.stdout.split('\n')[0]
                print_status(f"{tool}: {version}", "SUCCESS")
            else:
                available[tool] = False
                print_status(f"{tool}: не найден", "WARNING")
        except FileNotFoundError:
            available[tool] = False
            print_status(f"{tool}: не установлен", "WARNING")
    
    return available

def build_cpp_module():
    """Компиляция C++ модуля"""
    print_status("Компиляция C++ модуля производительности...")
    
    system = platform.system()
    
    if system == "Windows":
        lib_name = "performance.dll"
        compile_cmd = [
            "g++", "-shared", "-fPIC", "-O3", 
            "performance.cpp", "-o", lib_name
        ]
    else:
        lib_name = "performance.so"
        compile_cmd = [
            "g++", "-shared", "-fPIC", "-O3", 
            "performance.cpp", "-o", lib_name
        ]
    
    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status(f"C++ модуль скомпилирован: {lib_name}", "SUCCESS")
            return True
        else:
            print_status(f"Ошибка компиляции C++: {result.stderr}", "ERROR")
            return False
            
    except FileNotFoundError:
        print_status("g++ не найден. Установите GCC/MinGW", "ERROR")
        return False

def build_rust_module():
    """Компиляция Rust модуля"""
    print_status("Компиляция Rust модуля обработки данных...")
    
    try:
        # Компиляция в release режиме для максимальной производительности
        result = subprocess.run(
            ["cargo", "build", "--release"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Копируем исполняемый файл в корневую директорию
            system = platform.system()
            if system == "Windows":
                src = "target/release/data_processor.exe"
                dst = "data_processor.exe"
            else:
                src = "target/release/data_processor"
                dst = "data_processor"
            
            if os.path.exists(src):
                import shutil
                shutil.copy2(src, dst)
                print_status(f"Rust модуль скомпилирован: {dst}", "SUCCESS")
                return True
            else:
                print_status("Исполняемый файл Rust не найден", "ERROR")
                return False
        else:
            print_status(f"Ошибка компиляции Rust: {result.stderr}", "ERROR")
            return False
            
    except FileNotFoundError:
        print_status("Cargo не найден. Установите Rust", "ERROR")
        return False

def create_fallback_modules():
    """Создание заглушек для отсутствующих модулей"""
    print_status("Создание заглушек для недоступных модулей...")
    
    # Создаем пустой файл для C++ модуля, если он не скомпилирован
    cpp_files = ["performance.dll", "performance.so"]
    cpp_exists = any(os.path.exists(f) for f in cpp_files)
    
    if not cpp_exists:
        print_status("C++ модуль недоступен - будет использован Python fallback", "WARNING")
    
    # Проверяем Rust модуль
    rust_files = ["data_processor.exe", "data_processor"]
    rust_exists = any(os.path.exists(f) for f in rust_files)
    
    if not rust_exists:
        print_status("Rust модуль недоступен - будет использован Python fallback", "WARNING")

def test_modules():
    """Тестирование скомпилированных модулей"""
    print_status("Тестирование модулей...")
    
    # Тест C++ модуля
    cpp_files = ["performance.dll", "performance.so"]
    cpp_exists = any(os.path.exists(f) for f in cpp_files)
    
    if cpp_exists:
        try:
            import ctypes
            for cpp_file in cpp_files:
                if os.path.exists(cpp_file):
                    lib = ctypes.CDLL(f"./{cpp_file}")
                    lib.calculate_productivity.argtypes = [ctypes.c_int, ctypes.c_int]
                    lib.calculate_productivity.restype = ctypes.c_double
                    
                    # Тестовый вызов
                    result = lib.calculate_productivity(5, 300)
                    print_status(f"C++ модуль работает: тест вернул {result}", "SUCCESS")
                    break
        except Exception as e:
            print_status(f"Ошибка тестирования C++ модуля: {e}", "ERROR")
    
    # Тест Rust модуля
    rust_files = ["data_processor.exe", "data_processor"]
    rust_exists = any(os.path.exists(f) for f in rust_files)
    
    if rust_exists:
        try:
            # Создаем тестовый файл
            test_data = [
                {"id": 1, "title": "Test", "duration": 60, "created_at": "2025-01-01T10:00:00Z", "status": "active"}
            ]
            
            import json
            with open("test_data.json", "w") as f:
                json.dump(test_data, f)
            
            # Тестируем Rust модуль
            for rust_file in rust_files:
                if os.path.exists(rust_file):
                    result = subprocess.run(
                        [f"./{rust_file}", "test_data.json"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        print_status("Rust модуль работает корректно", "SUCCESS")
                    else:
                        print_status(f"Ошибка Rust модуля: {result.stderr}", "ERROR")
                    
                    # Удаляем тестовый файл
                    if os.path.exists("test_data.json"):
                        os.remove("test_data.json")
                    break
                    
        except Exception as e:
            print_status(f"Ошибка тестирования Rust модуля: {e}", "ERROR")

def main():
    """Главная функция сборки"""
    print_status("Сборка гибридного приложения Time Blocking Planner")
    print_status("=" * 60)
    
    # Проверяем зависимости
    deps = check_dependencies()
    
    print_status("-" * 60)
    
    # Компилируем модули
    cpp_success = False
    rust_success = False
    
    if deps.get("g++", False):
        cpp_success = build_cpp_module()
    else:
        print_status("Пропускаем C++ модуль (g++ не найден)", "WARNING")
    
    if deps.get("cargo", False):
        rust_success = build_rust_module()
    else:
        print_status("Пропускаем Rust модуль (cargo не найден)", "WARNING")
    
    # Создаем заглушки
    create_fallback_modules()
    
    print_status("-" * 60)
    
    # Тестируем модули
    test_modules()
    
    print_status("-" * 60)
    
    # Итоговый отчет
    print_status("Результаты сборки:")
    print_status(f"   C++ модуль: {'Готов' if cpp_success else 'Fallback'}")
    print_status(f"   Rust модуль: {'Готов' if rust_success else 'Fallback'}")
    print_status(f"   JavaScript: Встроен в приложение")
    print_status(f"   Python: Основа приложения")
    
    if cpp_success or rust_success:
        print_status("Гибридное приложение готово к запуску!", "SUCCESS")
    else:
        print_status("Приложение будет работать в режиме Python fallback", "WARNING")
    
    print_status("\nДля запуска используйте: python hybrid_app.py")

if __name__ == "__main__":
    main()
