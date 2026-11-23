---
license: cc-by-4.0
language:
  - en
pretty_name: Jyotisha Reference Dataset & Ayanamsha Benchmark (1900-2050)
tags:
  - vedic-astrology
  - jyotisha
  - astronomy
  - ephemeris
  - ayanamsha
  - nakshatra
  - shodashavarga
  - sidereal
  - reference-data
configs:
  - config_name: nakshatras_27
    data_files: data/nakshatras_27.jsonl
  - config_name: nakshatra_padas_108
    data_files: data/nakshatra_padas_108.jsonl
  - config_name: ayanamsha_benchmark_1900_2050
    data_files: data/ayanamsha_benchmark_1900_2050.jsonl
  - config_name: shodashavarga_specs
    data_files: data/shodashavarga_specs.jsonl
  - config_name: bhava_karakas_12
    data_files: data/bhava_karakas_12.jsonl
---

# Jyotisha Reference Dataset & Ayanamsha Discrepancy Benchmark (1900-2050)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24479752.svg)](https://doi.org/10.5281/zenodo.24479752)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0009--0363--5806-A6CE39.svg)](https://orcid.org/0009-0009-0363-5806)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Open-access, machine-readable reference tables and NASA JPL DE421 astronomical benchmarks for computational Vedic astrology (Jyotisha), maintained by **Tirth Doshi** ([Tantric Astro](https://www.tantricastro.com/), Ahmedabad, India).

## Companion Research Paper & Open Library Book
- **Peer-Archivable Working Paper (CERN Zenodo DOI):** [10.5281/zenodo.24479752](https://doi.org/10.5281/zenodo.24479752) - *True Citrapaksha vs. Mean Lahiri Ayanamsha Discrepancies Across 15 Parashari Divisional Charts and Jaimini Chara Karaka Assignments (1900-2050)*
- **Author ORCID:** [https://orcid.org/0009-0009-0363-5806](https://orcid.org/0009-0009-0363-5806)
- **Companion Book:** *Karaka: The Hand of God in Astrology* (2nd ed., ISBN `979-8163163182`, [Open Library OL46537512W](https://openlibrary.org/works/OL46537512W/K%C4%81raka))
- **Live Interactive Calculators (26 Free Tools):** [https://www.tantricastro.com/calculators/](https://www.tantricastro.com/calculators/)

---

## Dataset Files

| File | Rows | Description |
|---|---:|---|
| `data/nakshatras_27.jsonl` | 27 | Complete 27 Nakshatras (`Ashwini` to `Revati`) with exact sidereal degree boundaries (`13 deg 20'` each), Vimshottari Mahadasha lords and year durations (summing to 120 years), ruling deities, symbols, and Gana classifications. |
| `data/nakshatra_padas_108.jsonl` | 108 | All 108 Nakshatra Padas (`3 deg 20'` each) mapped to sidereal degree ranges, D1 Rashi sign & ruler, and exact D9 Navamsa sign & ruler. |
| `data/ayanamsha_benchmark_1900_2050.jsonl` | 151 | Annual Jan 1 TT time series (1900-2050) comparing **Mean Lahiri** (IAE 1955) vs. **True Citrapaksha** (apparent ecliptic longitude of Alpha Virginis / Spica HIP 65474 minus 180 deg) computed via NASA JPL DE421. |
| `data/shodashavarga_specs.jsonl` | 15 | Classical Parashari definitions and empirical chart-level discrepancy rates (`N = 5,000` charts) across D1, D3, D4, D7, D9, D10, D12, D16, D20, D24, D30, D40, D45, D60, and D108. |
| `data/bhava_karakas_12.jsonl` | 12 | Natural house significators (Bhava Karakas) for all 12 houses per *Brihat Parashara Hora Shastra*. |
| `data/ayanamsha_5000_results.json` | 1 | Full machine-readable summary output from the 5,000-chart NASA JPL DE421 Monte Carlo benchmark. |
| `scripts/run_ayanamsha_study.py` | - | Fully reproducible Python script (Skyfield + NASA JPL DE421 + Hipparcos HIP 65474). |

---

## Key Empirical Highlights (`N = 5,000` Birth Epochs, 1900-2050)
- **Mean Lahiri minus True Citrapaksha:** Mean = **`55.45"`** (SD = `19.14"`, min = `15.90"`, max = `97.38"`, J2000.0 = `75.40"`).
- **Chart-Level Divisional Sign Discrepancy (>= 1 of 9 Grahas flips sign):**
  - **D1 Rashi:** `0.50%`
  - **D9 Navamsa:** `3.72%`
  - **D10 Dasamsa:** `3.84%`
  - **D40 Khavedamsha:** `15.36%`
  - **D45 Akshavedamsha:** `17.76%`
  - **D60 Shashtiamsa:** `21.34%`
  - **D108 Ashtottaramsha:** `36.80%`
- **Jaimini Chara Karaka Rank Swaps:**
  - **7-Karaka scheme (Sun-Saturn):** `0.46%` any-rank swap rate
  - **8-Karaka scheme (with inverted Rahu `30 deg - deg`):** `1.20%` any-rank swap rate (**2.61x** higher sensitivity due to opposite-direction progression of Rahu under sidereal shifts)

---

## Live Open-Access Calculators (Tantric Astro)
Verify any planetary longitude, divisional sign, or Chara Karaka live online:
- [All 26 Free Vedic Astrology Calculators](https://www.tantricastro.com/calculators/)
- [D9 Navamsa Chart Calculator](https://www.tantricastro.com/navamsa-chart-calculator/) | [D10 Dasamsa Calculator](https://www.tantricastro.com/d10-chart-calculator/) | [D40 Khavedamsha Calculator](https://www.tantricastro.com/d40-chart-calculator/) | [D45 Akshavedamsha Calculator](https://www.tantricastro.com/d45-chart-calculator/)
- [D60 Shashtiamsa Calculator](https://www.tantricastro.com/d60-chart-calculator/) | [D108 Ashtottaramsha Calculator](https://www.tantricastro.com/d108-chart-calculator/)
- [Atmakaraka Calculator](https://www.tantricastro.com/atmakaraka-calculator/) | [Darakaraka Calculator](https://www.tantricastro.com/darakaraka-calculator/) | [Ishta Devata Calculator](https://www.tantricastro.com/ishta-devata-calculator/)
- [Nakshatra Calculator](https://www.tantricastro.com/nakshatra-calculator/) | [Vimshottari Dasha Calculator](https://www.tantricastro.com/vimshottari-dasha-calculator/)

---

## Citation
```bibtex
@misc{doshi2026citrapaksha,
  author       = {Doshi, Tirth},
  title        = {True Citrapaksha vs. Mean Lahiri Ayanamsha Discrepancies Across 15 Parashari Divisional Charts and Jaimini Chara Karaka Assignments (1900-2050)},
  month        = nov,
  year         = 2026,
  publisher    = {Tantric Astro / Zenodo},
  doi          = {10.5281/zenodo.24479752},
  url          = {https://doi.org/10.5281/zenodo.24479752}
}
```

---

## Official Author, Podcast & Knowledge Graph Links
- **Website & Free Tools:** [Tantric Astro](https://www.tantricastro.com/) | [All 26 Calculators](https://www.tantricastro.com/calculators/) | [Author Bio](https://www.tantricastro.com/about-us/)
- **The Tantric Astro Podcast:** [Spotify](https://open.spotify.com/show/4kv6hblOZI9lRsBjkzQZcc) | [Apple Podcasts](https://podcasts.apple.com/us/podcast/the-tantric-astro-podcast/id6838476086) | [Pocket Casts](https://pca.st/9avhi5i9)
- **YouTube Teachings:** [@TantricAstro](https://www.youtube.com/@TantricAstro)
- **Academic & Open Access:** [ORCID 0009-0009-0363-5806](https://orcid.org/0009-0009-0363-5806) | [CERN Zenodo DOI 10.5281/zenodo.24479752](https://doi.org/10.5281/zenodo.24479752) | [Hugging Face Mirror](https://huggingface.co/datasets/tirthdos/jyotisha-reference-dataset) | [GitHub Repository](https://github.com/Tirthdoshi/jyotisha-reference-dataset)
- **Book (*Karaka: The Hand of God in Astrology*, ISBN 979-8163163182):** [Amazon Paperback](https://www.amazon.com/dp/B0HNLYSPYK) | [Amazon Author](https://www.amazon.com/author/tirthdoshi) | [Open Library OL46537512W](https://openlibrary.org/works/OL46537512W/K%C4%81raka) | [Goodreads](https://www.goodreads.com/author/show/45938913.Tirth_Doshi)
