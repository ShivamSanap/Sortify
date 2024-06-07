from flask import Flask, send_file, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    array = [random.randint(1, 500) for _ in range(120)]
    return jsonify(array)

@app.route('/sort', methods=['POST'])
def sort():
    data = request.json
    algorithm = data['algorithm']
    array = data['array']

    if algorithm == 'selection':
        steps = selection_sort(array)
    elif algorithm == 'insertion':
        steps = insertion_sort(array)
    elif algorithm == 'bubble':
        steps = bubble_sort(array)

    return jsonify(steps)

def selection_sort(arr):
    steps = []
    array = arr[:]
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            steps.append({
                'array': array[:],
                'active': [i, j],
                'compared': [min_idx, j],
                'sorted': []
            })
            if array[min_idx] > array[j]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        steps.append({
            'array': array[:],
            'active': [i],
            'compared': [],
            'sorted': list(range(i + 1))
        })
    return steps

def insertion_sort(arr):
    steps = []
    array = arr[:]
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            steps.append({
                'array': array[:],
                'active': [i, j],
                'compared': [j],
                'sorted': []
            })
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
        steps.append({
            'array': array[:],
            'active': [i],
            'compared': [],
            'sorted': list(range(i + 1))
        })
    return steps

def bubble_sort(arr):
    steps = []
    array = arr[:]
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append({
                'array': array[:],
                'active': [j, j + 1],
                'compared': [],
                'sorted': []
            })
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                steps.append({
                    'array': array[:],
                    'active': [j, j + 1],
                    'compared': [j, j + 1],
                    'sorted': list(range(n - i, n))
                })
    return steps

if __name__ == '__main__':
    app.run(debug=True)
