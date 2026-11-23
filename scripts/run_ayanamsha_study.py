import os, json, math, random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from skyfield.api import Loader, Star, wgs84
from skyfield.framelib import ecliptic_frame

OUT = r"C:\Users\Tirth\.gemini\antigravity\brain\5b7a9928-a74e-4544-a5d6-1d8a2f184d88\scratch\zenodo_paper"
os.makedirs(OUT, exist_ok=True)
load = Loader(OUT)

print("Loading NASA JPL DE421 ephemeris...")
eph = load("de421.bsp")
ts = load.timescale()

earth = eph["earth"]
bodies = {
    "Sun": eph["sun"],
    "Moon": eph["moon"],
    "Mercury": eph["mercury"],
    "Venus": eph["venus"],
    "Mars": eph["mars"],
    "Jupiter": eph["jupiter barycenter"],
    "Saturn": eph["saturn barycenter"],
}

# Spica (Alpha Virginis, HIP 65474) - Hipparcos / ICRS J2000.0 exact catalog constants
spica = Star(
    ra_hours=(13, 25, 11.5793),
    dec_degrees=(-11, 9, 40.759),
    ra_mas_per_year=-42.35,
    dec_mas_per_year=-30.67,
    parallax_mas=13.06,
    radial_km_per_s=1.0,
)

# Uniformly sample 5,000 birth instants across 1900.0 - 2050.0 (DE421 covers 1899-2053)
rng = np.random.default_rng(20261124)
N = 5000
jd_start = 2415020.5  # 1900-01-01 00:00 TT
jd_end   = 2469807.5  # 2050-01-01 00:00 TT
jds = np.sort(rng.uniform(jd_start, jd_end, size=N))
t = ts.tt_jd(jds)

# 1. Compute True Citrapaksha Ayanamsha = Apparent Ecliptic Longitude of Spica - 180 deg
print("Computing True Citrapaksha (apparent Spica - 180 deg) across 5,000 epochs...")
_, spica_lon, _ = earth.at(t).observe(spica).apparent().frame_latlon(ecliptic_frame)
ayan_citra = (spica_lon.degrees - 180.0) % 360.0

# 2. Compute Standard Mean Lahiri Ayanamsha (IAE 1955 / Swiss Ephemeris SE_SIDM_LAHIRI)
# Exact J2000.0 Lahiri value: 23 deg 51' 25.5324" = 23.857092333 deg
# IAU 2006 / Lieske precession in longitude: p(T) = (5028.796195*T + 1.1054348*T^2)/3600 deg
T = (jds - 2451545.0) / 36525.0
ayan_lahiri = 23.857092333 + (5028.796195 * T + 1.1054348 * (T ** 2)) / 3600.0

diff_arcsec = (ayan_lahiri - ayan_citra) * 3600.0  # Lahiri minus True Citra in arcseconds
print(f"Ayanamsha Delta (Lahiri - True Citrapaksha): mean={np.mean(diff_arcsec):.2f}\", std={np.std(diff_arcsec):.2f}\", min={np.min(diff_arcsec):.2f}\", max={np.max(diff_arcsec):.2f}\"")

# 3. Compute Tropical Geocentric Ecliptic Longitudes for 7 Grahas + Mean Lunar Nodes (Rahu/Ketu)
print("Computing NASA JPL DE421 geocentric ecliptic longitudes for 7 planets + Mean Rahu/Ketu...")
trop = {}
for name, body in bodies.items():
    _, lon, _ = earth.at(t).observe(body).apparent().frame_latlon(ecliptic_frame)
    trop[name] = lon.degrees % 360.0

# Mean Longitude of Ascending Lunar Node (Meeus Ch. 47 / IAU)
rahu_trop = (125.0445479 - 1934.1362891 * T + 0.0020754 * (T**2) + (T**3)/467441.0) % 360.0
trop["Rahu"] = rahu_trop
trop["Ketu"] = (rahu_trop + 180.0) % 360.0

# Sidereal longitudes under both ayanamshas
sid_citra  = {k: (v - ayan_citra) % 360.0 for k, v in trop.items()}
sid_lahiri = {k: (v - ayan_lahiri) % 360.0 for k, v in trop.items()}

# 4. Classical Parashari Varga Sign Calculation (returns sign index 0..11)
def varga_sign(lon_deg, d):
    sign = np.floor(lon_deg / 30.0).astype(int) % 12
    deg = lon_deg % 30.0
    if d == 1:
        return sign
    elif d == 3:  # D3 Drekkana (Parashara)
        part = np.floor(deg / 10.0).astype(int)
        return (sign + part * 4) % 12
    elif d == 4:  # D4 Chaturthamsa
        part = np.floor(deg / 7.5).astype(int)
        return (sign + part * 3) % 12
    elif d == 7:  # D7 Saptamsa
        part = np.floor(deg / (30.0 / 7.0)).astype(int)
        odd = (sign % 2 == 0)  # Aries=0 is odd sign (1st)
        return np.where(odd, (sign + part) % 12, (sign + 6 + part) % 12)
    elif d == 9:  # D9 Navamsa
        return np.floor(lon_deg / (30.0 / 9.0)).astype(int) % 12
    elif d == 10:  # D10 Dasamsa
        part = np.floor(deg / 3.0).astype(int)
        odd = (sign % 2 == 0)
        return np.where(odd, (sign + part) % 12, (sign + 8 + part) % 12)
    elif d == 12:  # D12 Dwadasamsa
        part = np.floor(deg / 2.5).astype(int)
        return (sign + part) % 12
    elif d == 16:  # D16 Shodashamsa (Movable=0, Fixed=4, Dual=8)
        part = np.floor(deg / (30.0 / 16.0)).astype(int)
        start = np.where(sign % 3 == 0, 0, np.where(sign % 3 == 1, 4, 8))
        return (start + part) % 12
    elif d == 20:  # D20 Vimshamsha (Movable=0, Fixed=8, Dual=4)
        part = np.floor(deg / 1.5).astype(int)
        start = np.where(sign % 3 == 0, 0, np.where(sign % 3 == 1, 8, 4))
        return (start + part) % 12
    elif d == 24:  # D24 Siddhamsa (Odd=4 Leo, Even=3 Cancer)
        part = np.floor(deg / 1.25).astype(int)
        odd = (sign % 2 == 0)
        return np.where(odd, (4 + part) % 12, (3 + part) % 12)
    elif d == 30:  # D30 Trimsamsa (Parashara unequal degrees)
        odd = (sign % 2 == 0)
        # Odd: 0-5 Aries(0), 5-10 Aqu(10), 10-18 Sag(8), 18-25 Gem(2), 25-30 Lib(6)
        odd_s = np.where(deg < 5, 0, np.where(deg < 10, 10, np.where(deg < 18, 8, np.where(deg < 25, 2, 6))))
        # Even: 0-5 Tau(1), 5-12 Vir(5), 12-20 Pis(11), 20-25 Cap(9), 25-30 Sco(7)
        ev_s  = np.where(deg < 5, 1, np.where(deg < 12, 5, np.where(deg < 20, 11, np.where(deg < 25, 9, 7))))
        return np.where(odd, odd_s, ev_s)
    elif d == 40:  # D40 Khavedamsha (Odd=0 Aries, Even=6 Libra)
        part = np.floor(deg / 0.75).astype(int)
        odd = (sign % 2 == 0)
        return np.where(odd, part % 12, (6 + part) % 12)
    elif d == 45:  # D45 Akshavedamsha (Movable=0, Fixed=4, Dual=8)
        part = np.floor(deg / (30.0 / 45.0)).astype(int)
        start = np.where(sign % 3 == 0, 0, np.where(sign % 3 == 1, 4, 8))
        return (start + part) % 12
    elif d == 60:  # D60 Shashtiamsa (Parashara: sign + part)
        part = np.floor(deg / 0.5).astype(int)
        return (sign + part) % 12
    elif d == 108:  # D108 Ashtottaramsha (Navamsa-Dwadasamsa)
        return np.floor(lon_deg / (30.0 / 108.0)).astype(int) % 12
    raise ValueError(d)

vargas = [1, 3, 4, 7, 9, 10, 12, 16, 20, 24, 30, 40, 45, 60, 108]
grahas = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
varga_results = {}

for d in vargas:
    per_planet = {}
    any_flip = np.zeros(N, dtype=bool)
    total_flips_per_chart = np.zeros(N, dtype=int)
    for g in grahas:
        s_c = varga_sign(sid_citra[g], d)
        s_l = varga_sign(sid_lahiri[g], d)
        fl = (s_c != s_l)
        per_planet[g] = round(float(np.mean(fl) * 100.0), 3)
        any_flip |= fl
        total_flips_per_chart += fl.astype(int)
    varga_results[f"D{d}"] = {
        "division_arcmin": round(1800.0 / d, 3) if d != 30 else 360.0,
        "mean_planet_flip_pct": round(float(np.mean(list(per_planet.values()))), 3),
        "chart_any_flip_pct": round(float(np.mean(any_flip) * 100.0), 2),
        "mean_planets_flipped_per_chart": round(float(np.mean(total_flips_per_chart)), 3),
        "per_planet_pct": per_planet,
    }

# 5. Jaimini Chara Karaka Swaps (7-Karaka scheme: Sun..Saturn; 8-Karaka scheme: Sun..Saturn + Rahu inverted 30-deg)
def chara_karakas(sid_dict, include_rahu=False):
    names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    degs = [sid_dict[k] % 30.0 for k in names]
    if include_rahu:
        names.append("Rahu")
        degs.append(30.0 - (sid_dict["Rahu"] % 30.0))
    arr = np.vstack(degs)  # shape (K, N)
    # argsort descending along axis 0
    order = np.argsort(-arr, axis=0)
    return order, names

ord7_c, n7 = chara_karakas(sid_citra, False)
ord7_l, _  = chara_karakas(sid_lahiri, False)
ak7_swap = float(np.mean(ord7_c[0] != ord7_l[0]) * 100.0)
dk7_swap = float(np.mean(ord7_c[-1] != ord7_l[-1]) * 100.0)
any7_swap = float(np.mean(np.any(ord7_c != ord7_l, axis=0)) * 100.0)

ord8_c, n8 = chara_karakas(sid_citra, True)
ord8_l, _  = chara_karakas(sid_lahiri, True)
ak8_swap = float(np.mean(ord8_c[0] != ord8_l[0]) * 100.0)
dk8_swap = float(np.mean(ord8_c[-1] != ord8_l[-1]) * 100.0)
any8_swap = float(np.mean(np.any(ord8_c != ord8_l, axis=0)) * 100.0)

# 6. Nakshatra (27) & Pada (108) boundary flip rates (Moon + All 9 Grahas)
moon_nak_flip = float(np.mean((np.floor(sid_citra["Moon"] / (360.0/27.0)) != np.floor(sid_lahiri["Moon"] / (360.0/27.0)))) * 100.0)
moon_pada_flip = float(np.mean((np.floor(sid_citra["Moon"] / (360.0/108.0)) != np.floor(sid_lahiri["Moon"] / (360.0/108.0)))) * 100.0)
any_nak_flip = float(np.mean(np.any([np.floor(sid_citra[g]/(360.0/27.0)) != np.floor(sid_lahiri[g]/(360.0/27.0)) for g in grahas], axis=0)) * 100.0)

# Epoch-level time series (yearly 1900-2050) for Figure 1
years_grid = np.linspace(1900.0, 2050.0, 601)
jds_grid = 2415020.5 + (years_grid - 1900.0) * 365.25
t_grid = ts.tt_jd(jds_grid)
_, sp_g, _ = earth.at(t_grid).observe(spica).apparent().frame_latlon(ecliptic_frame)
ac_g = (sp_g.degrees - 180.0) % 360.0
T_g = (jds_grid - 2451545.0) / 36525.0
al_g = 23.857092333 + (5028.796195 * T_g + 1.1054348 * (T_g ** 2)) / 3600.0
delta_g = (al_g - ac_g) * 3600.0

summary = {
    "sample_size": N,
    "span_years": "1900-2050",
    "ephemeris": "NASA JPL DE421 + Hipparcos HIP 65474 (Alpha Virginis / Spica)",
    "delta_arcsec": {
        "mean": round(float(np.mean(diff_arcsec)), 2),
        "std": round(float(np.std(diff_arcsec)), 2),
        "median": round(float(np.median(diff_arcsec)), 2),
        "min": round(float(np.min(diff_arcsec)), 2),
        "max": round(float(np.max(diff_arcsec)), 2),
        "j2000_delta_arcsec": round(float((23.857092333 - ((earth.at(ts.tt_jd(2451545.0)).observe(spica).apparent().frame_latlon(ecliptic_frame)[1].degrees - 180.0) % 360.0)) * 3600.0), 2),
    },
    "vargas": varga_results,
    "chara_karaka": {
        "scheme_7_ak_swap_pct": round(ak7_swap, 2),
        "scheme_7_dk_swap_pct": round(dk7_swap, 2),
        "scheme_7_any_rank_swap_pct": round(any7_swap, 2),
        "scheme_8_ak_swap_pct": round(ak8_swap, 2),
        "scheme_8_dk_swap_pct": round(dk8_swap, 2),
        "scheme_8_any_rank_swap_pct": round(any8_swap, 2),
    },
    "nakshatra": {
        "moon_nakshatra_flip_pct": round(moon_nak_flip, 3),
        "moon_pada_flip_pct": round(moon_pada_flip, 3),
        "any_graha_nakshatra_flip_pct": round(any_nak_flip, 2),
    }
}

with open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

# Generate Figure 1: Ayanamsha Divergence Time Series (1900-2050)
plt.rcParams["font.family"] = "sans-serif"
fig, ax = plt.subplots(figsize=(8.2, 3.3), dpi=220)
ax.plot(years_grid, delta_g, color="#1B2A4A", linewidth=1.25, label="Mean Lahiri minus True Citrapaksha (arcseconds)")
ax.axhline(np.mean(diff_arcsec), color="#A8352A", linestyle="--", linewidth=1.1, label=f"150-Year Mean = {np.mean(diff_arcsec):.1f}\"")
ax.fill_between(years_grid, 0, delta_g, color="#C9A24F", alpha=0.14)
ax.set_title("Figure 1. Instantaneous Divergence Between Mean Lahiri and True Citrapaksha Ayanamshas (1900-2050)", fontsize=9.5, fontweight="bold", color="#12111F", pad=8)
ax.set_xlabel("Epoch (Year)", fontsize=8.5, color="#222")
ax.set_ylabel("Ayanamsha Difference (arcseconds)", fontsize=8.5, color="#222")
ax.set_xlim(1900, 2050)
ax.grid(True, linestyle=":", alpha=0.55)
ax.legend(fontsize=8, frameon=True, facecolor="white", edgecolor="#CCC")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig1_ayanamsha_delta.png"), dpi=220)
plt.close()

# Generate Figure 2: Chart-Level Discrepancy Rate Across 15 Divisional Charts
labels = [f"D{d}" for d in vargas]
any_pcts = [varga_results[k]["chart_any_flip_pct"] for k in labels]
mean_pcts = [varga_results[k]["mean_planet_flip_pct"] for k in labels]

fig, ax = plt.subplots(figsize=(8.2, 3.6), dpi=220)
x = np.arange(len(labels))
bars = ax.bar(x, any_pcts, width=0.62, color=["#1B2A4A" if p < 10 else ("#9A7420" if p < 25 else "#A8352A") for p in any_pcts], edgecolor="#12111F", linewidth=0.5)
for b, p in zip(bars, any_pcts):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.8, f"{p:.1f}%", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#12111F")
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.2, fontweight="bold")
ax.set_ylabel("Charts with >= 1 Graha Sign Flip (%)", fontsize=8.5, color="#222")
ax.set_title("Figure 2. Percentage of Birth Charts Exhibiting >= 1 Divisional Sign Discrepancy Across 9 Grahas (N = 5,000)", fontsize=9.2, fontweight="bold", color="#12111F", pad=8)
ax.set_ylim(0, max(any_pcts) + 8)
ax.grid(True, axis="y", linestyle=":", alpha=0.55)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig2_varga_discrepancy.png"), dpi=220)
plt.close()

print("DONE! Key Results:")
print(json.dumps({
    "delta_arcsec": summary["delta_arcsec"],
    "D1_any": varga_results["D1"]["chart_any_flip_pct"],
    "D9_any": varga_results["D9"]["chart_any_flip_pct"],
    "D10_any": varga_results["D10"]["chart_any_flip_pct"],
    "D40_any": varga_results["D40"]["chart_any_flip_pct"],
    "D45_any": varga_results["D45"]["chart_any_flip_pct"],
    "D60_any": varga_results["D60"]["chart_any_flip_pct"],
    "D108_any": varga_results["D108"]["chart_any_flip_pct"],
    "chara_karaka": summary["chara_karaka"],
    "nakshatra": summary["nakshatra"],
}, indent=2))
