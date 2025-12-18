import numpy as np
import json
from typing import Dict, List
import time
import matplotlib.pyplot as plt
import sys

# Set recursion limit for Merge Sort just in case
sys.setrecursionlimit(2000)

# --- KONFIGURASI ---
INITIAL_COUNT = 50      # Jumlah angka awal
TOTAL_DAYS = 14         # Durasi simulasi per bulan
TOTAL_MONTHS = 10       # Jumlah bulan (trials)
MIN_VALUE = 1           # Nilai random minimal
MAX_VALUE = 50          # Nilai random maksimal
MIN_GROWTH = 0.01       # Pertumbuhan minimal (1%)
MAX_GROWTH = 0.05       # Pertumbuhan maksimal (5%)
OUTPUT_FILE = 'array_data.json'

def generate_simulation_data(months: int, days: int, start_count: int) -> Dict[str, Dict[str, List[int]]]:
    """
    Menghasilkan data simulasi pertumbuhan array harian selama beberapa bulan.
    Structure: { "bulan_1": { "hari_1": [...], ... }, ... }
    """
    full_data = {}

    for month in range(1, months + 1):
        month_key = f"bulan_{month}"
        month_data = {}
        current_values = None
        
        print(f"\n--- Generating {month_key} ---")

        for day in range(1, days + 1):
            if day == 1:
                current_values = np.random.randint(MIN_VALUE, MAX_VALUE, start_count)
            else:
                # Pertumbuhan acak
                growth_rate = np.random.uniform(MIN_GROWTH, MAX_GROWTH)
                new_total_count = int(len(current_values) * (1 + growth_rate))
                
                # Pastikan selalu ada penambahan minimal jika growth rate sangat kecil tapi > 0
                if new_total_count <= len(current_values):
                     new_total_count = len(current_values) + 1

                num_new_items = new_total_count - len(current_values)
                new_items = np.random.randint(MIN_VALUE, MAX_VALUE, num_new_items)
                current_values = np.concatenate([current_values, new_items])

            day_key = f"hari_{day}"
            month_data[day_key] = current_values.tolist()
            # Optional conversion to list for JSON serialization happening here
            
            # Print info every now and then or for all
            # print(f"  {day_key} (Total item: {len(current_values)})")
        
        full_data[month_key] = month_data

    return full_data

def save_to_json(data: dict, filename: str):
    """
    Menyimpan dictionary ke file JSON.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving file: {e}")
        return False

def print_summary(data: dict, filename: str):
    """
    Menampilkan ringkasan hasil proses.
    """
    print(f"\n--- Ringkasan Data ---")
    print(f"File output : {filename}")
    print(f"Total Bulan : {len(data)}")
    first_month = list(data.keys())[0]
    print(f"Hari per Bulan: {len(data[first_month])}")

# %% Algorithms
def insertion_sort(arr):
    """
    Implementasi Insertion Sort.
    Kompleksitas Waktu: O(n^2)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    """
    Implementasi Merge Sort.
    Kompleksitas Waktu: O(n log n)
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

# %% Benchmark
# ... (Previous code remains the same until benchmark_algorithms)

def benchmark_algorithms(data_file):
    # ... (Same implementation as before)
    try:
        with open(data_file, 'r') as f:
            full_data = json.load(f)
    except FileNotFoundError:
        print(f"File {data_file} tidak ditemukan.")
        return None

    all_results = {}

    print(f"\n--- Memulai Benchmark ({len(full_data)} Bulan) ---")
    
    sorted_months = sorted(full_data.keys(), key=lambda x: int(x.split('_')[1]))

    for month_key in sorted_months:
        month_data = full_data[month_key]
        print(f"Processing {month_key}...")
        
        month_results = {
            'days': [],
            'sizes': [],
            'insertion_times': [],
            'merge_times': []
        }
        
        sorted_days = sorted(month_data.keys(), key=lambda x: int(x.split('_')[1]))
        
        for day_key in sorted_days:
            arr = month_data[day_key]
            size = len(arr)
            
            arr_copy_1 = arr.copy()
            start_time = time.time()
            insertion_sort(arr_copy_1)
            insertion_time = time.time() - start_time
            
            arr_copy_2 = arr.copy()
            start_time = time.time()
            merge_sort(arr_copy_2)
            merge_time = time.time() - start_time
            
            month_results['days'].append(day_key)
            month_results['sizes'].append(size)
            month_results['insertion_times'].append(insertion_time)
            month_results['merge_times'].append(merge_time)
        
        all_results[month_key] = month_results

    return all_results

def plot_individual_benchmarks(all_results):
    """
    Memvisualisasikan hasil benchmark setiap bulan dalam grid 5x2 dan menyimpannya.
    """
    if not all_results:
        return

    # Prepare figure for 5x2 grid
    fig, axes = plt.subplots(5, 2, figsize=(15, 20))
    axes = axes.flatten() 
    
    sorted_months = sorted(all_results.keys(), key=lambda x: int(x.split('_')[1]))
    
    for i, month_key in enumerate(sorted_months):
        if i >= len(axes): break

        ax = axes[i]
        results = all_results[month_key]
        
        ax.plot(results['sizes'], results['insertion_times'], label='Insertion Sort', marker='o', linestyle='-', markersize=4)
        ax.plot(results['sizes'], results['merge_times'], label='Merge Sort', marker='s', linestyle='-', markersize=4)
        
        ax.set_title(f'Benchmark: {month_key.replace("_", " ").title()}')
        ax.set_xlabel('Ukuran Array')
        ax.set_ylabel('Waktu (s)')
        ax.legend()
        ax.grid(True, linestyle= '--', alpha=0.5)

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle('Perbandingan Algoritma Sorting per Bulan (1-10)', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.97]) 
    
    output_path = os.path.join('results', 'benchmark_individual.png')
    plt.savefig(output_path)
    print(f"\nGrafik individual disimpan ke: {output_path}")
    plt.show()

def plot_average_benchmark(all_results):
    """
    Menghitung rata-rata dari semua bulan dan memvisualisasikannya dalam satu grafik.
    """
    if not all_results:
        return

    # Aggregate data
    agg_results = {i: {'sizes': [], 'insertion': [], 'merge': []} for i in range(1, TOTAL_DAYS + 1)}

    for month_key, results in all_results.items():
        for idx, day_key in enumerate(results['days']):
            # Asumsi urutan data konsisten
            day_num = int(day_key.split('_')[1])
            agg_results[day_num]['sizes'].append(results['sizes'][idx])
            agg_results[day_num]['insertion'].append(results['insertion_times'][idx])
            agg_results[day_num]['merge'].append(results['merge_times'][idx])

    avg_sizes = []
    avg_insertion = []
    avg_merge = []

    for day_num in range(1, TOTAL_DAYS + 1):
        data = agg_results[day_num]
        avg_sizes.append(sum(data['sizes']) / len(data['sizes']))
        avg_insertion.append(sum(data['insertion']) / len(data['insertion']))
        avg_merge.append(sum(data['merge']) / len(data['merge']))

    plt.figure(figsize=(10, 6))
    plt.plot(avg_sizes, avg_insertion, label='Avg Insertion Sort', marker='o', linestyle='-')
    plt.plot(avg_sizes, avg_merge, label='Avg Merge Sort', marker='s', linestyle='-')
    
    plt.title(f'Rata-rata Perbandingan Algoritma Sorting ({TOTAL_MONTHS} Bulan)')
    plt.xlabel('Rata-rata Ukuran Array')
    plt.ylabel('Rata-rata Waktu Eksekusi (detik)')
    plt.legend()
    plt.grid(True, linestyle= '--', alpha=0.7)
    plt.tight_layout()
    
    output_path = os.path.join('results', 'benchmark_average.png')
    plt.savefig(output_path)
    print(f"Grafik rata-rata disimpan ke: {output_path}")
    plt.show()

import os

if __name__ == "__main__":
    # Create results directory if not exists
    if not os.path.exists('results'):
        os.makedirs('results')

    # Generate Data
    simulation_data = generate_simulation_data(TOTAL_MONTHS, TOTAL_DAYS, INITIAL_COUNT)
    
    success = save_to_json(simulation_data, OUTPUT_FILE)
    if success:
        print_summary(simulation_data, OUTPUT_FILE)
        
        # Benchmark
        benchmark_results = benchmark_algorithms(OUTPUT_FILE)
        
        # Plot
        plot_individual_benchmarks(benchmark_results)
        plot_average_benchmark(benchmark_results)
