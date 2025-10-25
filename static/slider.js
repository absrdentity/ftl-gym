let autoSlideInterval; // Biarkan ini tetap global karena digunakan oleh fungsi resetAutoSlide

// Hanya jalankan kode ini setelah seluruh dokumen HTML dimuat
document.addEventListener("DOMContentLoaded", () => {
  // Pindahkan SEMUA deklarasi variabel yang mengambil elemen HTML ke SINI
  let slideIndex = 1;
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");
  const prev = document.querySelector(".prev");
  const next = document.querySelector(".next");

  // Lakukan pemeriksaan keamanan: Hentikan skrip jika elemen penting tidak ditemukan
  if (slides.length === 0 || !prev || !next) {
    console.error(
      "Kesalahan: Elemen slider tidak ditemukan. Periksa kembali HTML Anda."
    );
    return;
  }

  // --- Definisi Fungsi ---

  // Fungsi untuk menampilkan slide tertentu
  function showSlides(n) {
    if (n > slides.length) {
      slideIndex = 1;
    }
    if (n < 1) {
      slideIndex = slides.length;
    }

    // Sembunyikan semua slide dan hilangkan status aktif dari dots
    slides.forEach((slide) => slide.classList.remove("active"));
    dots.forEach((dot) => dot.classList.remove("active"));

    // Tampilkan slide saat ini
    slides[slideIndex - 1].classList.add("active");
    dots[slideIndex - 1].classList.add("active");
  }

  // Fungsi untuk memulai geser otomatis
  function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
      slideIndex++;
      showSlides(slideIndex);
    }, 5000);
  }

  // Fungsi untuk mengatur ulang geser otomatis
  function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
  }

  // Fungsi untuk menggeser ke slide berikutnya/sebelumnya
  function plusSlides(n) {
    slideIndex += n;
    showSlides(slideIndex);
    resetAutoSlide();
  }

  // Fungsi untuk navigasi langsung via dots
  function currentSlide(n) {
    slideIndex = n;
    showSlides(slideIndex);
    resetAutoSlide();
  }

  // Hubungkan event listeners (Tombol dan Dots)
  prev.addEventListener("click", () => plusSlides(-1));
  next.addEventListener("click", () => plusSlides(1));

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => currentSlide(index + 1));
  });

  // --- Inisialisasi ---
  showSlides(slideIndex);
  startAutoSlide();
});

// Catatan: Fungsi resetAutoSlide dan startAutoSlide tidak perlu dideklarasikan ulang
// karena sudah didefinisikan di dalam scope DOMContentLoaded.
