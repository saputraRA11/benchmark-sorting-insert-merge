from flask import Flask, render_template, jsonify, request
import numpy as np
import json
import time
import os
import sys

sys.setrecursionlimit(2000)

app = Flask(__name__)

# --- CONFIG ---
MIN_VALUE = 1
MAX_VALUE = 50
MIN_GROWTH = 0.01
MAX_GROWTH = 0.05

def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    arr = arr.copy()
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


def generate_data(months, days, start_count):
    full_data = {}
    current_values = None
    
    for month in range(1, months + 1):
        month_key = f"bulan_{month}"
        month_data = {}
        
        for day in range(1, days + 1):
            if month == 1 and day == 1:
                current_values = np.random.randint(MIN_VALUE, MAX_VALUE, start_count).tolist()
            else:
                growth_rate = np.random.uniform(MIN_GROWTH, MAX_GROWTH)
                new_total_count = int(len(current_values) * (1 + growth_rate))
                if new_total_count <= len(current_values):
                    new_total_count = len(current_values) + 1
                num_new_items = new_total_count - len(current_values)
                new_items = np.random.randint(MIN_VALUE, MAX_VALUE, num_new_items).tolist()
                current_values = current_values + new_items
            
            month_data[f"hari_{day}"] = current_values.copy()
        
        full_data[month_key] = month_data
    
    return full_data

def run_benchmark(data):
    results = {}
    
    for month_key in sorted(data.keys(), key=lambda x: int(x.split('_')[1])):
        month_data = data[month_key]
        month_results = {'days': [], 'sizes': [], 'insertion_times': [], 'merge_times': []}
        
        for day_key in sorted(month_data.keys(), key=lambda x: int(x.split('_')[1])):
            arr = month_data[day_key]
            size = len(arr)
            
            start = time.time()
            insertion_sort(arr)
            insertion_time = time.time() - start
            
            start = time.time()
            merge_sort(arr)
            merge_time = time.time() - start
            
            month_results['days'].append(day_key)
            month_results['sizes'].append(size)
            month_results['insertion_times'].append(insertion_time)
            month_results['merge_times'].append(merge_time)
        
        results[month_key] = month_results
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/benchmark', methods=['POST'])
def benchmark():
    params = request.json
    months = params.get('months', 4)
    days = params.get('days', 14)
    start_count = params.get('start_count', 50)
    
    data = generate_data(months, days, start_count)
    results = run_benchmark(data)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
