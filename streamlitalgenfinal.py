
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import time

# Fungsi untuk menginisialisasi populasi
def initialize_population(pop_size, num_genes):
    population = np.random.rand(pop_size, num_genes)
    population /= population.sum(axis=1)[:, None]  # Normalisasi
    return population

# Fungsi untuk menghitung fitness individu
def calculate_fitness(individual, biaya_produksi, hasil_produksi, luas_lahan, harga_jual, anggaran):
    total_biaya = sum(individual * luas_lahan * biaya_produksi)
    if total_biaya > anggaran:
        return -np.inf  # Fitness sangat rendah jika melebihi anggaran
    pendapatan = sum(individual * luas_lahan * hasil_produksi * harga_jual)
    return pendapatan - total_biaya

# Fungsi untuk seleksi roulette wheel
def roulette_wheel_selection(population, fitness):
    total_fitness = sum(fitness)
    relative_fitness = fitness / total_fitness
    probabilities = np.cumsum(relative_fitness)
    chosen_index = np.searchsorted(probabilities, np.random.random())
    return population[chosen_index]

# Fungsi untuk crossover aritmetika
def arithmetic_crossover(parent1, parent2, alpha=0.5):
    return alpha * parent1 + (1 - alpha) * parent2

# Fungsi untuk mutasi non-uniform
def non_uniform_mutation(individual, generation, max_generations, b=5):
    for i in range(len(individual)):
        if np.random.rand() < 0.1:  # Mutasi berdasarkan laju mutasi
            delta = (1 - np.power(np.random.rand(), np.power((1 - generation/max_generations), b)))
            individual[i] += delta
    individual /= individual.sum()  # Normalisasi
    return individual

# Algoritma genetika utama
def genetic_algorithm(pop_size, num_genes, max_generations, biaya_produksi, hasil_produksi, luas_lahan, harga_jual, anggaran, mutation_rate, crossover_rate, max_consecutive_generations_without_improvement):
    start_time = time.time() # Waktu mulai program
    progress_bar = st.progress(0)

    population = initialize_population(pop_size, num_genes)
    fitness_history = []
    best_individual_per_generation = []

    best_fitness = float('-inf')
    consecutive_generations_without_improvement = 0

    for generation in range(max_generations):
        fitness = np.array([calculate_fitness(ind, biaya_produksi, hasil_produksi, luas_lahan, harga_jual, anggaran) for ind in population])
        best_fitness_idx = np.argmax(fitness)
        current_best_fitness = fitness[best_fitness_idx]

        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            consecutive_generations_without_improvement = 0
        else:
            consecutive_generations_without_improvement += 1

        fitness_history.append(current_best_fitness)
        best_individual_per_generation.append(population[best_fitness_idx])
        progress_bar.progress((generation + 1) / max_generations)

        # Stopping criteria (Menghentikan iterasi jika tidak ada peningkatan dalam beberapa generasi)
        if consecutive_generations_without_improvement >= max_consecutive_generations_without_improvement:
            st.warning(f"Berhenti lebih awal karena tidak ada peningkatan keuntungan selama {max_consecutive_generations_without_improvement} generasi berturut-turut.")
            break

        # Menambahkan diversitas ke populasi dengan menyertakan beberapa individu acak
        num_mutations = max(1, int(pop_size * mutation_rate))
        new_population = [initialize_population(1, num_genes).flatten() for _ in range(num_mutations)]

        while len(new_population) < pop_size:
            parent1 = roulette_wheel_selection(population, fitness)
            parent2 = roulette_wheel_selection(population, fitness)

            if np.random.rand() < crossover_rate:
                child = arithmetic_crossover(parent1, parent2)
            else:
                child = parent1.copy()  # Tidak ada crossover, anak identik dengan parent1

            if np.random.rand() < mutation_rate:
                child = non_uniform_mutation(child, generation, max_generations)
            new_population.append(child)

        population = np.array(new_population)

    end_time = time.time() # Waktu berakhir program
    elapsed_time = end_time - start_time
    st.write(f"Total waktu yang dibutuhkan: {elapsed_time:.2f} detik")

    best_index = np.argmax(fitness)
    return population[best_index], fitness[best_index], fitness_history, best_individual_per_generation

# Fungsi untuk memplot alokasi lahan menggunakan pie chart
def plot_allocation(allocation, tanaman_labels):
    fig, ax = plt.subplots(figsize=(12, 12))
    wedges, texts, autotexts = ax.pie(
        allocation,
        labels=tanaman_labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
        textprops={'color': 'white', 'weight': 'bold'},
    )
    for text in texts:
        text.set_size(15)
    # Mengatur latar belakang transparan
    plt.setp(wedges, edgecolor='white', linewidth=1)
    plt.setp(autotexts, size=15, weight="bold", color='black')
    plt.title('Alokasi Lahan untuk Setiap Jenis Tanaman', color='white', fontsize=25, weight="bold")

    # Simpan plot sebagai gambar PNG
    plt.savefig("allocation_plot.png", transparent=True)
    st.image("allocation_plot.png", use_column_width=True)


# Fungsi untuk memplot fitness terbaik selama generasi
from matplotlib.ticker import ScalarFormatter
def plot_fitness(fitness_history):
    plt.rcParams['axes.edgecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = '#808080'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(fitness_history, color='limegreen', linewidth=3)
    ax.set_xlabel('Generasi', color='white', fontsize=15, weight='bold')
    ax.set_ylabel('Fitness Terbaik', color='white', fontsize=15, weight='bold')
    plt.title('Perkembangan Fitness Terbaik Sepanjang Generasi', color='white', pad=35, weight="bold", fontsize=20)
    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 10
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=False))
    ax.yaxis.get_offset_text().set_fontsize(15)
    # Menetapkan warna teks pada sumbu
    ax.tick_params(axis='x', colors='white', which='both', labelsize=15)
    ax.tick_params(axis='y', colors='white', which='both', labelsize=15)

    # Simpan plot sebagai gambar PNG
    plt.savefig("fitness_plot.png", transparent=True)
    st.image("fitness_plot.png", use_column_width=True)


# Fungsi utama untuk menjalankan aplikasi Streamlit

def main():
    st.set_page_config(page_title="Optimasi Lahan Pertanian", page_icon="👩‍🌾")
    st.title("Optimasi Penataan Lahan Pertanian dengan Algoritma Genetika")

    with st.sidebar:
        st.subheader("Pengaturan GA")

        max_consecutive_generations_without_improvement = st.number_input("Batas Generasi Tanpa Peningkatan", min_value=10, value=50, step=10)
        pop_size = st.number_input("Ukuran Populasi", min_value=10, value=50, step=10)
        max_generations = st.number_input("Maksimum Generasi", min_value=10, value=100, step=10)
        mutation_rate = st.number_input("Laju Mutasi", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
        crossover_rate = st.number_input("Laju Crossover", min_value=0.01, max_value=1.0, value=0.5, step=0.01)

    with st.form(key='my_form'):
        num_tanaman = 4  # Jumlah tanaman tetap
        biaya_produksi = []
        hasil_produksi = []
        harga_jual = []
        tanaman_labels = []

        # Bagian input untuk masing-masing tanaman
        for i in range(num_tanaman):
            st.subheader(f"Tanaman {i+1}")
            nama_tanaman = st.text_input(f"Nama Tanaman {i+1}", value=f"Tanaman {i+1}")
            tanaman_labels.append(nama_tanaman)
            biaya_produksi.append(st.number_input(f"Biaya produksi per hektar (IDR) untuk {nama_tanaman}", value=1000000))
            hasil_produksi.append(st.number_input(f"Hasil produksi per hektar (ton) untuk {nama_tanaman}", value=12.0))
            harga_jual.append(st.number_input(f"Harga jual per ton (IDR) untuk {nama_tanaman}", value=200000))

        # Memisahkan input luas lahan dan anggaran
        st.subheader("Input Umum")
        luas_lahan = st.number_input("Total luas lahan (hektar)", value=10.0)
        anggaran = st.number_input("Anggaran maksimum (IDR)", value=20000000)
        submit_button = st.form_submit_button(label='Optimasi Lahan')

    if submit_button:
        best_solution, best_fitness, fitness_history, best_individuals = genetic_algorithm(
            pop_size, num_tanaman, max_generations, biaya_produksi, hasil_produksi, luas_lahan, harga_jual, anggaran, mutation_rate, crossover_rate, max_consecutive_generations_without_improvement
        )

        st.header("Hasil Optimasi Lahan")
        st.subheader(f"**Keuntungan Maksimum (IDR):** `{best_fitness:,.2f}`")
        st.write(f"Jumlah generasi untuk mencapai solusi terbaik: {len(best_individuals)}")

        # Tampilkan grafik alokasi lahan
        plot_allocation(best_solution, tanaman_labels)
        # Tampilkan grafik perkembangan fitness
        plot_fitness(fitness_history)

if __name__ == "__main__":
    main()